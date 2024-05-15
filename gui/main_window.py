import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QFileDialog, QMessageBox, QLabel, QLineEdit)
from gui.logger_window import LogWindow
from output_producer import WorkerThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AutoReest')
        self.setGeometry(100, 100, 400, 400) 
        self.path_in = None
        self.path_out = None

        self.path_out_label = QLabel('Директория сохранения файла:', self)
        self.path_out_label.setGeometry(50, 50, 200, 20)

        self.path_out_field = QLineEdit(self)
        self.path_out_field.setGeometry(50, 80, 300, 30)
        self.path_out_field.setReadOnly(True)  # Поле только для чтения

        self.select_folder_button = QPushButton('Выберите директорию сохранения xlcx файла', self)
        self.select_folder_button.setGeometry(50, 120, 300, 30)
        self.select_folder_button.clicked.connect(self.select_output_dir)

        self.path_in_label = QLabel('Директория с документами:', self)
        self.path_in_label.setGeometry(50, 170, 200, 20)

        self.path_in_field = QLineEdit(self)
        self.path_in_field.setGeometry(50, 200, 300, 30)
        self.path_in_field.setReadOnly(True)  # Поле только для чтения

        self.select_output_button = QPushButton('Выберите папку с документами', self)
        self.select_output_button.setGeometry(50, 240, 300, 30)
        self.select_output_button.clicked.connect(self.select_folder)


        self.open_guide_button = QPushButton('Открыть гайд', self)
        self.open_guide_button.setGeometry(50, 300, 100, 30)
        self.open_guide_button.clicked.connect(self.open_guide)


        self.process_button = QPushButton('Далее', self)
        self.process_button.setStyleSheet("background-color: green; color: white; border-radius: 10px;")
        self.process_button.setGeometry(250, 300, 100, 30)
        self.process_button.clicked.connect(self.process)

        self.log_window = None


    def select_output_dir(self):
        options = QFileDialog.Options()
        self.path_out, _ = QFileDialog.getSaveFileName(self, "Выберите место сохранения файла", filter="Excel files (*.xlsx)", options=options)
        self.path_out_field.setText(self.path_out)
    
    
    def select_folder(self):
        options = QFileDialog.Options()
        self.path_in = QFileDialog.getExistingDirectory(self, "Выберите папку с PDF", options=options)
        self.path_in_field.setText(self.path_in)

    def process(self):
        if self.path_out == None:
            QMessageBox.warning(self, "Предупреждение", "Выберите директорию сохранения.")
            return 
        if self.path_in == None:
            QMessageBox.warning(self, "Предупреждение", "Выберите папку с файлами.")
            return   
        res = QMessageBox.question(self, "AutoReest", f"Выбрана папка: {self.path_in} \nИдем дальше?")
        if res == QMessageBox.Yes:
            if self.log_window is None or not self.log_window.isVisible():  
                self.log_window = LogWindow()  
                self.log_window.show()  

            self.worker_thread = WorkerThread(self.path_in, self.path_out)
            self.worker_thread.progress_updated.connect(self.log_window.update_progress)
            self.worker_thread.log_updated.connect(self.log_window.update_log)
            self.worker_thread.start()

    def open_guide(self):
        guide_text = (
            "Гайд по использованию приложения:\n"
            "1. Шаг 1: Нажмите кнопку 'Выберите директорию сохранения xlcx файла' для выбора места сохранения.\n"
            "2. Шаг 2: Нажмите кнопку 'Выберите папку с документами' для выбора папки с документами.\n"
            "3. Шаг 3: Нажмите кнопку 'Далее' для запуска обработки.\n"
        )
        QMessageBox.information(self, "Гайд по использованию приложения", guide_text)