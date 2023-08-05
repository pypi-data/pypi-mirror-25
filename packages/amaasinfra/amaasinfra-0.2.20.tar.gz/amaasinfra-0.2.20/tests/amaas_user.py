"""
Crude tests.  Need a better way to mock out the DynamoDB calls
"""
import unittest
from mock import patch
from amaasinfra.authorization.amaas_user import AMaaSUser
from amaasinfra.authorization.token_utils import TokenAttribute

class AMaaSUserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    @patch('amaasinfra.authorization.amaas_user.unpack_token')
    @patch('amaasinfra.authorization.amaas_user.AssetManagerRelationship')
    def testCheckAmidPermissions(self, mock_relationship, mock_unpack_token):
        mock_unpack_token.return_value = {TokenAttribute.asset_manager_id.value: 1}
        user = AMaaSUser('')
        user.asset_manager_permissions = [1, 10, 11, 12, 101]

        errors = user.check_asset_manager_permissions([1, 10, 11, 12])
        self.assertTrue(len(errors) == 0)

        errors = user.check_asset_manager_permissions([101])
        self.assertTrue(len(errors) == 0)

        errors = user.check_asset_manager_permissions(['101'])
        self.assertTrue(len(errors) == 0)

        errors = user.check_asset_manager_permissions([101,102])
        self.assertTrue(102 in errors)

        with self.assertRaises(ValueError):
            errors = user.check_asset_manager_permissions(['Invalid101'])
        
    @patch('amaasinfra.authorization.amaas_user.unpack_token')
    @patch('amaasinfra.authorization.amaas_user.AssetManagerRelationship')
    def testCheckNewUserPermissions(self, mock_relationship, mock_unpack_token):
        mock_unpack_token.return_value = {TokenAttribute.username.value: 'new_user'}
        user = AMaaSUser('')
        
        claims = [10, 11, 12, 101]
        errors = user.check_asset_manager_permissions(claims)
        self.assertEqual(claims, errors)
    
    def testLoadRelationships(self):
        pass
    
    def testLoadDataSources(self):
        pass
    
    def testLoadAssetManagerIdPermissions(self):
        pass

if __name__ == '__main__':
    unittest.main()