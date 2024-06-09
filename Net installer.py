#---------------------------------------------------------------------CONFIG---------------------------------------------------------------------#

app_name = r"Fast"
app_zip_url = r"https://github.com/PthePro777PRO/Fast-Browser-real/releases/download/v1.1/Fast.browser.zip"
main_file_exe_in_zip = r"main.exe"
uninstall_file_exe_in_zip = r"uninstall.exe"
version = "1.1"
publisher = "PthePro777"
create_startmenu_shortcut = True
create_desktop_shortcut = False
shortcut_name = "Fast browser"
common_data_file = "ASoj2SoajAWn210W.fdt"

#--------------------------------------------------------------------INSTALLER-------------------------------------------------------------------#

from PyQt5.QtCore import Qt, QTimer, QRectF, QPoint
from PyQt5.QtWidgets import QProgressBar, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QCheckBox, QDesktopWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from win32com.client import Dispatch
import os
import urllib.request 
import threading
import sys
import shutil
import winreg

common_data_file_path = os.environ["USERPROFILE"]+"/.installerData/"+common_data_file

def hex2QColor(c):
    return QColor(int(c[0:2],16),int(c[2:4],16),int(c[4:6],16))

class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasks = []

    def start(self):
        self.tasks_completed = 0
        self.total_tasks = len(self.tasks)
        self.update_proc = QTimer(self)
        self.update_proc.timeout.connect(self.update_progbar)
        self.update_proc.start(1)
        threading.Thread(target=self.do_tasks, daemon=True).start()

    def update_progbar(self):
        if self.tasks:
            progress = int(100 * (self.tasks_completed) / self.total_tasks)
            self.setValue(progress)
        else:
            self.setValue(100)

    def do_tasks(self):
        while self.tasks:
            task = self.tasks.pop(0)
            task()
            self.tasks_completed += 1

    def paintEvent(self, event):
        # Forcing rounded corners
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        painter.setClipPath(path)
        super().paintEvent(event)

class QWidgetSubclass(QWidget):pass
class BigText(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPointSize(20)  # Adjust the size as needed
        self.setFont(font)

class NormalText(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPointSize(10)  # Adjust the size as needed
        self.setFont(font)

class MainWindow(QWidgetSubclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"{app_name} installer")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 

        self.create_desktop_shortcut = create_desktop_shortcut
        self.create_startmenu_shortcut = create_startmenu_shortcut
        self.backgroundColor = hex2QColor("212121")
        self.foregroundColor = hex2QColor("cfcfcf")
        self.borderRadius = 12.0
        self.TBnormalColor = "#cfcfcf"
        self.TBhoverColor = "#858585"
        self.H4normalColor = "#4169a6"
        self.H4hoverColor = "#3061ab"
        self.close_available = True
        self.started = False

        self.this_file = os.path.abspath(sys.argv[0])

        self.vblay = QVBoxLayout(self)

        # TITLEBAR IMPLEMENTATION

        self.titleBar = QHBoxLayout()

        self.titleLabel = BigText(f"{app_name} installer")
        self.minimizeButton = QPushButton("—", self)
        self.closeButton = QPushButton("✕", self)

        button_font_size = "20px"
        self.minimizeButton.setStyleSheet(f"""background-color: transparent; border: none; color: #cfcfcf; font-size: {button_font_size};""")
        self.closeButton.setStyleSheet(f"""background-color: transparent; border: none; color: #cfcfcf; font-size: {button_font_size};""")

        self.minimizeButton.setFocusPolicy(Qt.NoFocus)
        self.closeButton.setFocusPolicy(Qt.NoFocus)

        self.minimizeButton.enterEvent = lambda event: self.hoverButtonTB(self.minimizeButton)
        self.minimizeButton.leaveEvent = lambda event: self.normalButtonTB(self.minimizeButton)
        self.closeButton.enterEvent = lambda event: self.hoverButtonTB(self.closeButton)
        self.closeButton.leaveEvent = lambda event: self.normalButtonTB(self.closeButton)

        self.minimizeButton.clicked.connect(self.showMinimized)
        self.closeButton.clicked.connect(self.exit_installer)


        self.titleBar.addWidget(self.titleLabel)
        self.titleBar.addStretch()
        self.titleBar.addWidget(self.minimizeButton)
        self.titleBar.addWidget(self.closeButton)


        # HBLAY1: Choose install path

        self.hblay1 = QHBoxLayout()
        
        self.outpath_lbl = NormalText(self)
        self.outpath_lbl.setText("Path to install in: ")
        self.outpath = QLineEdit(self)
        outpath_font = self.outpath.font()
        outpath_font.setPointSize(10)
        self.outpath.setFont(outpath_font)
        self.outpath.setText(os.environ["LOCALAPPDATA"]+"\\"+app_name)

        self.hblay1.addWidget(self.outpath_lbl)
        self.hblay1.addWidget(self.outpath)

        # HBLAY2: Choose whether to create desktop shortcut or not

        self.hblay2 = QHBoxLayout()
        
        self.desktop_shortcut = QCheckBox(self)
        self.desktop_shortcut.stateChanged.connect(self.set_desktop)
        self.desktop_shortcut.setChecked(self.create_desktop_shortcut)
        self.desktop_shortcut_lbl = NormalText(self)
        self.desktop_shortcut_lbl.setText("Create desktop shortcut")

        self.hblay2.addWidget(self.desktop_shortcut)
        self.hblay2.addWidget(self.desktop_shortcut_lbl)

        # HBLAY3: Choose whether to start menu shortcut or not

        self.hblay3 = QHBoxLayout()
        
        self.startmenu_shortcut = QCheckBox(self)
        self.startmenu_shortcut.stateChanged.connect(self.set_startmenu)
        self.startmenu_shortcut.setChecked(self.create_startmenu_shortcut)
        self.startmenu_shortcut_lbl = NormalText(self)
        self.startmenu_shortcut_lbl.setText("Create start menu shortcut")

        self.hblay3.addWidget(self.startmenu_shortcut)
        self.hblay3.addWidget(self.startmenu_shortcut_lbl)

        self.p_bar = ProgressBar(self)
        self.p_bar.setFixedHeight(20)
        self.setMinimumWidth(600)

        # HBLAY4: Start and finish buttons

        self.hblay4 = QHBoxLayout()
        
        self.startButton = QPushButton("Start", self)
        self.startButton.setStyleSheet(f"""background-color: {self.H4normalColor}; border: none; color: #cfcfcf; font-size: 20px; border-radius: 5px;""")
        self.startButton.clicked.connect(self.start_tasks)
        self.startButton.enterEvent = lambda event: self.hoverButtonH4(self.startButton)
        self.startButton.leaveEvent = lambda event: self.normalButtonH4(self.startButton)

        self.hblay4.addWidget(self.startButton)
        self.hblay4.addStretch()

        self.startButton.setMinimumWidth(self.startButton.width()+10)

        # LABEL FOR WHEN FINISHED
        
        self.finishedlbl = NormalText()

        # ADDING WIDGET & AND LAYOUTS TO VBLAY

        self.vblay.addLayout(self.titleBar)
        self.vblay.addLayout(self.hblay1)
        self.vblay.addLayout(self.hblay2)
        self.vblay.addLayout(self.hblay3)
        self.vblay.addWidget(self.p_bar)
        self.vblay.addWidget(self.finishedlbl)
        self.vblay.addLayout(self.hblay4)

        self.center()
        self.init_css()
        self.setLayout(self.vblay)

    def toggle_close_availability(self):
        self.close_available = not self.close_available
        if self.close_available:
            self.closeButton.setStyleSheet("background-color: transparent; border: none; color: #cfcfcf; font-size: 20px;")
        else:
            self.closeButton.setStyleSheet("background-color: transparent; border: none; color: #858585; font-size: 20px;")

    def start_tasks(self):
        if not self.started:
            tasks = self.generate_tasks(self.outpath.text())
            tasks.append(self.finish_handler)
            self.toggle_close_availability()
            self.p_bar.tasks = tasks
            self.p_bar.start()
            self.started = True

    def finish_handler(self):
        self.finishedlbl.setText("The installation process has now finished. You may close this window or\npress the \"finish\" button where the \"Start\" button was.")
        self.startButton.setText("Finish")
        self.startButton.clicked.connect(self.close)
        self.toggle_close_availability()

    def hoverButtonTB(self, button):
        button.setStyleSheet(f"""background-color: transparent; border: none; color: {self.TBhoverColor}; font-size: 20px;""")
    
    def normalButtonTB(self, button):
        if self.close_available:
            button.setStyleSheet(f"""background-color: transparent; border: none; color: {self.TBnormalColor}; font-size: 20px;""")

    def hoverButtonH4(self, button):
        button.setStyleSheet(f"""background-color: {self.H4hoverColor}; border: none; color: #cfcfcf; font-size: 20px; border-radius: 5px;""")
    
    def normalButtonH4(self, button):
        button.setStyleSheet(f"""background-color: {self.H4normalColor}; border: none; color: #cfcfcf; font-size: 20px; border-radius: 5px;""")

    def exit_installer(self):
        if self.close_available:
            self.close()

    def save_conf(self, app_path):
        os.makedirs(os.environ["USERPROFILE"]+"/.installerData", exist_ok=True)
        with open(common_data_file_path, "w+") as conf_file:
            conf_file.write(f"{app_name}\n{app_path+'/'+uninstall_file_exe_in_zip}\n{create_startmenu_shortcut}\n{create_desktop_shortcut}\n{shortcut_name}")

    def register_app(self, app_path):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall")

        subkey = winreg.CreateKeyEx(key, app_name, 0, winreg.KEY_ALL_ACCESS)

        winreg.SetValueEx(subkey, "DisplayName", 0, winreg.REG_SZ, app_name)
        winreg.SetValueEx(subkey, "DisplayIcon", 0, winreg.REG_SZ, app_path+"/"+main_file_exe_in_zip)
        winreg.SetValueEx(subkey, "DisplayVersion", 0, winreg.REG_SZ, version)
        winreg.SetValueEx(subkey, "Publisher", 0, winreg.REG_SZ, publisher)
        winreg.SetValueEx(subkey, "InstallLocation", 0, winreg.REG_SZ, app_path)
        winreg.SetValueEx(subkey, "UninstallString", 0, winreg.REG_SZ, app_path+"/"+uninstall_file_exe_in_zip)

        winreg.CloseKey(subkey)
        winreg.CloseKey(key)

    def init_css(self):
        self.setStyleSheet("""
        QWidgetSubclass{
            background-color: #212121;
            color: #cfcfcf;
            padding: 0px;
            border-radius: 12px;
        }
        QLineEdit {
            background-color: #212121;
            color: #cfcfcf;
            border-radius: 5px;
            border: 2px solid grey;
        }
        NormalText {
            color: #cfcfcf;            
        }
        BigText {
            color: #cfcfcf;            
        }
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #05B8CC;
            width: 20px;
        }
        """)

    def set_startmenu(self):
        if self.startmenu_shortcut.isChecked():
            self.create_startmenu_shortcut = True
        else:
            self.create_startmenu_shortcut = False

    def set_desktop(self):
        if self.desktop_shortcut.isChecked():
            self.create_desktop_shortcut = True
        else:
            self.create_desktop_shortcut = False

    def createShortcut(self, path, icon, target_path, cwd):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(path)
        shortcut.TargetPath = target_path
        shortcut.IconLocation = icon
        shortcut.WorkingDirectory = cwd
        shortcut.Save()

    def generate_tasks(self, out_path):
        
        out = [lambda: urllib.request.urlretrieve(app_zip_url, os.environ["LOCALAPPDATA"]+"/temp/appzip.zip"), lambda: shutil.unpack_archive(os.environ["LOCALAPPDATA"]+"/temp/appzip.zip", out_path, 'zip')]
        if self.create_startmenu_shortcut:
            out.append(
                lambda self=self: self.createShortcut(os.environ["APPDATA"]+"/Microsoft/Windows/Start menu/Programs/"+shortcut_name+".lnk", out_path+"/"+main_file_exe_in_zip, out_path+"/"+main_file_exe_in_zip, out_path)
            )
        if self.create_desktop_shortcut:
            if os.path.exists(os.environ["USERPROFILE"]+"/Desktop"):
                out.append(
                    lambda self=self: self.createShortcut(os.environ["USERPROFILE"]+"/Desktop/"+shortcut_name+".lnk", out_path+"/"+main_file_exe_in_zip, out_path+"/"+main_file_exe_in_zip, out_path)
                )
            elif os.path.exists(os.environ["USERPROFILE"]+"/Onedrive/Desktop"):
                out.append(
                    lambda self=self: self.createShortcut(os.environ["USERPROFILE"]+"/Onedrive/Desktop/"+shortcut_name+".lnk", out_path+"/"+main_file_exe_in_zip, out_path+"/"+main_file_exe_in_zip, out_path)
                )

        out += [
            lambda self=self, out_path=out_path: self.register_app(out_path),
            lambda out_path=out_path: self.save_conf(out_path),
            lambda: os.remove(os.environ["LOCALAPPDATA"]+"/temp/appzip.zip")
        ]
        return out
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def paintEvent(self, event):
        # get current window size
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(self.foregroundColor)
        qp.setBrush(self.backgroundColor)
        qp.drawRoundedRect(0, 0, s.width(), s.height(),
                           self.borderRadius, self.borderRadius)
        qp.end()

app = QApplication([])
win = MainWindow()
win.show()
app.exec()