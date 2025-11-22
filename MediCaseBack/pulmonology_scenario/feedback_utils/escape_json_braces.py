import json

def escape_json_braces(data) -> str:
    json_str = json.dumps(data, ensure_ascii=False)
    return json_str.replace('{', '{{').replace('}', '}}')
