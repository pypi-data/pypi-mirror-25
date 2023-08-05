from typing import List
from token_utils import TokenAttribute, unpack_token
from amaasinfra.infra.dynamodb.asset_manager_relationship import AssetManagerRelationship

class AMaaSUser(object):
    def __init__(self, token: str) -> None:
        attributes = unpack_token(token)
        # require asset_manager_id
        self.asset_manager_id = int(attributes[TokenAttribute.asset_manager_id.value])
        self.username = attributes.get(TokenAttribute.username.value, None)
        self.email = attributes.get(TokenAttribute.email.value, None)
        # amid 0-9 are reserved for system users
        self.system_user = asset_manager_id < 10
        self.relationships: List[AssetManagerRelationship] = []
        self.data_sources: List[int] = []
        self.permissions: List[int] = []

    
    def load_permissions(self) -> AMaaSUser:
        if not self.relationships:
            self.relationships = AssetManagerRelationship.related_id_index.query(self.asset_manager_id)
        if not self.data_sources:
            asset_manager_ids = [rel.asset_manager_id for rel in self.relationships]
            data_providers = set()
            for asset_manager_id in asset_manager_ids:
                data_providers |= {rel.related_id 
                                   for rel in AssetManagerRelationship.query(
                                       hash_key=asset_manager_id,
                                       relationship_type__eq='Data Provider')}
            self.data_sources = list(data_providers)
        
        if not self.permissions:
            permissions = set()
            permissions |= self.asset_manager_id
            permissions |= {rel.asset_manager_id for rel in relationships}
            permissions |= {data_source for data_source in self.data_sources}
            self.permissions = list(permissions)
