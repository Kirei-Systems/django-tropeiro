from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
import functools
import os


@functools.cache
def load_dotenv():
    try:
        import dotenv  # type: ignore

        dotenv.load_dotenv()
    except ModuleNotFoundError:
        pass


def project_dir() -> Path:
    project_dir = Path(os.getcwd())
    return Path(project_dir)


def project_name() -> str:
    val = os.environ.get("DJANGO_SETTINGS_MODULE")
    if val is None:
        raise ImproperlyConfigured("Missing DJANGO_SETTINGS_MODULE env var.")
    return val.split(".")[0].replace("_", "-")


load_dotenv()
