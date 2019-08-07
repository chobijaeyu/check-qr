import sys

import pkg_resources

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QHBoxLayout, QLabel, QMainWindow, QToolBar, QVBoxLayout, QWidget,
                             QLineEdit, QPushButton, QMessageBox, QTableWidget, QHBoxLayout,
                             QTabWidget, QSizePolicy, QTextEdit, QGridLayout,QTableView)
from PyQt5.QtSql import QSqlDatabase,QSqlTableModel

import pandas as pd
import sqlite3,csv
from os.path import exists

class checkqr(QMainWindow):
    """Create the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super(checkqr, self).__init__(parent)
        self.resize(1024, 768)
        self.setWindowTitle('checkqr')
        # window_icon = pkg_resources.resource_filename('checkqr.images',
        # 'ic_insert_drive_file_black_48dp_1x.png')
        # self.setWindowIcon(QIcon(window_icon))
        
        widget = QWidget(self)
        # self.layout = QHBoxLayout(widget)
        self.open_file()
        self.menu_bar = self.menuBar()
        self.about_dialog = AboutDialog()
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)
        
        self.file_menu()
        self.help_menu()
        
        # self.tool_bar_items()
        self.input_area()
        self.table_area()


        self.setCentralWidget(widget)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.textbox, 1, 0)
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
            print(fieldsName)
            with open(filename) as f ,sqlite3.connect('tmp.db') as dbcon:
                reader = csv.reader(f)
                self.c = dbcon.cursor()
                self.c.execute(f"""CREATE TABLE IF NOT EXISTS checkdata({fieldsName})""")
                for idx,field in enumerate(reader):
                    if idx == 0:
                        continue
                    self.c.execute('insert into checkdata values (?,?)' , field)
                dbcon.commit()

    def input_area(self):
        self.textbox=QLineEdit(self)
        # self.textbox.move(30,30)
        self.textbox.resize(280,40)
        # self.button=QPushButton('Click me',self)
        # self.button.move(15,85)
        # self.button.clicked.connect(self.on_click)
    
    # @pyqtSlot()
    # def on_click(self):
    #         textboxValue=self.textbox.text()
    #         QMessageBox.question(self, 'Hello, world!', "Confirm: "+textboxValue,                                                                            QMessageBox.Ok, QMessageBox.Ok)
    #         self.textbox.setText("")

    def table_area(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)
        # self.bottomLeftTabWidget.move(30,90)
        if not exists("tmp.db"):
            print("File tmp.db does not exist.")
            sys.exit()

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("tmp.db")
        db.open()
        model = QSqlTableModel(None, db)
        model.setTable("checkdata")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        view = QTableView()
        view.setModel(model)

        self.bottomLeftTabWidget.addTab(view,"table")
        

        # tab1 = QWidget()
        # tableWidget = QTableWidget(self.data.shape[0] if self.data.empty else 1, self.data.shape[1] if self.data.empty else 1)
        # tableWidget = QTableWidget(self.data.shape[0] , self.data.shape[1] )

        # tab1hbox = QHBoxLayout()
        # tab1hbox.setContentsMargins(5, 5, 5, 5)
        # tab1hbox.addWidget(tableWidget)
        # tab1.setLayout(tab1hbox)

        # tab2 = QWidget()
        # textEdit = QTextEdit()

        # textEdit.setPlainText("Twinkle, twinkle, little star,\n"
        #                       "How I wonder what you are.\n" 
        #                       "Up above the world so high,\n"
        #                       "Like a diamond in the sky.\n"
        #                       "Twinkle, twinkle, little star,\n" 
        #                       "How I wonder what you are!\n")

        # tab2hbox = QHBoxLayout()
        # tab2hbox.setContentsMargins(5, 5, 5, 5)
        # tab2hbox.addWidget(textEdit)
        # tab2.setLayout(tab2hbox)

        # self.bottomLeftTabWidget.addTab(tab1, "&Table")
        # self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

class AboutDialog(QDialog):
    """Create the necessary elements to show helpful text in a dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')

        self.resize(300, 200)

        author = QLabel('yujun')
        author.setAlignment(Qt.AlignCenter)

        icons = QLabel('Material design icons created by Google')
        icons.setAlignment(Qt.AlignCenter)

        github = QLabel('GitHub: chobijaeyu')
        github.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(author)
        self.layout.addWidget(icons)
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