import sys
from PyQt5 import QtWidgets as qtw
from gui_part.stylesheet import style_sheet
from gui_part.nica_ui import NICA_UI


def main():
    '''
    Main function of NICApy
    Creates the application and opens NICA_UI
    '''
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    nica_ui = NICA_UI()
    nica_ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()