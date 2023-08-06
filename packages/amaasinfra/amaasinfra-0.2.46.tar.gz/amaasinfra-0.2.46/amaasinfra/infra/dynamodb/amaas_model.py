import os
import six
from pynamodb.attributes import NumberAttribute, UTCDateTimeAttribute, UnicodeAttribute
from pynamodb.models import Model
from pynamodb.models import MetaModel
from pynamodb.connection.util import pythonic

def table_name(name):
    return name + '_' + os.environ.get('AWS_ENV', 'DEV').lower()

def table_region():
    return os.environ.get('AWS_DEFAULT_REGION', 'ap-southeast-1')

class MetaBase(MetaModel):
    def __new__(cls, name, bases, d, **kwargs):
        d['Meta'] = type('Meta', (), {
            'table_name': table_name(pythonic(name)),
            'region': table_region(),
            'read_capacity_units': 5,
            'write_capacity_units': 5
        })
        return MetaModel.__new__(cls, name, bases, d, **kwargs)

class ModelBase(Model):
    asset_manager_id = NumberAttribute(hash_key=True)
    created_by = UnicodeAttribute(null=False)
    created_time = UTCDateTimeAttribute(null=False)
    updated_by = UnicodeAttribute(null=False)
    updated_time = UTCDateTimeAttribute(null=False)

AMaaSModel = six.with_metaclass(MetaBase, ModelBase)


