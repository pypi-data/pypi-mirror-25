import os
import logging
from typing import List
from amaasinfra.authorization.token_utils import TokenAttribute, unpack_token
from amaasinfra.infra.dynamodb.asset_manager_relationship import AssetManagerRelationship

class AMaaSUser(object):
    def __init__(self, token: str) -> None:
        self.logger = logging.getLogger()
        attributes = unpack_token(token)
        # require asset_manager_id
        self.asset_manager_id = int(attributes[TokenAttribute.asset_manager_id.value])
        self.username = attributes.get(TokenAttribute.username.value, None)
        self.email = attributes.get(TokenAttribute.email.value, None)
        # amid 0-9 are reserved for system users
        self.system_user = self.asset_manager_id < 10
        self.relationships: List[AssetManagerRelationship] = []
        self.data_sources: List[int] = []
        self.asset_manager_permissions: List[int] = []
        self.book_permissions: List[str] = []
        self.environment = os.environ.get('AWS_ENV')

    def load_relationships(self) -> 'AMaaSUser':
        self.relationships = [rel for rel in AssetManagerRelationship
                              .related_id_index.query(self.asset_manager_id)]
        return self

    def load_data_sources(self) -> 'AMaaSUser':
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

    def check_asset_manager_permissions(self, asset_manager_id_claims: List[int]) -> List[int]:
        """
        Returns a list of asset manager ids from the list of claims that the user does not have acess to
        """
        error_asset_manager_ids = [asset_manager_id for asset_manager_id in asset_manager_id_claims
                                   if asset_manager_id not in self.asset_manager_permissions]
        return error_asset_manager_ids

    def check_book_permissions(self, book_id_claims: List[str]) -> None:
        pass
