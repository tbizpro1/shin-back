from .user_permission import BaseAcess

class UserPermission(BaseAcess):

    ROLE_USER = "user"


class AdminPermission(BaseAcess):

    ROLE_USER = "admin"
