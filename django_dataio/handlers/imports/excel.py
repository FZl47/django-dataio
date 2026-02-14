try:
    import openpyxl

    check_dependencies = True
except ImportError:
    check_dependencies = False

from pathlib import Path
from typing import Iterable, Any, Optional

from .base import BaseImporter


class ExcelImporter(BaseImporter):
    """
    Importer for importing data from Excel (.xlsx) files into Django models
    using openpyxl library.
    """

    check_dependencies: bool = check_dependencies

    workbook = None
    workbook_page = None
    file_path: Optional[Path] = None

    def set_file(self, file_path: Path) -> None:
        """
        Set Excel file path for imports.

        :param file_path: Path to Excel file
        """
        self.file_path = file_path

    def _import_source(self) -> Path:
        """
        Return imports file path.
        """
        if not self.file_path:
            raise ValueError("No imports file provided. Use set_file() first.")
        return self.file_path

    def _prepare_perform(self) -> None:
        """
        Prepare workbook before importing.
        """
        super()._prepare_perform()
        self.workbook = openpyxl.load_workbook(self._import_source())
        self.workbook_page = self.workbook.active

    def _load(self) -> Iterable[dict[str, Any]]:
        """
        Load rows from Excel and convert them to dictionaries.

        :return: Iterable of row dictionaries
        """
        rows = self.workbook_page.iter_rows(values_only=True)
        header = next(rows)
        for row in rows:
            yield dict(zip(header, row))

    def _save(self, rows: Iterable[dict[str, Any]]) -> int:
        """
        Save imported rows into database.

        :param rows: Parsed row data
        :return: Number of created objects
        """
        count = 0
        for row in rows:
            data = {}

            for field in self.fields_name_list:
                if field in ('id',): # TODO: add fully field checker
                    continue
                field_value = row.get(field)
                data[field] = field_value

            self.model.objects.create(**data)
            count += 1
        return count

    def perform(self) -> int:
        """
        Run Excel imports process.

        :return: Number of imported records
        """
        self._prepare_perform()
        rows = self._load()
        return self._save(rows)
