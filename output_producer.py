import sys
from PyQt5.QtCore import QThread, pyqtSignal
import openpyxl
from parser import *

class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)

    def __init__(self, path_in, path_out):
        super().__init__()
        self.path_in = path_in
        self.path_out = path_out

    def run(self):
        files = get_pdf_files(self.path_in)
        total_files = len(files)
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.column_dimensions['A'].width = 40
        worksheet.column_dimensions['B'].width = 30
        cell_a1 = worksheet['A1']
        cell_a1.value = "Номер последнего изменения документа"
        cell_b1 = worksheet['B1']
        cell_b1.value = "Обозначение документа"
        header = openpyxl.styles.Font(color="FF0000")
        hyperlink = openpyxl.styles.Font(underline='single', color='0563C1')
        cell_a1.font = header
        cell_b1.font = header
        row = 2
        for idx, file in enumerate(files, start=1):
            last_number = get_last_number(file)
            link = file
            doc_num = get_document_number(file)
            cell_ai = worksheet.cell(row=row, column=1)
            cell_bi = worksheet.cell(row=row, column=2)
            try:
                cell_ai.value = f"{last_number}"
                cell_bi.value = '=HYPERLINK("{}", "{}")'.format(link, f"{doc_num}")
                cell_bi.font = hyperlink
                row += 1
            except openpyxl.utils.exceptions.IllegalCharacterError as illegalCharacterError:
                cell_ai.value = f"{last_number}"
                cell_bi.value = '=HYPERLINK("{}", "{}")'.format(link, "Invalid text")
                cell_bi.font = hyperlink
                row += 1
            progress_percentage = idx * 100 // total_files
            self.progress_updated.emit(progress_percentage)
            self.log_updated.emit(f"Обработано файлов: {idx}/{total_files}: {last_number} - {doc_num} - {file}")
        workbook.save(self.path_out)
        workbook.close()