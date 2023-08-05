class UserPermission(object):
    def __init__(self, permission_type: str, read: bool, write: bool):
        self.permission_type = permission_type
        self.read = read
        self.write = write