import io
import json


def str_to_utf8(s):
    """Return utf-8 encoded string."""
    return unicode(s).encode("utf-8")


def list_to_utf8(l):
    """Return utf-8 encoded list."""
    return [str_to_utf8(s) for s in l]


def dict_to_utf8(d):
    """Return utf-8 encoded dict."""
    return {str_to_utf8(k): str_to_utf8(v) for k, v in d.items()}


def save_utf8_json(data, target_path):
    """Write the merged data into the target file."""
    with io.open(target_path, 'wt', encoding='utf8') as target_file:
        target_file.write(unicode(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)))
