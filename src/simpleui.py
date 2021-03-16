from PySide2 import QtWidgets


class SimpleUI(QtWidgets.QDialog):
    """This is my SimpleUI class to create graphical user interface"""
    def __init__(self):
        """Constructor"""
        # Passing the object SimpleUI as an argument to super()
        # makes this line python 2 and 3 compatible
        super(SimpleUI, self).__init__()
        self.setWindowTitle("A Simple UI")
