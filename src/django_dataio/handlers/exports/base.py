import abc
from pathlib import Path
from typing import Iterable, Optional, Type

from django.conf import settings
from django.db import models

from django_dataio import utils


class BaseExporter(abc.ABC):
    """
    Base abstract class for all data exporters.

    This class defines the common interface and shared logic for exporting
    Django model data into different formats (e.g. Excel, CSV, JSON).
    """

    check_dependencies: Optional[bool] = None
    name: Optional[str] = None
    fields: Optional[models.QuerySet] = None
    model: Optional[Type[models.Model]] = None
    queryset: Optional[Iterable[models.Model]] = None

    base_export_folder: Path = (
    Path(settings.MEDIA_ROOT)
        if settings.MEDIA_ROOT
        else settings.BASE_DIR / "django_dataio_media")
    export_folder: Path = base_export_folder / "django_dataio_exports"

    def __init__(
        self,
        name: str,
        model: Type[models.Model],
        fields: models.QuerySet,
    ) -> None:
        """
        Initialize exporter.

        :param name: Exporter name
        :param model: Django model to exports
        :param fields: Fields queryset
        """
        self.name = name
        self.model = model
        self.fields = fields
        self.fields_name_list: list[str] = list(
            self.fields.values_list('name', flat=True)
        )
        self.queryset = self.model.objects.all().iterator()

    @classmethod
    def _check_dependencies(cls) -> Optional[bool]:
        """
        Check exporter dependencies.
        """
        return cls.check_dependencies

    @classmethod
    def is_active(cls, strict: bool = False) -> bool:
        """
        Check if exporter is usable.

        :param strict: Raise error if dependencies are missing
        :return: True if active, otherwise False
        """
        if not cls._check_dependencies():
            if strict:
                raise ImportError(
                    f"Exporter {cls.__name__} cant be used, dependencies not installed."
                )
            return False
        return True

    @abc.abstractmethod
    def _export_location(self) -> Path:
        """
        Return exports file path.
        """
        raise NotImplementedError

    def _prepare_perform(self) -> None:
        """
        Prepare exports directories.
        """
        utils.create_folder(self.base_export_folder)
        utils.create_folder(self.export_folder)

    @abc.abstractmethod
    def _save(self) -> None:
        """
        Save exported data.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def perform(self) -> Path:
        """
        Run exports process.

        :return: Path of exported file
        """
        raise NotImplementedError
