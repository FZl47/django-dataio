from typing import Dict, Type

from .excel import ExcelImporter
from .base import BaseImporter

IMPORTER: Dict[str, Type[BaseImporter]] = {
    "excel": ExcelImporter,
}

ACTIVE_IMPORTER: Dict[str, Type[BaseImporter]] = {}


def _initial_importer_cls() -> None:
    """
    Initialize active importers based on dependency availability.
    """
    for name, imp_cls in IMPORTER.items():
        if not imp_cls.is_active():
            continue
        ACTIVE_IMPORTER[name] = imp_cls


_initial_importer_cls()


def get_importer(name: str) -> Type[BaseImporter]:
    """
    Get importer class by name.

    :param name: Importer name (e.g. "excel")
    :return: Importer class
    :raises ValueError: If importer does not exist or is inactive
    """
    try:
        return ACTIVE_IMPORTER[name]
    except KeyError:
        raise ValueError(
            f"There is no importer with '{name}' name or it is inactive"
        )
