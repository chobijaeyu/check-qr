import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog

from checkqr import checkqr


@pytest.fixture
def window(qtbot):
    """Pass the application to the test functions via a pytest fixture."""
    new_window = checkqr.checkqr()
    qtbot.add_widget(new_window)
    new_window.show()
    return new_window


def test_window_title(window):
    """Check that the window title shows as declared."""
    print(window)
    assert window.windowTitle() == 'checkqr'


def test_window_geometry(window):
    """Check that the window width and height are set as declared."""
    assert window.width() == 1800
    assert window.height() == 1024


def test_open_file(window, qtbot, mocker):
    """Test the Open File item of the File submenu.

    Qtbot clicks on the file sub menu and then navigates to the Open File item. Mock creates
    an object to be passed to the QFileDialog.
    """
    qtbot.mouseClick(window.file_sub_menu, Qt.LeftButton)
    qtbot.keyClick(window.file_sub_menu, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileName', return_value=('', ''))
    qtbot.keyClick(window.file_sub_menu, Qt.Key_Enter)


def test_about_dialog(window, qtbot, mocker):
    """Test the About item of the Help submenu.

    Qtbot clicks on the help sub menu and then navigates to the About item. Mock creates
    a QDialog object to be used for the test.
    """
    qtbot.mouseClick(window.help_sub_menu, Qt.LeftButton)
    qtbot.keyClick(window.help_sub_menu, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.help_sub_menu, Qt.Key_Enter)


def test_inputqr(window, qtbot, mocker):
    qtbot.keyClicks(window.inputqr, "abc", )
    qtbot.keyClick(window.inputqr, Qt.Key_Enter)
    assert window.outputqr.toPlainText() != ""
    
def test_resetbutton(window,qtbot,):
    qtbot.mouseClick(window.resetButton)
    assert window.outputqr.toPlainText() == ""
    qtbot.keyClicks(window.inputqr, "abc", )
    qtbot.keyClicks(window.inputqr,Qt.Key_Enter)
    assert window.outputqr.toPlainText() != ""
    qtbot.mouseClick(window.resetButton)
    assert window.outputqr.toPlainText() == ""

def test_nextbutton(window,qtbot):
    assert window.count == 1
    qtbot.keyClicks(window.inputqr, "abc", )
    qtbot.keyClick(window.inputqr,Qt.Key_Enter)
    assert window.count == 2
    qtbot.mouseClick(window.nextButton)
    assert window.count == 1

def test_offsetinput(window,qtbot):
    assert window.offset == 1
    qtbot.keyClicks(window.offsetinput,Qt.Key_5)
    qtbot.keyClick(window.offsetinput,Qt.Key_Enter)
    assert window.offset == 5

def test_countinput(window,qtbot):
    assert window.count == 1
    qtbot.keyClick(window.countinput,Qt.Key_5)
    qtbot.keyClick(window.countinput,Qt.Key_Enter)
    assert window.count == 5
