import os
import string
import random
from datetime import datetime, timezone
from typing import Optional, Union

from .static import static as django_dataio_static

def random_string(length: int = 16) -> str:
    """
    Generates a random alphanumeric string.

    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

def time_now(frmt: Optional[str] = None) -> Union[datetime, str]:
    """
    Returns the current UTC datetime, optionally formatted as a string.
    """
    t = datetime.now(timezone.utc)
    if frmt:
        return t.strftime(frmt)
    return t


def create_folder(path: str) -> str:
    """
    Creates a folder at the given path if it doesn't exist.

    Returns:
        str: The absolute path to the created (or existing) folder.
    """
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)