import re


def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9.@_\\+\\-\\|]'
    print(username)
    print(re.match(pattern, username))
    return bool(re.match(pattern, username))