from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:/Program Files/Kiwoom/KiwoomFlash2/khministarter.exe")

account = []
with open("../../data/account.txt", 'r') as f:
    account = f.readlines()

title = "번개 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

idForm = dlg.Edit0
idForm.SetFocus()
idForm.TypeKeys(account[0])

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys(account[1])

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys(account[2])

btn_ctrl = dlg.Button0
btn_ctrl.Click()

time.sleep(50)
os.system("taskkill /im khmini.exe")

