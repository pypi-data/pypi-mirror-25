import os
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

class RelatedIdIndex(GlobalSecondaryIndex):
    """
    Index for RelatedId.  Allows us to query for all relationships of a given RelatedId easily
    """
    class Meta:
        index_name = "related_id_index"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    
    related_id = UnicodeAttribute(hash_key=True)

class AssetManagerRelationshipCacheItem(Model):
    """
    Cached record for asset manager
    """
    class Meta:
        environment = os.environ.get('AWS_ENV') or 'dev'
        region = os.environ.get('AWS_DEFAULT_REGION', 'ap-southeast-1')
        table_name = "asset-manager-relationship-cache-{}".format(environment.lower())
    
    asset_manager_id = UnicodeAttribute(hash_key=True)
    related_id_index = RelatedIdIndex()
    related_id = UnicodeAttribute(range_key=True)
    relationship_type = UnicodeAttribute(null = False)
    relationship_status = UnicodeAttribute(null = False)    

