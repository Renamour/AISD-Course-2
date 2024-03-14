import random

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import cipher
import ast


class SignUp(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_dialog = parent
        self.setWindowTitle("Sign up")
        self.setFixedSize(600, 400)
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 90))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Регистрация")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 100, 360, 35))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Имя пользователя")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 150, 360, 35))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Пароль")

        self.rpassInput = QtWidgets.QLineEdit(self)
        self.rpassInput.setGeometry(QtCore.QRect(120, 200, 360, 35))
        self.rpassInput.setObjectName("rpassInput")
        self.rpassInput.setPlaceholderText("Повторите пароль")

        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(200, 250, 200, 45))
        self.signupBtn.setText("Зарегистрироваться")

        self.backtologin = QtWidgets.QPushButton(self)
        self.backtologin.setGeometry(QtCore.QRect(200, 300, 200, 45))
        self.backtologin.setText("Я уже зарегистрирован")

        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        if self.loginInput.text() and self.passInput.text() and self.rpassInput.text():
            login = self.loginInput.text()
            password = self.passInput.text()
            rpassword = self.rpassInput.text()
            if password == rpassword:
                with open('login.txt', 'r+') as f:
                    data = f.read()
                accounts = []
                if data is not None:
                    rows = data.split('\n')
                    if len(rows) > 1:
                        if len(rows) != 0:
                            accounts = [x.split() for x in rows]
                if len(accounts) != 0:
                    find = False
                    for acc in accounts:
                        if len(acc) >= 2:
                            if acc[0] == login:
                                find = True
                    if find:
                        QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь с таким именем уже существует')
                    else:
                        with open('login.txt', 'a+') as f:
                            account_row = [login.replace(' ', ''), cipher.encrypt(password)]
                            f.write(str(account_row) + "\n")
                        self.close()
                else:
                    with open('login.txt', 'a+') as f:
                        account_row = [login.replace(' ', ''), cipher.encrypt(password)]
                        f.write(str(account_row) + "\n")
                    self.close()
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Введённые пароли не совпадают!')
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')

    def tologin(self):
        self.close()
        self.parent_dialog.show()

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)
        self.backtologin.clicked.connect(self.tologin)

    def closeEvent(self, event):
        self.tologin()


class CipherWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent_dialog = parent
        self.setWindowTitle("RSA Encryption")
        self.setFixedSize(600, 450)
        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 50))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Шифр RSA")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_to_cipher = QtWidgets.QLineEdit(self)
        self.text_to_cipher.setGeometry(QtCore.QRect(120, 70, 360, 35))
        self.text_to_cipher.setObjectName("text_to_cipher")
        self.text_to_cipher.setPlaceholderText("Текст для шифрования")

        self.text_to_cipher_key = QtWidgets.QLineEdit(self)
        self.text_to_cipher_key.setGeometry(QtCore.QRect(120, 120, 175, 35))
        self.text_to_cipher_key.setObjectName("text_to_cipher_key")
        self.text_to_cipher_key.setPlaceholderText("Ключ значение 1")
        self.text_to_cipher_key.setText(str(cipher.APP_RSA_PUBLIC_KEY[0]))

        self.text_to_cipher_key2 = QtWidgets.QLineEdit(self)
        self.text_to_cipher_key2.setGeometry(QtCore.QRect(305, 120, 175, 35))
        self.text_to_cipher_key2.setObjectName("text_to_cipher_key2")
        self.text_to_cipher_key2.setPlaceholderText("Ключ значение 2")
        self.text_to_cipher_key2.setText(str(cipher.APP_RSA_PUBLIC_KEY[1]))

        self.cipher_btn = QtWidgets.QPushButton(self)
        self.cipher_btn.setGeometry(QtCore.QRect(200, 170, 200, 45))
        self.cipher_btn.setText("Зашифровать")

        self.key_to_decipher = QtWidgets.QLineEdit(self)
        self.key_to_decipher.setGeometry(QtCore.QRect(120, 230, 175, 35))
        self.key_to_decipher.setObjectName("key_to_decipher")
        self.key_to_decipher.setPlaceholderText("Ключ значение 1")
        self.key_to_decipher.setText(str(cipher.APP_RSA_PRIVATE_KEY[0]))

        self.key_to_decipher2 = QtWidgets.QLineEdit(self)
        self.key_to_decipher2.setGeometry(QtCore.QRect(305, 230, 175, 35))
        self.key_to_decipher2.setObjectName("key_to_decipher2")
        self.key_to_decipher2.setPlaceholderText("Ключ значение 2")
        self.key_to_decipher2.setText(str(cipher.APP_RSA_PRIVATE_KEY[1]))

        self.decipher_btn = QtWidgets.QPushButton(self)
        self.decipher_btn.setGeometry(QtCore.QRect(200, 330, 200, 45))
        self.decipher_btn.setText("Расшифровать")

        self.newKeyPair_btn = QtWidgets.QPushButton(self)
        self.newKeyPair_btn.setGeometry(QtCore.QRect(200, 380, 200, 45))
        self.newKeyPair_btn.setText("Создать новую ключ пару")

        self.decipher_res = QtWidgets.QLineEdit(self)
        self.decipher_res.setGeometry(QtCore.QRect(120, 280, 360, 35))
        self.decipher_res.setObjectName("decipher_res")
        self.decipher_res.setPlaceholderText("Результат расшифровки")

        self.registerBtns()

    @QtCore.pyqtSlot()
    def cipherText(self):
        try:
            if self.text_to_cipher_key.text() and self.text_to_cipher.text():
                cipher_text = "".join([chr(x) for x in cipher.encrypt(self.text_to_cipher.text(), (self.text_to_cipher_key.text(), self.text_to_cipher_key2.text()))])
                with open('cipher_text.txt', 'wb') as f:
                    f.write(cipher_text.encode())
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')
        except:
            QtWidgets.QMessageBox.information(self, 'Ошибка!', 'Недопустимый ключ!')

    @QtCore.pyqtSlot()
    def decipherText(self):
        if self.key_to_decipher.text() and self.key_to_decipher2.text():
            data = ''
            with open('cipher_text.txt', 'rb') as f:
                data = f.read().decode()
            self.decipher_res.setText(cipher.decrypt(data, (self.key_to_decipher.text(), self.key_to_decipher2.text())))
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не указали ключ для расшифровки!')

    def tologin(self):
        self.close()
        self.parent_dialog.show()

    def newKeyPair(self):
        public, private = cipher.generate_keypair(random.randint(1, 1000), random.randint(1, 1000), 16)
        self.text_to_cipher_key.setText(str(public[0]))
        self.text_to_cipher_key2.setText(str(public[1]))

        self.key_to_decipher.setText(str(private[0]))
        self.key_to_decipher2.setText(str(private[1]))

    def registerBtns(self):
        self.cipher_btn.clicked.connect(self.cipherText)
        self.decipher_btn.clicked.connect(self.decipherText)
        self.newKeyPair_btn.clicked.connect(self.newKeyPair)

    def closeEvent(self, event):
        self.tologin()


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log in")
        self.setFixedSize(600, 350)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.def_font = QtGui.QFont()
        self.def_font.setFamily("Tahoma")
        self.def_font.setPixelSize(25)
        self.def_font.setBold(True)
        self.def_font.setItalic(False)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 600, 90))
        self.label.setFont(self.def_font)
        self.label.setObjectName("label")
        self.label.setText("Авторизация")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.loginInput = QtWidgets.QLineEdit(self)
        self.loginInput.setGeometry(QtCore.QRect(120, 100, 360, 35))
        self.loginInput.setObjectName("loginInput")
        self.loginInput.setPlaceholderText("Имя пользователя")

        self.passInput = QtWidgets.QLineEdit(self)
        self.passInput.setGeometry(QtCore.QRect(120, 150, 360, 35))
        self.passInput.setObjectName("passInput")
        self.passInput.setPlaceholderText("Пароль")

        self.loginBtn = QtWidgets.QPushButton(self)
        self.loginBtn.setGeometry(QtCore.QRect(200, 200, 200, 45))
        self.loginBtn.setText("Войти")

        self.signupBtn = QtWidgets.QPushButton(self)
        self.signupBtn.setGeometry(QtCore.QRect(200, 250, 200, 45))
        self.signupBtn.setText("У меня нет учетной записи")

        self.registerBtns()

    @QtCore.pyqtSlot()
    def registerBtnHandler(self):
        self.hide()
        self.sign_up_wind = SignUp(self)
        self.sign_up_wind.show()

    @QtCore.pyqtSlot()
    def loginBtnHandler(self):
        login = self.loginInput.text()
        password = self.passInput.text()
        if not login or not password:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля!')
            return
        with open('login.txt', 'r') as f:
            data = f.read()
        if data is not None:
            rows = data.split('\n')
            accounts = []
            for k in rows:
                if len(k) > 0:
                    accounts.append(ast.literal_eval(k))
            account_data = None
            for k in accounts:
                if len(k) == 2:
                    if k[0] == login.replace(' ', ''):
                        account_data = k
                        break
            if account_data is not None:
                if account_data[1] == cipher.encrypt(password, cipher.APP_RSA_PUBLIC_KEY):
                    self.close()
                    self.hide()
                    self.cipher_wind = CipherWindow(self)
                    self.cipher_wind.show()
                else:
                    QtWidgets.QMessageBox.information(self, 'Внимание!', 'Неверный пароль')
            else:
                QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')
        else:
            QtWidgets.QMessageBox.information(self, 'Внимание!', 'Пользователь не найден')

    def registerBtns(self):
        self.signupBtn.clicked.connect(self.registerBtnHandler)
        self.loginBtn.clicked.connect(self.loginBtnHandler)