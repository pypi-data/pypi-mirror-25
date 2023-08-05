import os
import logging
from typing import List
from amaasinfra.authorization.token_utils import TokenAttribute, unpack_token
from amaasinfra.authorization.user_permission import UserPermission
from amaasinfra.infra.dynamodb.asset_manager_relationship import AssetManagerRelationship
from amaasinfra.infra.dynamodb.book_permission import BookPermission

class AMaaSUser(object):
    def __init__(self, token: str) -> None:
        self.logger = logging.getLogger()
        attributes = unpack_token(token)
        user_amid = attributes.get(TokenAttribute.asset_manager_id.value)
        self.asset_manager_id = int(user_amid) if user_amid else None
        self.username = attributes.get(TokenAttribute.username.value)
        self.email = attributes.get(TokenAttribute.email.value)
        self.firstname = attributes.get(TokenAttribute.first_name.value, '')
        self.lastname = attributes.get(TokenAttribute.last_name.value, '')
        # amid 0-9 are reserved for system users
        self.system_user = self.asset_manager_id < 10 if self.asset_manager_id else False
        self.relationships: List[AssetManagerRelationship] = []
        self.data_sources: List[int] = []
        self.asset_manager_permissions: List[int] = []
        self.book_permissions: List[BookPermission] = []
        self.environment = os.environ.get('AWS_ENV')

    def load_relationships(self) -> 'AMaaSUser':
        if self.asset_manager_id is None:
            return self

        self.relationships = [rel for rel in AssetManagerRelationship
                            .related_id_index.query(self.asset_manager_id, relationship_status__eq='Active')]
        return self

    def load_data_sources(self) -> 'AMaaSUser':
        if self.asset_manager_id is None:
            return self

        if not self.relationships:
            self.load_relationships()

        asset_manager_ids = [rel.asset_manager_id for rel in self.relationships]
        data_providers = set()
        for asset_manager_id in asset_manager_ids:
            data_providers |= {rel.related_id
                            for rel in AssetManagerRelationship.query(hash_key=asset_manager_id,
                                                                      relationship_type__eq='Data Provider')}
        self.data_sources = list(data_providers)
        return self

    def load_asset_manager_permissions(self) -> 'AMaaSUser':
        if self.asset_manager_id is None:
            return self

        if not self.relationships:
            self.load_relationships()

        if not self.data_sources:
            self.load_data_sources()

        permissions = set()
        permissions |= {self.asset_manager_id}
        permissions |= {rel.asset_manager_id for rel in self.relationships}
        permissions |= {data_source for data_source in self.data_sources}
        self.asset_manager_permissions = list(permissions)

        return self

    def load_book_permissions(self) -> 'AMaaSUser':
        if self.asset_manager_id is None:
            return self

        self.book_permissions = [perm for perm in
                                 BookPermission.user_id_index.query(self.asset_manager_id,
                                                                    permission_status__eq='Active')]

    def check_asset_manager_permissions(self, asset_manager_id_claims: List[int]) -> (bool, List[int]):
        """
        Returns the asset_manager_ids that the user does not have access to
        """
        error_asset_manager_ids = [int(asset_manager_id) for asset_manager_id in asset_manager_id_claims
                                   if int(asset_manager_id) not in self.asset_manager_permissions]
        return error_asset_manager_ids


    def check_book_permissions(self, asset_manager_id, book_id, permission) -> None:
        if self.book_permissions is None:
            self.load_book_permissions()
        for book_permission in self.book_permissions:
            if (book_permission.book_id == book_id or book_permission.book_id == '*') and book_permission.asset_manager_id == asset_manager_id:
                if permission == 'write' and book_permission.permission == 'read':
                    raise TypeError('User %s does not have requested %s access to the book: %s'%(self.asset_manager_id, permission, book_id))
                return None
        raise TypeError('User %s does not have requested %s access to the book: %s'%(self.asset_manager_id, permission, book_id))