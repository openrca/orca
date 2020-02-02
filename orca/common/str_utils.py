def escape(s):
    escaped = s.replace('"', '\\"')
    escaped = escaped.replace('\n', '\\n')
    return escaped
