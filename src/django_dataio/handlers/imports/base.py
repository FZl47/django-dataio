import abc
from pathlib import Path
from typing import Iterable, Optional, Type, Any

from django.conf import settings
from django.db import models

from django_dataio import utils


class BaseImporter(abc.ABC):
    """
    Base abstract class for all data importers.

    This class defines the common interface and shared logic for importing
    data into Django models from different formats (e.g. Excel, CSV, JSON).
    """

    check_dependencies: Optional[bool] = None
    name: Optional[str] = None
    fields: Optional[models.QuerySet] = None
    model: Optional[Type[models.Model]] = None
    data: Optional[Iterable[Any]] = None
    file_path: Optional[Path] = None

    base_import_folder: Path = (
        Path(settings.MEDIA_ROOT)
        if settings.MEDIA_ROOT
        else settings.BASE_DIR / "django_dataio_media"
    )
    import_folder: Path = base_import_folder / "django_dataio_imports"

    def __init__(
        self,
        name: str,
        model: Type[models.Model],
        fields: models.QuerySet,
        data: Optional[Iterable[Any]] = None,
    ) -> None:
        """
        Initialize importer.

        :param name: Importer name
        :param model: Target Django model
        :param fields: Fields queryset
        :param data: Optional iterable of input data rows
        """
        self.name = name
        self.model = model
        self.fields = fields
        self.fields_name_list: list[str] = list(
            self.fields.values_list('name', flat=True)
        )
        self.data = data

    def set_file(self, file_path: Path) -> None:
        """
        Set imports file path for importer.

        :param file_path: Path to file to imports
        """
        self.file_path = file_path

    @classmethod
    def _check_dependencies(cls) -> Optional[bool]:
        """
        Check importer dependencies.
        """
        return cls.check_dependencies

    @classmethod
    def is_active(cls, strict: bool = False) -> bool:
        """
        Check if importer is usable.

        :param strict: Raise error if dependencies are missing
        :return: True if active, otherwise False
        """
        if not cls._check_dependencies():
            if strict:
                raise ImportError(
                    f"Importer {cls.__name__} cant be used, dependencies not installed."
                )
            return False
        return True

    @abc.abstractmethod
    def _import_source(self) -> Path:
        """
        Return imports file path.

        Subclasses should use self.file_path if set.
        """
        raise NotImplementedError

    def _prepare_perform(self) -> None:
        """
        Prepare imports directories.
        """
        utils.create_folder(self.base_import_folder)
        utils.create_folder(self.import_folder)

    @abc.abstractmethod
    def _load(self) -> Iterable[dict[str, Any]]:
        """
        Load and parse raw data from source.

        :return: Iterable of row dictionaries
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _save(self, rows: Iterable[dict[str, Any]]) -> int:
        """
        Save imported data into database.

        :param rows: Parsed data rows
        :return: Number of created/updated objects
        """
        raise NotImplementedError

    @abc.abstractmethod
    def perform(self) -> int:
        """
        Run imports process.

        :return: Number of imported records
        """
        raise NotImplementedError
