from amaasinfra.infra.dynamodb.amaas_model import AMaaSModel
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

class UserIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'user_id_index'
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    user_asset_manager_id =  NumberAttribute(hash_key=True)

class BookPermission(AMaaSModel):
    book_id = UnicodeAttribute(range_key=True)
    user_id_index = UserIdIndex()
    user_asset_manager_id = NumberAttribute(null=False)
    permission_status = UnicodeAttribute(null=False)
    permission = UnicodeAttribute(null=False)
