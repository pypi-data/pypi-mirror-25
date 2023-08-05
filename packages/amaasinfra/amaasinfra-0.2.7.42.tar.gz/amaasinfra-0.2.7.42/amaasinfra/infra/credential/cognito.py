from enum import Enum
from typing import List, Any
import jwt

class TokenAttribute(Enum):
    username = 'cognito:username'
    email = 'cognito:email'
    asset_manager_id = 'custom:asset_manager_id'

def unpack_token(token: str, *additional_attributes: TokenAttribute) -> List[Any]:
    """
    Unpacks the Cognito token attributes into a list of their values.
    
    Args:
        token: the encoded jwt token from the Authorization request header
        *additional_attributes: optional token attributes to be unpacked and returned
    
    Returns:
        List[Any]: the list containing the username and asset_manager_id and any
        *additional_attributes were specified
    """
    contents = jwt.decode(token, verify=False)
    username = contents.get('cognito:username')
    asset_manager_id = int(contents.get('custom:asset_manager_id', '0'))
    results = [username, asset_manager_id]

    for attr in additional_attributes:
        if not isinstance(attr, TokenAttribute):
            raise ValueError('Invalid token attribute specified.')
        
        results.append(contents.get(attr.value))

    return results