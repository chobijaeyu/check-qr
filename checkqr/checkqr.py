import sys

import pkg_resources

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget,
                             QLineEdit, QPlainTextEdit,
                             QTabWidget, QSizePolicy, QGridLayout, QTableView, QGroupBox, QPushButton)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

import pandas as pd
import sqlite3
import csv
from os.path import exists


class checkqr(QMainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        self.count = 1
        self.offset = 1
        super(checkqr, self).__init__(parent)
        self.resize(1800, 1024)
        self.setWindowTitle('checkqr')
        # window_icon = pkg_resources.resource_filename('checkqr.images',
        # 'ic_insert_drive_file_black_48dp_1x.png')
        # self.setWindowIcon(QIcon(window_icon))

        widget = QWidget(self)
        # self.layout = QHBoxLayout(widget)
        # self.open_file()
        self.menu_bar = self.menuBar()
        self.about_dialog = AboutDialog()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)

        self.file_menu()
        self.help_menu()

        # self.tool_bar_items()
        self.input_area()
        self.table_area()
        self.tool_area()
        self.output_area()

        self.setCentralWidget(widget)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.inputqr, 1, 0)
        mainLayout.addWidget(self.outputqr, 2, 1)
        widget.setLayout(mainLayout)

    def file_menu(self):
        """Create a file submenu with an Open File item that opens a file dialog."""
        self.file_sub_menu = self.menu_bar.addMenu('&File')

        self.open_action = QAction(' &Open File', self)
        self.open_action.setStatusTip('Open a file into checkqr.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.exit_action = QAction(' &Exit Application', self)
        self.exit_action.setStatusTip('Exit the application.')
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(lambda: QApplication.quit())

        self.file_sub_menu.addAction(self.open_action)
        self.file_sub_menu.addAction(self.exit_action)

    def help_menu(self):
        """Create a help submenu with an About item tha opens an about dialog."""
        self.help_sub_menu = self.menu_bar.addMenu('Help')

        self.about_action = QAction('About', self)
        self.about_action.setStatusTip('About the application.')
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(lambda: self.about_dialog.exec_())

        self.help_sub_menu.addAction(self.about_action)

    def tool_bar_items(self):
        """Create a tool bar for the main window."""
        self.tool_bar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        self.tool_bar.setMovable(False)

        tool_bar_open_action = QAction('Open File', self)
        tool_bar_open_action.triggered.connect(self.open_file)

        self.tool_bar.addAction(tool_bar_open_action)

    def open_file(self):
        """Open a QFileDialog to allow the user to open a file into the application."""
        filename, accepted = QFileDialog.getOpenFileName(self, 'Open File')

        if accepted:
            # with open(filename) as file:
            #     file.read()
            self.data = pd.read_csv(filename)
            fieldsName = ''
            for i in list(self.data):
                fieldsName += f'{i} varchar,'
            fieldsName = fieldsName[:-1]
            with open(filename) as f, sqlite3.connect('tmp.db') as dbcon:
                reader = csv.reader(f)
                c = dbcon.cursor()
                c.execute(
                    f"""CREATE TABLE IF NOT EXISTS checkdata({fieldsName})""")
                for idx, field in enumerate(reader):
                    if idx == 0:
                        _columns = len(field) - 1
                        continue
                    c.execute(
                        f'insert into checkdata values ({"?," * _columns}?)', field)
                dbcon.commit()
        self.load_table()

    def input_area(self):
        self.inputqr = QLineEdit(self)
        # self.textbox.move(30,30)
        self.inputqr.resize(280, 40)
        self.inputqr.returnPressed.connect(self.on_input)
        # self.button=QPushButton('Click me',self)
        # self.button.move(15,85)
        # self.button.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_input(self):
        textboxValue = self.inputqr.text()
        print(textboxValue)
        self.outputqr.appendPlainText(
            f"{self.count}番目-sacned-->{textboxValue}")
        self.inputqr.setText("")
        self.on_check(textboxValue)

    def on_check(self, checktext):
        with sqlite3.connect('tmp.db') as dbcon:
            c = dbcon.cursor()
            c.execute("select * from checkdata where rowid= ?",
                      (str(self.count),))
            dbcon.commit()
        res = c.fetchone()
        print(res)
        if res[-1] == checktext:
            self.outputqr.appendPlainText(f"{self.count}番目-checked-->{res}")
            self.count += self.offset
        else:
            self.outputqr.appendPlainText(f"{self.count}番目-not found-->{res}")

    def table_area(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.view = QTableView()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)
        # if not exists("tmp.db"):
        #     print("File tmp.db does not exist.")
        self.load_table()

    def load_table(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("tmp.db")
        db.open()
        model = QSqlTableModel(None, db)
        model.setTable("checkdata")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        self.view.setModel(model)
        self.bottomLeftTabWidget.addTab(self.view, "table")

    def output_area(self):
        self.outputqr = QPlainTextEdit()
        self.outputqr.setFocusPolicy(Qt.NoFocus)

    def tool_area(self):
        self.topRightGroupBox = QGroupBox("tool area")
        self.offsetlabel = QLabel(
            f"offset setting, now offset is {self.offset}")
        self.countlabel = QLabel(f"setting your count,now is {self.count}")
        onlyInt = QIntValidator()
        self.countinput = QLineEdit(self)
        self.countinput.setValidator(onlyInt)
        self.countinput.returnPressed.connect(lambda: self.set_count(self.countinput.text()))
        self.nextButton = QPushButton('next', self)
        self.nextButton.clicked.connect(self.on_click_nextbutton)
        self.resetButton = QPushButton('reset', self)
        self.resetButton.clicked.connect(self.reset)
        self.offsetinput = QLineEdit(self)
        self.offsetinput.setValidator(onlyInt)
        self.offsetinput.returnPressed.connect(
            lambda: self.on_offsetinput(self.offsetinput.text()))
        layout = QVBoxLayout()
        layout.addWidget(self.nextButton)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.offsetlabel)
        layout.addWidget(self.offsetinput)
        layout.addWidget(self.countlabel)
        layout.addWidget(self.countinput)

        self.topRightGroupBox.setLayout(layout)

    @pyqtSlot()
    def on_offsetinput(self, offset):
        self.offset = int(offset)
        self.offsetlabel.setText(
            f"offset setting, now offset is {self.offset}")

    @pyqtSlot()
    def on_click_nextbutton(self):
        self.read_next()

    def read_next(self):
        self.count += self.offset

    def set_count(self, count):
        self.count = int(count)
        self.countlabel.setText(f"setting where count from,now is from {self.count}")

    def reset(self):
        self.count = 1
        self.offset = 1
        self.outputqr.setPlainText('')
        self.offsetlabel.setText(
            f"offset setting, now offset is {self.offset}")


class AboutDialog(QDialog):
    """Create the necessary elements to show helpful text in a dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')

        self.resize(300, 200)

        author = QLabel('yujun')
        author.setAlignment(Qt.AlignCenter)

        github = QLabel('GitHub: chobijaeyu')
        github.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(author)
        self.layout.addWidget(github)

        self.setLayout(self.layout)


def main():
    application = QApplication(sys.argv)
    window = checkqr()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
