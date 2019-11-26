def has_permission(user, permission):
    for role in user.role_set:
        for per in role.permission_set:
            if per.id == permission.id:
                return True
    return False
