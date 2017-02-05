
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWIndow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        self.setWindowTitle("종목 코드")
        self.setGeometry(300, 300, 300, 300)

        btn1 = QPushButton("종목코드 얻기", self)
        btn1.move(190, 10)
        btn1.clicked.connect(self.btn1_clicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 170, 130)

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for code in kospi_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [code])
            kospi_code_name_list.append("%s: %s" % (code, name))

        self.listWidget.addItems(kospi_code_name_list)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWIndow()
    myWindow.show()
    sys.exit(app.exec_())




