import openpyxl
from parser import *

def worker(path_in, path_out):
    is_succeed = False # Флаг о статусе операции
    files = get_pdf_files(path_in)

    # Create a xlcx file
    workbook = openpyxl.Workbook()
    # Add a worksheet
    worksheet = workbook.active
    # Write data to a cell
    worksheet['A1'] = 'Изменение'
    worksheet['B1'] = 'Ссылка на файл'
    row = 2
    for file in files:
        last_number = get_last_number(file)
        number_of_doc = get_document_number(file)
        
        worksheet.cell(row=row, column=1, value=f"{last_number}")
        worksheet.cell(row=row, column=3, value=f"{file}")
        row += 1
        print(f"{last_number} - {number_of_doc} - {file}")
    # Save the workbook
    workbook.save(path_out)
    workbook.close()
    is_succeed = True
    return is_succeed
