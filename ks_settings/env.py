from pathlib import Path
import functools
import os


@functools.cache
def load_dotenv():
    try:
        import dotenv

        dotenv.load_dotenv()
    except ModuleNotFoundError:
        pass


def project_dir() -> Path:
    project_dir = Path(os.getcwd())
    return Path(project_dir)


def project_name() -> str:
    pdir = project_dir()
    name = pdir.name
    modpath = pdir.joinpath(name)
    if not modpath.exists():
        raise Exception(
            "ks_settings expects the project root and settings module to be named the same.\n"
            f"Please make sure {modpath} exists."
        )
    return name


def set_settings_module():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name()}.settings")


load_dotenv()
