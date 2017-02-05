import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import time

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.OnEventConnect.connect(self.on_event_connect)
        self.OnEventConnect.connect(self.OnReceiveTrData)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_loop = QEventLoop()
        self.login_loop.exec_()

    def on_event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("not connected")
        self.login_loop.exit()

    def SetInputValue(self, sID, sValue):
        self.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def CommRqData(self, sRQName, sTRCode, nPrevNext, sScreenNo):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", sRQName, sTRCode, nPrevNext, sScreenNo)

        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def CommGetData(self, sJongmokCode, sRealType, sFieldName, nIndex, sInnerFiledName):
        data = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", sJongmokCode, sRealType,
                                sFieldName, nIndex, sInnerFiledName)
        return data.strip()

    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg):
        self.prev_next = PrevNext

        if RQName == "opt10081_req":
            cnt = self.GetRepeatCnt(TrCode, RQName)

            for i in range(cnt):
                date = self.CommGetData(TrCode, "", RQName, i, "일자")
                open = self.CommGetData(TrCode, "", RQName, i, "시가")
                high = self.CommGetData(TrCode, "", RQName, i, "고가")
                low  = self.CommGetData(TrCode, "", RQName, i, "저가")
                end  = self.CommGetData(TrCode, "", RQName, i, "현재가")
                print(date, ":", open, ' ', high, ' ', low, ' ', end)

        self.tr_event_loop.exit()

    def GetRepeatCnt(self, sTrCode, sRecordName):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRecordName)
        return ret

    def get_codelist_by_market(self, market):
        func = 'GetCodeListByMarket("%s")' % market
        codes = self.dynamicCall(func)
        return codes.split(';')

    def get_master_code_name(self, code):
        func = 'GetMasterCodeName("%s")' % code
        name = self.dynamicCall(func)
        return name


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Test Code
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    # TR
    kiwoom.SetInputValue("종목코드", "039490")
    kiwoom.SetInputValue("기준일자", "20160624")
    kiwoom.SetInputValue("수정주가구분", 1)
    kiwoom.CommRqData("opt10081_req", "opt10081", 0, "0101")

    while kiwoom.prev_next == '2':
        time.sleep(0.2)
        kiwoom.SetInputValue("종목코드", "039490")
        kiwoom.SetInputValue("기준일자", "20160624")
        kiwoom.SetInputValue("수정주가구분", 1)
        kiwoom.CommRqData("opt10081_req", "opt10081", 2, "0101")

