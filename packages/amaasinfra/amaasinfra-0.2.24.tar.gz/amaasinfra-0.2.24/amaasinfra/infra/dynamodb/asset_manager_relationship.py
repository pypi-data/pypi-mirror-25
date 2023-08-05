from amaasinfra.infra.dynamodb.amaas_model import AMaaSModel
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

class RelatedIdIndex(GlobalSecondaryIndex):
    """
    Index for RelatedId.  
    Allows us to query for all relationships of a given RelatedId without 
    specifying the asset_manager_id partition key.
    """
    class Meta:
        index_name = "related_id_index"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    related_id = NumberAttribute(hash_key=True)

class AssetManagerRelationship(AMaaSModel):
    related_id_index = RelatedIdIndex()
    related_id = NumberAttribute(range_key=True)
    relationship_type = UnicodeAttribute(null=False)
    relationship_status = UnicodeAttribute(null=False)
    
    