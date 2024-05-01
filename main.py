from gui.main_window import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pdf_app = MainWindow()
    pdf_app.show()
    sys.exit(app.exec_())
