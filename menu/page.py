from PyQt6.QtWidgets import QWidget


class Page(QWidget):
    def __init__(self, changePage):
        super().__init__()
        self.changePage = changePage
