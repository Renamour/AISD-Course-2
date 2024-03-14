import sys
from dialogs import Login
from PyQt5.QtWidgets import QApplication
import cipher

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())