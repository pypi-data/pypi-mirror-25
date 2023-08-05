import re

def camel_to_snake(s):
    """Convert string from camel case to snake case"""
    return re.sub("([A-Z])", "_\\1", s).lower().lstrip("_")