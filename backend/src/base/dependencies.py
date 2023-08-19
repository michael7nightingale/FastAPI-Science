from fastapi_authtools.exceptions import raise_permissions_error


def check_object_permissions(obj, user, field_name):
    if getattr(obj, field_name) != user.id:
        raise_permissions_error()
