from typing import Dict, Type

from .excel import ExcelExporter
from .base import BaseExporter

EXPORTER: Dict[str, Type[BaseExporter]] = {
    "excel": ExcelExporter,
}

ACTIVE_EXPORTER: Dict[str, Type[BaseExporter]] = {}


def _initial_exporter_cls() -> None:
    """
    Initialize active exporters based on dependency availability.
    """
    for name, exp_cls in EXPORTER.items():
        if not exp_cls.is_active():
            continue
        ACTIVE_EXPORTER[name] = exp_cls


_initial_exporter_cls()


def get_exporter(name: str) -> Type[BaseExporter]:
    """
    Get exporter class by name.

    :param name: Exporter name (e.g. "excel")
    :return: Exporter class
    :raises ValueError: If exporter does not exist or is inactive
    """
    try:
        return ACTIVE_EXPORTER[name]
    except KeyError:
        raise ValueError(
            f"There is no exporter with '{name}' name or it is inactive"
        )
