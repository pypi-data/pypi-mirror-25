from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from amaasinfra.infra.dynamodb.amaas_model import AMaaSModel

class WorkflowContext(AMaaSModel):
    workflow_id = UnicodeAttribute(range_key=True)
    workflow_type = UnicodeAttribute(null=False)
    token = UnicodeAttribute(null=False)
    context = UnicodeAttribute()