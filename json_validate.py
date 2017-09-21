schema_users_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["name", "password"],
    "additionalProperties": False
}

schema_sessions_post = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["name", "password"],
    "additionalProperties": False
}

SCHEMA = {
    'schema_users_post': schema_users_post,
    'schema_sessions_post': schema_sessions_post
}

schema_token = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string"}
    },
    "required": ["id"],
    "additionalProperties": False
}

SCHEMA_INTERNAL = {
   'schema_token': schema_token
}
