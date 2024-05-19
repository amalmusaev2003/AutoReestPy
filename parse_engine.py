import os
import pdfplumber
import re


def extractor(path, object):
  tables = []
  with pdfplumber.open(path) as file:
    # Достаем все таблицы с 1 по 5 странииы 
    if object == 't':
        for i, v in enumerate(file.pages):
          if i == 5:
            break
          tables.append(v.extract_table())
        return tables
    # Достаем текст первой страницы документа
    elif object == 'd':
       text = file.pages[0].extract_text_simple()
       return text


#Достаем все файлы с расширением .pdf из папки
def get_pdf_files(folder_path):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
      for filename in files:
        if filename.lower().endswith(".pdf"):
          pdf_files.append(os.path.join(root, filename))
    return pdf_files

#Фильтруем все таблицы с помощью регулярных выражений
def filter_tables(table) -> list:
    pattern = re.compile(r"(\d+)\s+(\d+-\d+(?:-\d+)?)\s+\d{2}.\d{2}.\d{2,4}|\d+\s+\d{2}.\d{2}")  # шаблон для поиска: любое количество цифр
    filtered_tables = []
    str_table = ' '.join(table)

    if pattern.match(str_table):
      filtered_tables.append(table)
    return filtered_tables

#Метод который достает последний номер изменений документа
def get_last_number(file) -> tuple:
  last_number = 0
  try:
    tables = extractor(file, 't')
    filtered_tables = []
    for i in range(len(tables)):
      if tables[i] == None:
        continue
      #print(tables[i]) debug 
      for item in tables[i]:
        chunk = [el for el in item if el is not None]
        if len(filter_tables(chunk)) != 0:
          filtered_tables.append(filter_tables(chunk)[0])
    
    if filtered_tables:
        numbers = []
        for item in filtered_tables:
            try:
                number = int(item[0])
                numbers.append(number)
            except ValueError:
                return -2 # -2 значит, что номер файла считался с ошибкой
        if numbers:
            last_number = max(numbers)
        else:
            last_number = 0
    else:
        last_number = 0

  except(AssertionError):
    return -1       # -1 значит, что файл не считался "AssertionError"

  return last_number


def filter_text(path, text):
  pattern = re.compile(r"\d+-\d+\/\d+-\d+-\d+-?\s?\S+")
  split_symbols = "\n"
  chunks = re.split(split_symbols, text)
  for e in chunks:
    if re.match(pattern, e):
      return e
    else:
      return os.path.splitext(os.path.basename(path))[0] #Возвращаем название файла в качестве обознаения документа
       

def get_document_number(file):
  try:
      text = extractor(file, 'd')
      return filter_text(file, text)
  except(AssertionError):
     return -1  # -1 значит, что файл не считался "AssertionError"
  
'''
# test
res = get_last_number("E:/CodeProjects/task/autoreest ошибки/Крашат программу/ONPZ-OFS-PD-6004-IOS7_1_1-r3-087.pdf")
print(res)
'''
