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

@pytest.fixture
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
    qtbot.mouseClick(window.file_s768ub_menu, Qt.LeftButton)
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

if __name__ == "__main__":
    test_window_title(window())