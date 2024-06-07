import requests


with open("fl")as f:firtslaunch=f.read()!=""
if firtslaunch:import fl;fl.run()
else:
    # IMPORTS
    import os
    import sys
    import customs
    import keyboard
    import pyautogui;pyautogui.FAILSAFE = False
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    # WEB ENGEINE( pip install PyQtWebEngine)
    from PyQt5.QtWebEngineWidgets import *
    from PyQt5.QtWebEngineCore import *
    #THEME MONITOR
    #JSON READER
    import json
    with open("html/historyheader.html")as hishfil:
        historyheader = hishfil.read()
    
    with open("html/history.html", 'r') as hsf:
        historyfooter = hsf.read().split(historyheader)[0]

    bookmarkdata = {}
    bookmarks = {}                   
    
    class MainWindow(QMainWindow):
        def __init__(self, *args, **kwargs):
            global bookmarkdata
            global bmbar
            with open("html/newtab.html")as newtabfil:
                self.nthtml = newtabfil.read()
            with open("css/dark.css")as darkcssfil:
                self.darkcss = darkcssfil.read()
            with open("css/light.css")as lightcssfil:
                self.lightcss = lightcssfil.read()
            
            global bookmarks
            super(MainWindow, self).__init__(*args, **kwargs)
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.show()

            # ADD WINDOW ELEMENTS
            # ADD TAB WIGDETS TO DISPLAY WEB TABS
            x, y = pyautogui.size()
            self.browser = QWebEngineView()
            self.browser.page().profile().downloadRequested.connect(
                self.on_downloadRequested
            )
            self.browserSettings=self.browser.settings()
            self.browserSettings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
            self.browserSettings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            self.browserSettings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            self.browserSettings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
            self.browser.page().fullScreenRequested.connect(self.FullscreenRequest)
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            transparencyfile = open("options/transparency", "r")
            transparencylevel = transparencyfile.read()
            transparencyfile.close()
            if transparencylevel.replace(" ", "").replace("\n", "") == "9":
                self.t1a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "8":
                self.t2a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "7":
                self.t3a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "6":
                self.t4a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "5":
                self.t5a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "4":
                self.t6a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "3":
                self.t7a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "2":
                self.t8a()
            elif transparencylevel.replace(" ", "").replace("\n", "") == "1":
                self.t9a()
            self.tabs = QTabWidget()
            self.tabs.setDocumentMode(True)
            self.tabs.setTabsClosable(True)
            self.setCentralWidget(self.tabs)
            self.setGeometry( int(x/2)-600, int(y/2)-350, 1200, 700)

            self.menubarwidget = QMenuBar(self)
            self.setMenuBar(self.menubarwidget)

            tm = self.menuBar().addMenu("&Options")
            themefile = open("options/theme", "r")
            self.theme = themefile.read()
            transp_menu = tm.addMenu("&Window Transparency")
            theme_menu = tm.addMenu("&Theme")
            dark = QAction("Dark mode", self)
            light = QAction("Light mode", self)
            dark.triggered.connect(lambda _: self.dark())
            light.triggered.connect(lambda _: self.light())
            theme_menu.addAction(dark)
            theme_menu.addAction(light)
            guimagnif = tm.addMenu("&Gui Magnification")
            gui1 = QAction("1x   ", self)
            gui125 = QAction("1.25x", self)
            gui15 = QAction("1.50x", self)
            gui175 = QAction("1.75x", self)
            gui2 = QAction("2x   ", self)
            guimagnif.addAction(gui1)
            guimagnif.addAction(gui125)
            guimagnif.addAction(gui15)
            guimagnif.addAction(gui175)
            guimagnif.addAction(gui2)
            gui1.triggered.connect(lambda _: self.magnifygui(16))
            gui125.triggered.connect(lambda _: self.magnifygui(20))
            gui15.triggered.connect(lambda _: self.magnifygui(24))
            gui175.triggered.connect(lambda _: self.magnifygui(28))
            gui2.triggered.connect(lambda _: self.magnifygui(32))
            t1 = QAction("90%", self)
            t2 = QAction("80%", self)
            t3 = QAction("70%", self)
            t4 = QAction("60%", self)
            t5 = QAction("50%", self)
            t6 = QAction("40%", self)
            t7 = QAction("30%", self)
            t8 = QAction("20%", self)
            t9 = QAction("10%", self)
            t0 = QAction("0%", self)
            transp_menu.addAction(t1)
            transp_menu.addAction(t2)
            transp_menu.addAction(t3)
            transp_menu.addAction(t4)
            transp_menu.addAction(t5)
            transp_menu.addAction(t6)
            transp_menu.addAction(t7)
            transp_menu.addAction(t8)
            transp_menu.addAction(t9)
            transp_menu.addAction(t0)
            # ADD NEW TAB
            t1.triggered.connect(lambda _: self.t1a())
            t2.triggered.connect(lambda _: self.t2a())
            t3.triggered.connect(lambda _: self.t3a())
            t4.triggered.connect(lambda _: self.t4a())
            t5.triggered.connect(lambda _: self.t5a())
            t6.triggered.connect(lambda _: self.t6a())
            t7.triggered.connect(lambda _: self.t7a())
            t8.triggered.connect(lambda _: self.t8a())
            t9.triggered.connect(lambda _: self.t9a())
            t0.triggered.connect(lambda _: self.t0a())
            
            self.TITLEBAR = customs.CustomTitleBar(self)
            self.menuBar().addSeparator()
            self.menuBar().setCornerWidget(self.TITLEBAR, Qt.Corner.TopRightCorner)
            f = open("options/ptsf", "r")
            ptsf = f.read()
            f.close()
            if ptsf == "False":
                self.ptsfaction = QAction("Always prompt where to save file", self)
                self.ptsfaction.triggered.connect(self.triggerf)
            elif ptsf == "True":
                self.ptsfaction = QAction("Always prompt where to save file  ✓", self)
                self.ptsfaction.triggered.connect(self.triggert)
            tm.addAction(self.ptsfaction)

            # ADD DOUBLE CLICK EVENT LISTENER
            self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
            # ADD TAB CLOSE EVENT LISTENER
            self.tabs.tabCloseRequested.connect(self.close_current_tab)
            # ADD ACTIVE TAB CHANGE EVENT LISTENER
            self.tabs.currentChanged.connect(self.current_tab_changed)

            # ADD NAVIGATION TOOLBAR
            self.navtb = QToolBar("Navigation")
            self.navtb.setIconSize(QSize(30, 30))
            self.navtb.setMovable(False)
            self.addToolBar(self.navtb)

            self.his = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-history.png'))), "History", self)
            self.his.setStatusTip("History")
            self.navtb.addAction(self.his)
            self.his.triggered.connect(self.openhistory)

            # ADD BUTTONS TO NAVIGATION TOOLBAR
            # PREVIOUS WEB PAGE BUTTON
            self.back_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-arrow-circle-left.png'))), "Back", self)
            self.back_btn.setStatusTip("Back to previous page")
            self.navtb.addAction(self.back_btn)
            # NAVIGATE TO PREVIOUS PAGE
            self.back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

            #self.console=ConsoleWindow(self)
            #self.console.show()

            # NEXT WEB PAGE BUTTON
            self.next_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-arrow-circle-right.png'))), "Forward", self)
            self.next_btn.setStatusTip("Forward to next page")
            self.navtb.addAction(self.next_btn)
            # NAVIGATE TO NEXT WEB PAGE
            self.next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

            # REFRESH WEB PAGE BUTTON
            self.reload_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-reload.png'))), "Reload", self)
            self.reload_btn.setStatusTip("Reload page")
            self.navtb.addAction(self.reload_btn)
            # RELOAD WEB PAGE
            self.reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())




            # HOME PAGE BUTTON
            self.home_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-home.png'))), "Home", self)
            self.home_btn.setStatusTip("Go home")
            self.navtb.addAction(self.home_btn)
            # NAVIGATE TO DEFAULT HOME PAGE
            self.home_btn.triggered.connect(self.navigate_home)

            self.new_tab_action = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-newtab.png'))), "New Tab", self)
            self.new_tab_action.setStatusTip("Open a new tab")
            self.new_tab_action.setShortcut("Ctrl+T")
            self.navtb.addAction(self.new_tab_action)
            self.new_tab_action.triggered.connect(lambda _: self.add_new_tab())

            self.bookmarks_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-open-bookmarks.png'))), "Delete a bookmark", self)
            self.bookmarks_btn.triggered.connect(lambda: self.delbookmark())
            self.bookmarks_btn.setStatusTip("Delete a bookmark")
            self.navtb.addAction(self.bookmarks_btn)

            self.bookmark_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-add-bookmark.png'))), "Add this page as a bookmark",self)
            self.bookmark_btn.setStatusTip("Add this page as a bookmark")
            self.bookmark_btn.triggered.connect(self.add_bookmark)
            self.navtb.addAction(self.bookmark_btn)


            # ADD SEPARATOR TO NAVIGATION BUTTONS
            self.navtb.addSeparator()

            # ADD LABEL ICON TO SHOW THE SECURITY STATUS OF THE LOADED URL
            self.httpsicon = QLabel()  
            self.httpsicon.setPixmap(QPixmap(self.resource_path(os.path.join('icons', f'lock-locked.png'))))
            self.navtb.addWidget(self.httpsicon)
            # ADD LINE EDIT TO SHOW AND EDIT URLS
            self.urlbar = QLineEdit()
            self.navtb.addWidget(self.urlbar)
            #self.urlbar.
            # LOAD URL WHEN ENTER BUTTON IS PRESSED
            self.urlbar.returnPressed.connect(self.navigate_to_url)

            # ADD STOP BUTTON TO STOP URL LOADING
            self.stop_btn = QAction(QIcon(self.resource_path(os.path.join('icons', f'{self.theme}-media-stop.png'))), "Stop", self)
            self.stop_btn.setStatusTip("Stop loading current page")
            self.navtb.addAction(self.stop_btn)
            # STOP URL LOADING
            self.stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
            bmbar.setIconSize(QSize(30, 30))
            bookmarks = self.read_bookmarks()
            self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)
            self.addToolBar(Qt.ToolBarArea.TopToolBarArea, bmbar)
            bookmarkdata = self.read_bookmarks()
            for bookmark_name in bookmarks:
                bookmark_url = bookmarks[bookmark_name]
                bookmark_btn = QAction(bookmark_name, self)      
                dta = {}
                dta["url"]=bookmark_url
                dta["actionID"] = bookmark_btn
                bookmark_btn.triggered.connect(lambda _, url=bookmark_url: self.add_new_tab(url)) 
                bmbar.addAction(bookmark_btn)
                bookmarkdata[bookmark_name] = dta

            self.status = QStatusBar()
            self.setStatusBar(self.status)

            self.progress = QProgressBar()
            self.progress.setMaximumWidth(120)
            self.status.addPermanentWidget(self.progress)

            # SET WINDOW TITTLE AND ICON
            self.setWindowTitle("Fast Browser")
            self.setWindowIcon(QIcon(self.resource_path(os.path.join('icons', f'icon.png'))))         

            # ADD STYLESHEET TO CUSTOMIZE YOUR WINDOWS
            # STYLESHEET (DARK MODE)
            if self.theme == "dark":
                self.dark()
            elif self.theme == "light":
                self.light()
            self.add_new_tab(QUrl('fast://newtab'), 'Home')
            self.navigate_home()
            self.show()

        # ############################################
        # FUNCTIONS
        ##############################################
        #SAVE THEME
        def save_theme(self,theme):
            th = open("options/theme", "w+")
            th.write(theme)
            th.close()
        #DARK THEME
        def dark(self):
            self.setStyleSheet(self.darkcss)
            self.theme = 'dark'
            self.save_theme("dark")
            self.refresh_btn_icons()
            self.TITLEBAR.setStyleSheet("""
                background-color: #333;
                color: white;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 5px;
            """)
            self.tabs.setStyleSheet("""
                QTabWidget::tab:selected {
                    background-color: #333;
                    color: white; /* Text color */
                }
            """)
        #LIGHT THEME
        def light(self):
            self.setStyleSheet(self.lightcss)
            self.theme = 'light'
            self.save_theme("light")
            self.refresh_btn_icons()
            self.TITLEBAR.setStyleSheet("""
                background-color: #ccc;
                color: black;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 5px;
            """)
            self.tabs.setStyleSheet("""
                QTabWidget::tab:selected {
                    background-color: #ccc;
                    color: white; /* Text color */
                }
            """)
        
        def resource_path(self, relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            #try:
            #    # PyInstaller creates a temp folder and stores path in _MEIPASS
            #    base_path = sys._MEIPASS
            #except Exception:
            #    base_path = os.path.abspath(".")

            return os.path.join(os.path.abspath("."), relative_path)

        #MAGNIFY GUI
        def maxres(self):
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()
        # ADD NEW WEB TAB
        def add_new_tab(self, qurl="fast://newtab", label="Blank"): #new tab official page: https://sites.google.com/view/my--browser
            # Check if url value is blank
            if qurl is None:
                qurl = QUrl('')#pass empty string to url

            # Load the passed url
            browser = QWebEngineView()
            if qurl == 'fast://newtab':
                browser.setHtml(self.nthtml)
                # ADD THE WEB PAGE TAB
                i = self.tabs.addTab(browser, label)
                self.tabs.setCurrentIndex(i)

                # ADD BROWSER EVENT LISTENERS
                # On URL change
                browser.urlChanged.connect(lambda qurl, browser=browser:
                                        self.update_urlbar(QUrl("New Tab"), browser))
                # On loadfinished
                browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                            self.tabs.setTabText(i, browser.page().title()))
            elif qurl == 'fast://history':
                i = self.tabs.addTab(browser, label)
                self.tabs.setCurrentIndex(i)
                # ADD BROWSER EVENT LISTENERS
                # On URL change
                browser.urlChanged.connect(lambda qurl, browser=browser:
                                        self.update_urlbar(QUrl("History"), browser))
                # On loadfinished
                browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                            self.tabs.setTabText(i, browser.page().title()))
            elif qurl == 'fast://snake':
                i = self.tabs.addTab(browser, label)
                self.tabs.setCurrentIndex(i)
                # ADD BROWSER EVENT LISTENERS
                # On URL change
                browser.urlChanged.connect(lambda qurl, browser=browser:
                                        self.update_urlbar(QUrl("No wifi"), browser))
                # On loadfinished
                browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                            self.tabs.setTabText(i, browser.page().title()))
                
            else:
                try:
                    if not self.noWifi():
                        browser.setUrl(QUrl(qurl))
                        # ADD THE WEB PAGE TAB
                        i = self.tabs.addTab(browser, label)
                        self.tabs.setCurrentIndex(i)

                        # ADD BROWSER EVENT LISTENERS
                        # On URL change
                        browser.urlChanged.connect(lambda qurl, browser=browser:
                                                self.update_urlbar(qurl, browser))
                        # On loadfinished
                        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                                    self.tabs.setTabText(i, browser.page().title()))
                except:
                    
                        browser.setUrl(QUrl(qurl))
                        # ADD THE WEB PAGE TAB
                        i = self.tabs.addTab(browser, label)
                        self.tabs.setCurrentIndex(i)

                        # ADD BROWSER EVENT LISTENERS
                        # On URL change
                        browser.urlChanged.connect(lambda qurl, browser=browser:
                                                self.update_urlbar(qurl, browser))
                        # On loadfinished
                        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                                    self.tabs.setTabText(i, browser.page().title()))
            
        def triggerf(self):
            self.ptsfaction.setText('Always prompt where to save file ✓')
            self.ptsfaction.triggered.connect(self.triggert)
            f =open("options/ptsf", "w+")
            f.write("True")
            f.close()
        def triggert(self):
            self.ptsfaction.setText('Always prompt where to save file')
            self.ptsfaction.triggered.connect(self.triggerf)
            f =open("options/ptsf", "w+")
            f.write("False")
            f.close()

        # ADD NEW TAB ON DOUBLE CLICK ON TABS
        def tab_open_doubleclick(self, i):
            if i == -1:  # No tab under the click
                self.add_new_tab()

        # CLOSE TABS 
        def close_current_tab(self, i):
            if self.tabs.count() < 2: #Only close if there is more than one tab open
                return

            self.tabs.removeTab(i)

        def record_history(self, url):
            global historyfooter
            if "data:text/html;charset" not in url:
                main = open("html/history.html", "w+")
                if not url.startswith("fast://"):
                    historyfooter = "<p>"+url+"</p>\n"+historyfooter
                main.write(historyheader+historyfooter)
        def t1a(self):
            self.setWindowOpacity(0.1)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(9))
            transparencyfile.close()
        def t2a(self):
            self.setWindowOpacity(0.2)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(8))
            transparencyfile.close()
        def t3a(self):
            self.setWindowOpacity(0.3)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(7))
            transparencyfile.close()
        def t4a(self):
            self.setWindowOpacity(0.4)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(6))
            transparencyfile.close()
        def t5a(self):
            self.setWindowOpacity(0.5)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(5))
            transparencyfile.close()
        def t6a(self):
            self.setWindowOpacity(0.6)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(4))
            transparencyfile.close()
        def t7a(self):
            self.setWindowOpacity(0.7)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(3))
            transparencyfile.close()
        def t8a(self):
            self.setWindowOpacity(0.8)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(2))
            transparencyfile.close()
        def t9a(self):
            self.setWindowOpacity(0.9)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(1))
            transparencyfile.close()
        def t0a(self):
            self.setWindowOpacity(1)
            transparencyfile = open("options/transparency", "w+")
            transparencyfile.write(str(0))
            transparencyfile.close()
        def refresh_btn_icons(self): #NEEDED FOR THEME-SWITCHING
            buttons = {
                self.resource_path(f'icons/{self.theme}-add-bookmark.png'): self.bookmark_btn, 
                self.resource_path(f'icons/{self.theme}-newtab.png'): self.new_tab_action, 
                self.resource_path(f'icons/{self.theme}-home.png'):self.home_btn, 
                self.resource_path(f'icons/{self.theme}-reload.png'):self.reload_btn, 
                self.resource_path(f'icons/{self.theme}-arrow-circle-right.png'):self.next_btn, 
                self.resource_path(f'icons/{self.theme}-arrow-circle-left.png'):self.back_btn, 
                self.resource_path(f'icons/{self.theme}-history.png'):self.his, 
                self.resource_path(f'icons/{self.theme}-open-bookmarks.png'):self.bookmarks_btn,
                self.resource_path(f'icons/{self.theme}-media-stop.png'):self.stop_btn
            }
            for i in buttons:
                buttons[i].setIcon(QIcon(self.resource_path(os.path.join('icons', i))))
        # UPDATE URL TEXT WHEN ACTIVE TAB IS CHANGED
        def update_urlbar(self, q, browser=None):
            if browser != self.tabs.currentWidget(): 
                # If this signal is not from the current tab, ignore
                return
            
            # URL Schema
            if q.scheme() == 'https':
                icon_path = 'icons/lock-locked.png'
            else:
                icon_path = 'icons/lock-unlocked.png'
            
            if self.httpsicon.pixmap().cacheKey() != QPixmap(self.resource_path(icon_path)).cacheKey():
                # Update security icon only if it has changed
                self.httpsicon.setPixmap(QPixmap(self.resource_path(icon_path)))

            current_url = self.tabs.currentWidget().url().toString()
            if current_url == "https://sites.google.com/view/my--browser":
                self.urlbar.setText("")
            elif current_url.startswith('data:text/html'):
                if 'New Tab' in current_url:
                    self.urlbar.setText("New Tab")
                elif 'No wifi' in current_url:
                    self.urlbar.setText("No wifi")
            else:
                self.urlbar.setText(current_url)

            self.record_history(self.urlbar.text())
            self.urlbar.setCursorPosition(0)

        def unregisterbookmark(self, bookname, id, pressed):
            bookms = self.read_bookmarks()
            del bookms[bookname]
            f = open("bookmarks.json", "w+")
            f.write(str(bookms).replace("'", '"'))
            f.close()
            bmbar.removeAction(id)
            self.DelBar.removeAction(pressed)

        def delbookmark(self):
            #si.wShowWindow = subprocess.SW_HIDE # default
            self.DelBar = QToolBar("Delete Bookmarks", self)
            self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.DelBar)
            bms = self.read_bookmarks()
            for bookmark_name in bms:
                db = QAction("Delete "+bookmark_name, self)
                bid = bookmarkdata[bookmark_name]["actionID"]
                db.triggered.connect(lambda _, sid=bid, name=bookmark_name, cd=db: self.unregisterbookmark(name, sid, cd)) 
                self.DelBar.addAction(db)
            close = QAction("Close", self)
            close.triggered.connect(self.DelBar.deleteLater)
            self.DelBar.addAction(close)
        
        def editbookmark(self):pass
        def read_bookmarks(self):
            return json.load(open("bookmarks.json"))


        # ACTIVE TAB CHANGE ACTIONS
        def current_tab_changed(self, i):
            # i = tab index
            # GET CURRENT TAB URL
            qurl = self.tabs.currentWidget().url()
            # UPDATE URL TEXT
            self.update_urlbar(qurl, self.tabs.currentWidget())
            # UPDATE WINDOWS TITTLE
            self.update_title(self.tabs.currentWidget())

        # UPDATE WINDOWS TITTLE
        def update_title(self, browser):
            if browser != self.tabs.currentWidget():
                # If this signal is not from the current ACTIVE tab, ignore
                return

            title = self.tabs.currentWidget().page().title()
            self.setWindowTitle(title)
        
        def toggle_maximize(self):
            if self.isMaximized():self.showNormal();self.maximize_button.setIcon(QIcon(f"icons\\{self.theme}-max.png"))
            else:self.showMaximized();self.maximize_button.setIcon(QIcon(f"icons\\{self.theme}-pop.png"))

        # NAVIGATE TO PASSED URL
        def navigate_to_url(self):
            q = QUrl(self.urlbar.text())
            qn = self.urlbar.text().strip()
            if qn == "fast://newtab":
                self.navigate_home()
            elif qn == "fast://history":
                self.openhistory()
            elif qn == "fast://snake":
                with open("html/nowifi.html") as nwf:
                    self.tabs.currentWidget().setHtml(nwf.read())
            else:
                if self.noWifi():
                    return
                if not "." in qn or " " in qn:
                    newq = qn.replace(" ", "%20")
                    self.tabs.currentWidget().setUrl(QUrl(f"https://www.google.com/search?q={newq}"))
                else:
                    if q.scheme() == "":
                        q.setScheme("http")
                    self.tabs.currentWidget().setUrl(q)

        def noWifi(self):
            try:
                requests.get("http://google.com/", timeout=3)
                return False
            except requests.RequestException:
                with open("html/nowifi.html") as nwf:
                    self.tabs.currentWidget().setHtml(nwf.read())
                self.urlbar.setText("No wifi")
                return True

        # NAVIGATE TO DEFAULT HOME PAGE
        def navigate_home(self):
            self.tabs.currentWidget().setHtml(self.nthtml)
            i = self.tabs.currentIndex()
            self.tabs.setTabText(i, "New Tab")


            #self.tabs.currentWidget().setUrl(QUrl("https://sites.google.com/view/my--browser"))

        def add_bookmark(self):
            name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Name:')
            if ok:
                url, ok = QInputDialog.getText(self, 'Add Bookmark', 'URL:')
                if ok:
                    if not url.startswith(("http://", "https://", "fast://")):
                        url = "http://" + url
                    bookmark_action = QAction(name, self)
                    bookmark_action.triggered.connect(lambda: self.add_new_tab(QUrl(url)))
                    self.bmbar.addAction(bookmark_action)
                    self.bookmarks[name] = url
                    with open("bookmarks.json", "w") as fp:
                        json.dump(self.bookmarks, fp)
                    self.bookmarkdata[name] = {"url": url, "actionID": bookmark_action}

        def sethistoryfile(self):
            with open("html/history.html", 'r') as htmlfile:
                self.tabs.currentWidget().setHtml(htmlfile.read())
                i = self.tabs.currentIndex()
                self.tabs.setTabText(i, "History")
                self.urlbar.setText('History')
                self.setWindowTitle("History")

        def openhistory(self):
            if self.urlbar.text() !='New Tab':
                self.sethistoryfile()
            else:
                self.add_new_tab('fast://history', 'History')
        #ALLOW WINDOW TO BE DRAGGABLE
        
        def mousePressEvent(self, event):
            self.oldPos = event.globalPos()
        
        def cc(self):
            while True:
                if keyboard.is_pressed("ctrl"):
                    if keyboard.is_pressed("w"):
                        self.close_current_tab(self.tabs.currentIndex())

        def mouseMoveEvent(self, event):
            if event.buttons() == Qt.LeftButton:
                delta = QPoint(event.globalPos() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()

        def on_downloadRequested(self, download):
            f = open("options/ptsf", "r")
            mdo = f.read()
            f.close()
            if mdo == "True":
                path,_ = QFileDialog.getSaveFileName(self, "Save Download",download.url().path() , "*."+QFileInfo(download.url().path()).suffix())
                download.setPath(path)
            download.accept()
        def createWindow(self, _type):
            if QWebEnginePage.WebWindowType.WebBrowserTab:
                v = MainWindow([self])
                v.resize(640, 480)
                v.show()
                return v
            
        def FullscreenRequest(self, request: QWebEngineFullScreenRequest):
            request.accept()
            print("Requested")
            if request.toggleOn():
                self.showFullScreen()
                self.navtb.hide()
                bmbar.hide()
                self.progress.hide()
                self.status.hide()
            else:
                self.navtb.show()
                bmbar.show()
                self.progress.show()
                self.status.show()
                self.browser.setParent(self)
                self.setCentralWidget(self.browser)
                self.browser.showNormal()
    if __name__ == "__main__":
            app = QApplication(sys.argv)
            bmbar = QToolBar("Bookmarks")
            #interceptor = WebEngineUrlRequestInterceptor()
            #QWebEngineProfile.defaultProfile().setUrlRequestInterceptor(interceptor)
            # APPLICATION NAME
            app.setApplicationName("Fast Browser")
            window = MainWindow()
            app.exec()
