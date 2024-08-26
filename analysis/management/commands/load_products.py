from typing import Any
from django.core.management.base import BaseCommand
from analysis.logic import UploadCleanDataSet
import os

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = base_dir + "/generated_products_dataset.csv"
            UploadCleanDataSet().processDataSetToDatabase(path=file_path)
        except Exception as e:
            raise Exception(e)