from pathlib import Path
import os


def project_dir() -> Path:
    project_dir = Path(os.getcwd())
    return Path(project_dir)


def project_name() -> str:
    pdir = project_dir()
    name = pdir.name
    if not pdir.joinpath(name).exists():
        print(
            "gpsettings expects the project root and settings module to be named the same."
        )
        raise Exception("Expected django project to be run at project root.")
    return name


def set_settings_module():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name()}.settings")
