import os
import shutil
import threading
import sys

from PyQt5.QtCore import Qt, QTimer, QRectF, QPoint
from PyQt5.QtWidgets import QProgressBar, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QDesktopWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPainterPath
import winreg

common_conf_path = os.path.join(os.environ["USERPROFILE"], ".installerData", "ASoj2SoajAWn210W.fdt")

# ------------API------------#

class parse_uninstall_conf:
    def __init__(self) -> None:
        with open(common_conf_path) as conf_file:
            lines = conf_file.read().split("\n")
        self.app_name = lines[0]
        self.uninstall_exe = lines[1]
        self.startmenu_shortcut = (lines[2]=="True")
        self.desktop_shortcut = (lines[3]=="True")
        self.shortcut_name = lines[4]
class appdeleter:
    def __init__(self, install_conf: parse_uninstall_conf):
        self.install_conf = install_conf
        self.files_path = "\\".join(install_conf.uninstall_exe.replace("\\", "/").split("/")[:-1])
    def delete_files(self):
        for item in os.listdir(self.files_path):
            if os.path.isdir(item):
                shutil.rmtree(os.path.join(self.files_path, item))
            else:
                if not os.path.join(self.files_path, item).replace("\\", "/") == self.install_conf.uninstall_exe.replace("\\", "/"):
                    os.remove(os.path.join(self.files_path, item))
    def delete_shortcuts(self):
        if self.install_conf.desktop_shortcut:
            if os.path.exists(os.path.join(os.environ["USERPROFILE"], "Desktop")):
                if os.path.exists(os.path.join(os.environ["USERPROFILE"], "Desktop", self.install_conf.shortcut_name+".lnk")):
                    os.remove(os.path.join(os.environ["USERPROFILE"], "Desktop", self.install_conf.shortcut_name+".lnk"))
            if os.path.exists(os.path.join(os.environ["USERPROFILE"], "Onedrive", "Desktop")):
                if os.path.exists(os.path.join(os.environ["USERPROFILE"], "Onedrive", "Desktop", self.install_conf.shortcut_name+".lnk")):
                    os.remove(os.path.join(os.environ["USERPROFILE"], "Onedrive", "Desktop", self.install_conf.shortcut_name+".lnk"))
        if self.install_conf.startmenu_shortcut:
            if os.path.exists(os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start menu", "Programs", self.install_conf.shortcut_name+".lnk")):
                os.remove(os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start menu", "Programs", self.install_conf.shortcut_name+".lnk"))
    def delete_self_and_exit(self):
        shutil.rmtree(os.path.dirname(os.path.abspath(sys.argv[0])))
    def delete_common_settings(self):
        os.remove(common_conf_path)
    def unregister_app(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall", 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteKey(key, self.install_conf.app_name)
            winreg.CloseKey(key)
        except:
            pass

# ------------GUI-------------#

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

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.conf = parse_uninstall_conf()

        self.setWindowTitle(f"{self.conf.app_name} uninstaller")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 

        # BASIC DECLARATIONS
        
        self.vblay = QVBoxLayout(self)
        self.deleter = appdeleter(self.conf)
        self.backgroundColor = hex2QColor("212121")
        self.foregroundColor = hex2QColor("cfcfcf")
        self.borderRadius = 12.0
        self.TBnormalColor = "#cfcfcf"
        self.TBhoverColor = "#858585"
        self.H4normalColor = "#4169a6"
        self.H4hoverColor = "#3061ab"
        self.close_available = True

        # TITLEBAR IMPLEMENTATION

        self.titleBar = QHBoxLayout()

        self.titleLabel = BigText(f"{self.conf.app_name} uninstaller")
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
        self.closeButton.clicked.connect(self.exit_uninstaller)


        self.titleBar.addWidget(self.titleLabel)
        self.titleBar.addStretch()
        self.titleBar.addWidget(self.minimizeButton)
        self.titleBar.addWidget(self.closeButton)

        # OTHER WIDGETS

        self.p_bar = ProgressBar(self)
        self.p_bar.setFixedHeight(20)
        self.setMinimumWidth(600)
        self.finnishedlbl = NormalText()
        self.startButton = QPushButton("Start", self)
        self.startButton.setStyleSheet(f"""background-color: {self.H4normalColor}; border: none; color: #cfcfcf; font-size: 20px; border-radius: 5px;""")
        self.startButton.clicked.connect(self.start_tasks)
        self.startButton.enterEvent = lambda event: self.hoverButtonH4(self.startButton)
        self.startButton.leaveEvent = lambda event: self.normalButtonH4(self.startButton)
        self.startButton.setMinimumWidth(self.startButton.width()+10)

        # ADD TO VBLAY

        self.vblay.addLayout(self.titleBar)
        self.vblay.addWidget(self.p_bar)
        self.vblay.addWidget(self.finnishedlbl)
        self.vblay.addWidget(self.startButton)

        # CALL SOME FUNCTIONS

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
        tasks = self.generate_tasks()
        tasks.append(self.finnish_handler)
        self.toggle_close_availability()
        self.p_bar.tasks = tasks
        self.p_bar.start()

    def finnish_handler(self):
        self.finnishedlbl.setText("The removal process has now finnished. You may close this window or\npress the \"Finnish\" button where the \"Start\" button was.")
        self.startButton.setText("Finish")
        self.startButton.clicked.connect(self.exit_uninstaller)
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

    def exit_uninstaller(self):
        if self.close_available:
            self.deleter.delete_self_and_exit()
            self.close()

    def generate_tasks(self):
        return [
            self.deleter.delete_files,
            self.deleter.delete_shortcuts,
            self.deleter.unregister_app
        ]
    
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