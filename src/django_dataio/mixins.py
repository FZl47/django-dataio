from typing import Any, List, Union
from pathlib import Path

from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.utils import timezone

from .models import ModelField
from .handlers.exports import get_exporter
from .handlers.imports import get_importer

ExportTypes: List[str] = [
    'excel',
]

ImportTypes: List[str] = [
    'excel',
]


class DjangoDataIOModelMixin:
    """
    Mixin for exporting and importing model data based on ModelField configuration.

    Provides simple methods to get a timestamped table name,
    exports data using a registered exporter, and a placeholder for imports.
    """

    @classmethod
    def data_table_name(cls) -> str:
        """
        Returns a table name based on the model class and current date.
        """
        t = timezone.now().strftime('%Y-%m-%d')
        return f'{cls.__name__}({t})'

    @classmethod
    def data_export_model_fields(cls) -> QuerySet[ModelField]:
        """
        Returns all ModelField objects registered for this model.
        """
        model_content_type = ContentType.objects.get_for_model(cls)
        return ModelField.objects.filter(model=model_content_type).select_related('model').order_by(
            'xp')  # Order by X position

    @classmethod
    def data_export(cls, export_name: str) -> Path:
        """
        Exports the model data using the specified exporter.

        Args:
            export_name (str): Type of exporter (must be in ExportTypes).

        Returns:
            str: Path to the exported file.
        """
        if export_name not in ExportTypes:
            raise ValueError(f"Unsupported exports type: {export_name}")

        fields = cls.data_export_model_fields()
        if not fields.exists():
            raise ValueError("No ModelFields defined for this model.")

        exporter_cls = get_exporter(export_name)
        if not exporter_cls:
            raise ValueError(f"No exporter registered for type: {export_name}")

        exporter = exporter_cls(cls.data_table_name(), cls, fields)
        path = exporter.perform()
        return path

    @classmethod
    def data_import(cls, file: Union[Path, Any], import_name: str) -> int:
        """
        Imports data into the model from a file using the specified importer.

        Args:
            file (Union[Path, Any]): Path or file-like object to imports.
            import_name (str): Type of importer (must be in ImportTypes).

        Returns:
            int: Number of imported records.

        Raises:
            ValueError: If no fields are defined or unsupported imports type.
        """
        if import_name not in ImportTypes:
            raise ValueError(f"Unsupported imports type: {import_name}")

        fields = cls.data_export_model_fields()
        if not fields.exists():
            raise ValueError("No ModelFields defined for this model.")

        importer_cls = get_importer(import_name)
        if not importer_cls:
            raise ValueError(f"No importer registered for type: {import_name}")

        importer = importer_cls(cls.__name__, cls, fields)
        # Set the file
        if isinstance(file, Path):
            importer.set_file(file)
        else:
            # TODO: handle file-like objects (e.g., InMemoryUploadedFile)
            raise NotImplementedError("File-like objects not implemented yet.")

        count = importer.perform()
        return count
