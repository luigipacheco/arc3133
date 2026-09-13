"""Replace generated outputs atomically while editors or preview servers read them."""
import os
from pathlib import Path
import tempfile


def write_text(path, content):
    path = Path(path)
    handle, temporary = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(handle, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
