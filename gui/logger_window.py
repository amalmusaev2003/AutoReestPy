from PyQt5.QtWidgets import QMainWindow, QTextEdit, QProgressBar

class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Логгер')
        self.setGeometry(400, 200, 1000, 300) 

        self.log_textedit = QTextEdit(self)
        self.log_textedit.setReadOnly(True)
        self.log_textedit.setMaximumHeight(250)
        self.setCentralWidget(self.log_textedit)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 260, 380, 30)
        self.progress_bar.setValue(0)

    def update_log(self, message):
        self.log_textedit.append(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)