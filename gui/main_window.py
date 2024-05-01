import sys
from output_producer import worker
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path_in = ""
        self.path_out = ""
        self.setWindowTitle("AutoReest")
        self.setGeometry(100, 100, 400, 300)

        # Кнопка для выбора папки с PDF-файлами
        self.select_folder_button = QPushButton("Выбрать папку с PDF", self)
        self.select_folder_button.setGeometry(50, 50, 300, 30)
        self.select_folder_button.clicked.connect(self.select_folder)

        # Кнопка для открытия окна с гайдом
        self.open_guide_button = QPushButton("Открыть гайд", self)
        self.open_guide_button.setGeometry(50, 100, 300, 30)
        self.open_guide_button.clicked.connect(self.open_guide)

        # Кнопка для добавления директории сохранения
        self.add_output_dir_button = QPushButton("Добавить директорию сохранения", self)
        self.add_output_dir_button.setGeometry(50, 150, 300, 30)
        self.add_output_dir_button.clicked.connect(self.add_output_dir)

    def select_folder(self):
        options = QFileDialog.Options()
        self.path_in = QFileDialog.getExistingDirectory(self, "Выберите папку с PDF", options=options)
        
        if self.path_in:
            self.process_files()
                
         
    def process_files(self):
        res = QMessageBox.question(self, "AutoReest", f"Выбрана папка: {self.path_in} \n Идем дальше?")
        if res == QMessageBox.Yes:
            if self.path_out == "":
                QMessageBox.warning(self, "Предупреждение", "Выберите директорию сохранения.")
                return  
            is_succeed = worker(self.path_in, self.path_out)
            if is_succeed:
                QMessageBox.information(self, "Готово!", "Ваш xlsx файл готов. Вы можете либо закрыть программу, либо продолжить работу")


    def open_guide(self):
        pass

    def add_output_dir(self):
        options = QFileDialog.Options()
        self.path_out, _ = QFileDialog.getSaveFileName(self, "Выберите место сохранения файла", filter="Excel files (*.xlsx)", options=options)

