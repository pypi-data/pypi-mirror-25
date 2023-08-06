from amaasinfra.infra.dynamodb.amaas_model import AMaaSModel
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

class AssetClassIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'asset_class_index'
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    asset_class = UnicodeAttribute(hash_key=True)

class Asset(AMaaSModel):
    asset_id = UnicodeAttribute(range_key=True)
    asset_class_index = AssetClassIndex()
    asset_class = UnicodeAttribute(null=False)
    asset_type = UnicodeAttribute(null=False)
    asset_status = UnicodeAttribute(null=False)
    fungible = BooleanAttribute()
    hashcode = UnicodeAttribute(null=False)

    