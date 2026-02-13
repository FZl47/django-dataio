try:
    import openpyxl

    check_dependencies = True
except ImportError:
    check_dependencies = False

from pathlib import Path
from typing import Optional

from django_dataio import utils

from .base import BaseExporter


class ExcelExporter(BaseExporter):
    """
    Exporter for exporting Django model data into Excel (.xlsx) format
    using openpyxl library.
    """

    check_dependencies: bool = check_dependencies

    workbook: Optional["openpyxl.Workbook"] = None
    workbook_page: Optional["openpyxl.worksheet.worksheet.Worksheet"] = None

    def _export_location(self) -> Path:
        """
        Generate exports file path.

        :return: Path to .xlsx file
        """
        export_name = f"{utils.time_now('%Y-%m-%d')}__{utils.random_string(5)}.xlsx"
        return Path(f"{self.export_folder}/{export_name}")

    def _prepare_perform(self) -> None:
        """
        Prepare workbook and worksheet before exporting.
        """
        super()._prepare_perform()
        self.workbook = openpyxl.Workbook()
        self.workbook_page = self.workbook.active
        self.workbook_page.title = self.name

    def _save(self) -> Path:
        """
        Save Excel file to disk.

        :return: Path of saved file
        """
        path = self._export_location()
        self.workbook.save(path)
        return path

    def perform(self) -> Path:
        """
        Execute Excel exports process.

        Writes header row from fields and then model data rows.

        :return: Path of exported Excel file
        """
        self._prepare_perform()

        # Set header
        self.workbook_page.append(self.fields_name_list)

        # Set data
        for obj in self.queryset:
            rows_list: list[str] = []

            for field in self.fields:
                field_value = getattr(obj, field.name, None)
                if not field_value:
                    # TODO: add log
                    continue
                rows_list.append(str(field_value))

            self.workbook_page.append(rows_list)

        return self._save()
