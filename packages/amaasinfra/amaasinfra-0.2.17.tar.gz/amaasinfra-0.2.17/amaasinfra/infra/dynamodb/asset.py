from amaasinfra.infra.dynamodb.amaas_model import AMaaSModel
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute

class Asset(AMaaSModel):
    asset_id = UnicodeAttribute(range_key=True)
    asset_class = UnicodeAttribute(null=False)
    asset_type = UnicodeAttribute(null=False)
    asset_status = UnicodeAttribute(null=False)
    fungible = BooleanAttribute()
    hashcode = UnicodeAttribute(null=False)

    