

def validateCreateUser(user):
    if not user["name"]:
        return False
    if not user["email"]:
        return False
    if not user["password"]:
        return False
    if len(user["password"]) < 5:
        return False
    if not user["name"].isalnum():
        return False
    if '@' not in user["email"]:
        return False
    return True

def validateUpdateUser(user):
    if "email" in user.keys():
        if '@' not in user["email"]:
            return False
    if "password" in user.keys():
        if len(user["password"]) < 5:
            return False
    if "name" in user.keys():
        if not user["name"].isalnum():
            return False
    return True