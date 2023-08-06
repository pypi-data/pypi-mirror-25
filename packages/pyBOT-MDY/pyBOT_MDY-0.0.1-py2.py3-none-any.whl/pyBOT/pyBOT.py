from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSplashScreen, QProgressBar, QFileDialog, QAction, QInputDialog, QDesktopWidget, QSystemTrayIcon, QCompleter 
from PyQt5.QtGui import QPixmap, QIcon 
import sys, time, datetime
import threading
import psutil
#import numpy
import pandas as pd
import syntax
import res_rc

import lxml.html

from utils import PandasModel

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo

from tasks import sisactValidator

debug = True
#debug = False

cnx = pymongo.MongoClient()
db = cnx["selenium"]
scripts = db["scripts"]

def dbg(logString):
    print(str(logString))

"""
class Spyder(object):
    driver = webdriver.Firefox()
    #driver.get("http://paginasblancas.pe/")
    driver = webdriver.Ie()
    driver.get("http://intranetsisact/sisact/Index.aspx")
    driver.find_element_by_xpath("//a[@data-target='address']").click()
    driver.find_element_by_name("street").send_keys("carlos izaguirre")
    driver.find_element_by_name("streetNumber").send_keys("2")
    driver.find_element_by_id("aLocality").send_keys(u"los olivos\ue007")
"""

class CacheCleanerWorkerThread(QtCore.QThread):
    def __init__(self, data):
        super(WorkerThread, self).__init__()
        self.setTerminationEnabled(True)
        self.start()

    def run(self):
        print("thread is running")
        pass
    #myworker = CacheCleanerWorkerThread(data)
    #myworker.finished.connect(self.clearCache)

class runkeyFilter(QtCore.QObject):
    runkeyPressed = QtCore.pyqtSignal(name="run")

    def eventFilter(self,  obj,  event):
        if event.type() == QtCore.QEvent.KeyPress:
            #if (event.key() == QtCore.Qt.Key_Return) and (event.modifiers() & QtCore.Qt.ShiftModifier) :
            if (event.key() == QtCore.Qt.Key_Return) and (event.modifiers() & QtCore.Qt.AltModifier) :
                self.runkeyPressed.connect(self.handler)
                self.runkeyPressed.emit()
                print('runkey pressed ready for run %s' % obj.objectName())
                return True
        return False
    def handler(self):
        print ("Hndler is runniing")



source = ""
try:
    form, base = uic.loadUiType("pyBOT.ui")
    source = "ui"
except Exception as e:
    from pyBOTForm import Ui_MainWindow
    form = Ui_MainWindow
    source = "class"
    #background-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69))

class pyBOT (QtWidgets.QMainWindow, form):
    driverType = ""
    title = ""
    processInfo = {}

    startJQuerySelector = ('#', '.', '@', '*',)
    searchMethod = {'#':'id', '.': 'className', '@':'name', '*':'dataAttr', '$':'other'}
    searchMethod2 = {'#': 'self.driver.find_element_by_id', '.': 'self.driver.find_element_by_class_name', '@': 'self.driver.find_element_by_name', '*':'self.driver.find_element_by_xpath', '$':'self.driver.find_element_by_css_selector'}
    elementsWithID = {}
    availableCommands = ('find', 'go', 'exit', 'start',)
    tagNameWithValueOrText = {'div':'text', 'span':'text', 'a':'text', 'li':'text', 'input':'value', 'textarea':'value'}
    tagNameWithValueOrText2 = {'style':'text', 'div':'text', 'span':'text', 'a':'text', 'li':'text', 'input':'get_attribute("value")', 'textarea':'get_attribute("value")'}
    #tagNameWithValueOrText3 = {'style':'text', 'div':'text', 'span':'text', 'a':'text', 'li':'text', 'input':'get("value")', 'textarea':'get("value")'}
    tagNameWithValueOrText3 = {'style':'text_content()', 'div':'text_content()', 'span':'text_content()', 'a':'text_content()', 'li':'text_content()', 'input':'get("value")', 'textarea':'get("value")'}
    unsuscriptableTags = ['style', 'javascript', 'frame', 'iframe', 'frameset']
    goNavigateShortcuts = {'google':'https://www.google.com.pe', 'facebook':'https://www.facebook.com', 'elcomercio':'http://elcomercio.pe', 'sisact':'http://intranetsisact/sisact/Index.aspx', 'siacpost':'http://intranetsiacpost/siacpost-frontend'}

    def __init__(self, mixin_arg, **kwds):
        #https://www.tutorialspoint.com/pyqt/pyqt_signals_and_slots.htm
        #https://programtalk.com/vs2/python/10998/retext/ReText/editor.py/
        #http://pythoncentral.io/
        #https://stackoverflow.com/questions/28037126/how-to-use-qcombobox-as-delegate-with-qtableview
        super().__init__(**kwds)
        self.setupUi(self)
        self.setWindowFlags( QtCore.Qt.Window |
                    QtCore.Qt.CustomizeWindowHint |
                    QtCore.Qt.WindowStaysOnTopHint |
                    #QtCore.Qt.WindowMinimizeButtonHint |
                    #QtCore.Qt.WindowCloseButtonHint |
                    QtCore.Qt.FramelessWindowHint |
                    QtCore.Qt.WindowTitleHint)
        self.title =  self.windowTitle()
        self.setFixedSize(582, 382)
        #self.resize(604,370)
        self.txtCommand.setFocus()
        self.lblStatus = QtWidgets.QLabel(self.centralwidget)
        self.statusbar.addWidget(self.lblStatus)
        self.lblStatus.setText("pyBOT Ready!!!")
        self.txtScript.hide()
        self.chkTopMost.setChecked(True)
        self.txtCommand.setPlaceholderText("insert command")

        self.openFile = QAction(QIcon('open.png'), 'Open', self)
        self.openFile.setShortcut('Ctrl+O')
        self.openFile.setStatusTip('Open new File')
        self.openFile.triggered.connect(self.showDialog)

        self.txtScript.setLineWrapMode(0)
        self.pnlScriptsData.hide()
        self.pnlScriptsData.move(0,0)
        self.highlight = syntax.PythonHighlighter(self.txtScript.document())
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #self.setWindowOpacity(0.5)


        # Set the opacity
        #self.setWindowOpacity(1 - 50 / 100)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.txtScript.setDocumentTitle("My-Script")
        self.runFilter = runkeyFilter(self)
        self.txtScript.installEventFilter(self.runFilter)
        #self.runFilter.connect(self.mbox)
        #self.handler.connect(self.mbox)

        self.tblScripts.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblScripts.setStyleSheet("gridline-color: rgb(191, 191, 191)")
        self.tblScripts.setShowGrid(True)
        font = QtGui.QFont("Calibri (Body)", 7)
        self.tblScripts.setFont(font)

        vh = self.tblScripts.verticalHeader()
        vh.setVisible(True)

        hh = self.tblScripts.horizontalHeader()
        hh.setStretchLastSection(True)
        self.tblScripts.resizeColumnsToContents()
        self.tblScripts.setSortingEnabled(True)
        #self.tblScripts.setShowGrid(True)

        self.mainTab.resize(571, 313)
        self.currentWindowSize = 582
        self.currentTabsSize = 571
        self.pendingProcess = False
        self.webElement = {}
        self.t1 = threading.Thread(target=self.setIDSInCache, args=(self.webElement,))
        self.t1.setDaemon(True)
        self.t1.start()

        self.pbCache.setValue(0)
        self.pbCache.setAlignment(QtCore.Qt.AlignCenter)
        
        self.completer = QCompleter()
        self.txtCommand.setCompleter(self.completer)
        self.model = QtCore.QStringListModel()
        self.completer.setModel(self.model)
        self.model.setStringList(['go', 'find', 'start', 'exit'])
        self.txtCommand.hide()
        self.cboCommand.setEditable(True)
        self.cboCommand.setStyleSheet ("QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}");
        #self.cboCommand.keyPressEvent(self._key_press)   
        

        """
        self.oldPos = self.pos()
        self.mwidget = QtWidgets.QMainWindow(self)
        self.center()
    
    

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        pass

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        pass

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()  #"""
        pass

        """
        def paintEvent(self):
        QPixmap canvas(rect())
        canvas.fill(Qt.transparent) # fill transparent (makes alpha channel available)

        QPainter p(canvas)           # draw on the canvas
        p.setOpacity(0.3)
        p.setBrush(QBrush(Qt.white)) # use the color you like
        p.setPen(QPen(Qt.transparen))

        p.drawRect(rect()) # draws the canvas with desired opacity

        p.start(self)      # now draw on the window itself
        p.drawPixmap(rect(), canvas) #"""


        #self.btnOpenScript.addAction(self.openFile)

        self.__bind__()
        #self.tabWidget.setStyleSheet("padding-bottom:50px; background-color:red;")
        #self.tabBOT.setStyleSheet("padding-bottom:50px; background-color:red;")
        #self.tabTASKS.setStyleSheet("padding-bottom:50px; background-color:red;")
        #self.debugInit()

    
    #"""
        
    def mkeyPressEvent(self, key, count=1):
        # FIXME:qtwebengine Abort scrolling if the minimum/maximum was reached.
        print("RUN")
        for i in range(count):
            pass
            press_evt = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier, 0, 0, 0)
            release_evt = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, key, QtCore.Qt.NoModifier,0, 0, 0)
            self._tab.send_event(press_evt)
            self._tab.send_event(release_evt) #"""
    
    def closeEvent(self, event):
        if not debug:
            reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                               QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                self.hide()
                event.ignore()
                self.sysTray.show()

    def create_sys_tray(self):
        self.sysTray = QSystemTrayIcon(self)
        self.sysTray.setIcon( QtGui.QIcon(':/img/img/pyBOT.ico') )
        self.sysTray.setVisible(True)
        self.sysTray.activated.connect(self.checkIfInTrayMode)
        #self.connect(self.sysTray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.on_sys_tray_activated)

        self.sysTrayMenu = QtWidgets.QMenu(self)
        act = self.sysTrayMenu.addAction("FOO")

    def event(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange and self.isMinimized()):
            # The window is already minimized at this point.  AFAIK,
            # there is no hook stop a minimize event. Instead,
            # removing the Qt.Tool flag should remove the window
            # from the taskbar.
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
            self.sysTray.show()
            return True
        else:
            return super(pyBOT, self).event(event)

    def checkIfInTrayMode(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.sysTray.hide()
            # self.showNormal will restore the window even if it was
            # minimized.
            self.showNormal()

    #@QtCore.pyqtSlot(name="keyPressEvent")
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            self.txtScript.clear()
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.txtScript.setPlainText(data) #appendPlainText, insertText, setPlainText

    def debugInit(self):
        self.startBOT()
        self.procCommand("go google")

    def keyPressEvent(self, event):
        key = event.key()
        if event.modifiers() & QtCore.Qt.ControlModifier:
            self.mbox("modifier with control key")
        elif (event.modifiers() & QtCore.Qt.ShiftModifier) and (key == QtCore.Qt.Key_Return):
            self.mbox("modifier with shift key ready for run")

        if key == QtCore.Qt.Key_Enter:
            #For Enter of keyboard number
            print("key Enter press 1")
            #self.updateUi()
        if key == QtCore.Qt.Key_Return:
            #For Enter of keyboard
            #self.txtScript.keyPressEvent(self, event)
            print("key Enter press 2")
            #self.updateUi()

    def focusManager(self, old, new):
        if now is None and QApplication.activeWindow() is not None:
            print("Set Focus to active window")
            QApplication.activeWindow().setFocus()

    #self.txtScript.viewportEvent.connect(self.copy_the_text)
    def copy_the_text(self, event):
        if isinstance(event, QtGui.QKeyEvent):  # as viewportEvent gets *all* events
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                pass

    def xkeyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_X and ev.modifiers() == QtCore.Qt.AltModifier:
            if self.replace_possible_unicode_sequence():
                ev.accept()
                return
        if ev.key() == QtCore.Qt.Key_Insert:
            self.setOverwriteMode(self.overwriteMode() ^ True)
            ev.accept()
            return
        if self.snippet_manager.handle_key_press(ev):
            self.completion_popup.hide()
            return
        if self.smarts.handle_key_press(ev, self):
            self.handle_keypress_completion(ev)
            return
        QPlainTextEdit.keyPressEvent(self, ev)
        self.handle_keypress_completion(ev)

    def alert(self):
        pass

    def __bind__(self):
        self.btnSend.clicked.connect(self.txtCommand_keyPress)
        self.btnExit.clicked.connect(self.closeBOT)
        self.btnStart.clicked.connect(self.startBOT)
        self.btnDebug.clicked.connect(self.showDebugTask)
        self.btnSwitch.clicked.connect(self.toggleSwitch)
        self.txtCommand.returnPressed.connect(self.txtCommand_keyPress)
        self.lsbxLog.currentItemChanged.connect(self.repeatCommand)
        self.chkTopMost.stateChanged.connect(self.toggleTopMost)
        self.btnOpenScript.clicked.connect(self.showDialog)
        self.btnSaveScript.clicked.connect(self.saveScriptToDB)
        self.btnGetScript.clicked.connect(self.getScriptsFromDB)
        self.btnCancelScriptSelection.clicked.connect(self.closePnlScript)
        self.btnRunScript.clicked.connect(self.runScript)
        self.btnShowGrid.clicked.connect(self.showPanelGrid)
        self.tblScripts.doubleClicked.connect(self.tblScriptsGetSelectedData)
        #self.tblScripts.clicked.connect(self.clicktable)
        """
        self.timerTime = QtCore.QTimer()
        self.timerTime.timeout.connect(self.setTime)
        self.timerTime.start(1000) #"""
        self.create_sys_tray()

        #grow = self.frameGeometry().width()
        #self.txtCommand.setText("%d" % grow)

        #self.txtScript.keyPressEvent(self.mbox)
        #self.txtScript.keyPressEvent.connect(self.txtScriptKeypressEvent)
        #self.txtScript.installEventFilter(self.txtScriptKeypressEvent)
        #self.txtScript.installEventFilter(self.keyPressEvent)
        #self.txtScript.keyPressEvent.connect(self.keyPressEvent)
        #self.connect(self.txtScript, SIGNAL("keyPressEvent(event)"), self.keyPressEvent)
        #self.windowActivationChange(True)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.ActivationChange: #QEvent.FocusIn
            if self.isActiveWindow():
                self.txtCommand.setFocus()
                self.setWindowOpacity(1.0)
            else:
                self.setWindowOpacity(0.5)

    def eventFilter(self, watched, event):
        self.mbox("alert")
        if event.type() == QtCore.QEvent.KeyPress:
            if (event.key() == QtCore.Qt.Key_Return) and (event.modifiers() & QtCore.Qt.ShiftModifier) :
                self.runkeyPressed.emit()
                print('runkey pressed ready for run %s' % obj.objectName())
                return True
        return False


    def windowActivationChange(self, state):
        if state:
            self.mbox("active")
        else:
            self.mbox("inactive")

    def runScript(self):
        strToCompile = self.txtScript.toPlainText()
        compiled = compile(strToCompile, "<string>", "exec")
        #exec(compiled)
        eval(compiled)
    """
    def clicktable(self, index):
        print("Row %s and Column %s was clicked" % (str(index.row()), "column"))
        item = self.tblScripts.model().data(index)
        print("value %s" % str(item)) #"""

    def tblScriptsGetSelectedData(self):
        index = self.tblScripts.selectedIndexes()[3]
        scriptData = str(self.tblScripts.model().data(index))
        self.txtScript.setPlainText(scriptData)

        self.txtScript.setDocumentTitle("title-changed")
        self.txtScript.setReadOnly(True)
        self.txtScript.setStyleSheet("background-color:#E0FEE0;")

        if self.lsbxLog.isVisible():
            self.lsbxLog.hide()
            self.txtScript.show()

        self.pnlScriptsData.hide()

        #indexes = self.tblScripts.selectionModel().selectedRows()
        #print(indexes)
        """
        for index in sorted(indexes):
            print(self.tblScripts.itemAt(1,3))
            #print(str(self.tblScripts.model().data(index)))
            print(str(self.tblScripts.model().data(index)))
            print('Row %d is selected' % index.row()) #"""

    def closePnlScript(self):
        self.pnlScriptsData.hide()

    def getScriptsFromDB(self):
        #globals() script
        scripts_ = scripts.find()
        #mdl = PandasModel(list(scripts_))
        #mdl = pd.DataFrame(list(scripts_), columns = ["script"])
        mdl = pd.DataFrame.from_records(list(scripts_))
        #mdl = pd.DataFrame.from_records(scripts_, )

        mdl2 = PandasModel(mdl)
        rawText = ""
        self.tblScripts.setModel(mdl2)
        for s in scripts_:
            rawText += s['script']
            self.mbox(rawText)
        self.pnlScriptsData.show()

    def processTogglePanel(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerToglePanel)
        self.timer.start(5)

    def setTime(self):
        #self.lblTime.setText(time.strftime("%H"+":"+"%M"+":"+"%S"))
        self.lcdTime.display(time.strftime("%H"+":"+"%M"+":"+"%S"))

    def timerToglePanel(self):
        growWindow = self.currentWindowSize
        growTab = self.currentWindowSize

        direction = self.btnShowGrid.text()

        if direction == ">":
            growedWindow =  growWindow + 40
            growedTab =  growTab + 40
            if growedWindow >= 900:
                growedWindow = 900
                growedTab =  889
                self.timer.stop()
                self.btnShowGrid.setText("<")
        else:
            growedWindow =  growWindow - 40
            growedTab =  growTab - 40
            if growedWindow <= 582:
                growedWindow = 582
                growedTab =  571
                self.timer.stop()
                self.btnShowGrid.setText(">")
        self.currentWindowSize = growedWindow
        self.currentTabsSize = growedTab
        self.mainTab.resize(growedTab,313)
        self.setFixedSize(growedWindow,382)

    def showPanelGrid(self):
        self.processTogglePanel()

    def saveScriptToDB(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter script name:')
        if ok and len(text) > 0:
            id_ = scripts.insert({'name':text,'script':self.txtScript.toPlainText(), 'filename':str(datetime.date.today())})
            if id_:
                self.mbox(str(id_))

    def txtScriptKeypressEvent(self, event):
        pass


    def toggleTopMost(self):
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint) #clear(& ~), enable(|), toggle(^)
        self.show()
        #if self.chkTopMost.isChecked():
            #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            #self.mbox("Is Checked")
            #pass
        #else:
            #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            #self.mbox("Is NOT Checked")
            #pass

    def toggleSwitch(self):
        if self.txtScript.isVisible():
           self.txtScript.hide()
           self.lsbxLog.show()
        elif self.lsbxLog.isVisible():
           self.txtScript.show()
           self.lsbxLog.hide()

    def manageProcess(self):
        driversName = ["iedriverserver.exe", "geckodriver.exe", "chromedriver.exe", "iexplore.exe"]
        p = psutil.Process(browser.service.process.pid)

        for proc in psutil.process_iter():
            try:
                processInfo = proc.as_dict(attrs=['pid', 'name'])
                if processInfo['name'].lower() in driversName:
                    proc.terminate()
                    proc.wait()
            except psutil.NoSuchProcess:
                pass
            #else:
                #print(processInfo)
        try:
            self.lsbxLog.addItem("%s - %s" % (self.driver.service.process.pid, self.driver.service.process.pid))
            #p = psutil.Process(browser.service.process.pid)
            p.terminate()
            p.wait()

            #c = webdriver.Chrome()
            #c.service.process # is a Popen instance for the chromedriver process
            #import psutil
            #p = psutil.Process(c.service.process.pid)
            #print p.get_children(recursive=True)
        except Exception as e:
            pass


            #driver.Navigate().GoToUrl("http://www.whatismyip.com/");
            #driver.SwitchTo().DefaultContent();

            #//Close the ad-popup(s)
            #while (driver.GetWindowHandles().Count > 1)
            #{
                    #var win = driver.GetWindowHandles().Last();
                    #driver.SwitchTo().Window(win);
                    #driver.Close();
            #}
            #driver.Manage().DeleteAllCookies();

    def showDebugTask(self):
        #self.manageProcess()
        slug = ""
        self.mbox(self.txtScript.documentTitle())
        """
        for i in self.elementsWithID:
            print(str(i))
            slug += str(i)
        self.mbox(slug) """

    def closeBOT(self):
        if 'driver' in globals():
            self.driver.close()
        try:
            self.driver.close()
            self.manageProcess()
        except Exception as e:
            pass
        self.close()

    def repeatCommand(self, current, previous):
        self.txtCommand.setText(current.text())
        print(current.text())
        #self.labelBigImageDisplay(current.pixmap())

    def changeText(self):
        global source
        self.lblDebug.setText(source + " - " + self.driverType + " - " +self.txtCommand.text())

    def moveToCorner(self):
        self.screenShape = QDesktopWidget().screenGeometry()
        newX = self.screenShape.width() - self.width()
        newY = self.screenShape.height() - self.height()
        self.move(newX, newY)

    def txtCommand_keyPress(self):

        rawCommand = self.txtCommand.text().strip()
        if len(rawCommand) > 0:
            self.preprocCommand(rawCommand)
            self.txtCommand.clear()
        #self.changeText()

    def preprocCommand(self, rawCommand):
        if rawCommand.lower() == 'exit':
            self.closeBOT()
        elif  rawCommand.lower() == 'start':
            self.startBOT()
            return
        elif rawCommand.lower() == 'tasks':
            taskSS = sisactValidator()
            taskSS.runTask()
            pass
        else:
            self.procCommand(rawCommand)

    def procCommand(self, rawCommand):
        rawCommandParts = rawCommand.split(" ")
        lenghtRawCommandLength = len(rawCommandParts)
        firstPartFromCommand = rawCommandParts[0]
        firstCharFromRawCommand = firstPartFromCommand[0]
        successCommand = False

        if rawCommandParts[0] == "go":
            successCommand = self.goToPage(self.goNavigateShortcuts[rawCommandParts[1]])
            if successCommand:
                self.addLogToBox(rawCommand)
            return

        if firstCharFromRawCommand in self.startJQuerySelector:
            theCriteria, theProperty, theValue = ("", "", "")

            if lenghtRawCommandLength == 2:
                theValue = rawCommandParts[1]

            theCriteria, theProperty = self.getJQueryParts(firstPartFromCommand)
            #self.mbox("run jquery length: %d - criteria [%s] - property [%s] - value [%s] " % (lenghtRawCommandLength, theCriteria, theProperty, theValue))

            successCommand = self.runJqueryMode(firstCharFromRawCommand, theCriteria, theProperty, theValue)
        if successCommand:
            self.addLogToBox(rawCommand)

    def mbox(self, message="Default Message"):
        """self.messageBox = QMessageBox()
        self.messageBox.setIcon(QMessage.Question)
        self.messageBox.setWindowTitle("MESSAGE")
        self.messageBox.setInformativeText(message) """
        #reply = QMessageBox.question(self, 'Message', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #reply = QMessageBox.question(self, 'Message', message, QMessageBox.Yes | QMessageBox.No)
        reply = QMessageBox.question(self, 'Message', message, QMessageBox.Yes)
        #if reply == QMessageBox.Yes:
            #event.accept()
        #else:
            #event.ignore()


    def runJqueryMode(self, firstChar, theCriteria, theProperty, args = ""):
        try:
            theCriteria = theCriteria[1:len(theCriteria)]
            #self.mbox("run jquery length: %d - criteria [%s] - property [%s] - value [%s] " % (len(args), theCriteria, theProperty, str(args)))
            if theProperty.lower() == "click":
                eval(self.searchMethod2[firstChar])(theCriteria).click()
            elif theProperty.lower() == "clear":
                eval(self.searchMethod2[firstChar])(theCriteria).clear()
            elif theProperty.lower() == "value" and len(args) > 0:
                eval(self.searchMethod2[firstChar])(theCriteria).send_keys(str(args))
            return True
        except Exception as e:
            self.lsbxLog.addItem(str(e))

    def getJQueryParts(self, rawJQueryCommand):
        if rawJQueryCommand[0] == ".":
            rawJQueryCommand = rawJQueryCommand[1:len(rawJQueryCommand)]
        return rawJQueryCommand.split(".")

    def bgRUnner(self):
        while myFUnc():
            print("running")

    def setIDSInCache(self, data):        
        #http://infohost.nmt.edu/~shipman/soft/pylxml/web/Element-getchildren.html        
        #doc.xpath("//div[@class='name']/parent::*")
        import os
        while 1:            
            self.setTime()
            while self.pendingProcess:
                self.pendingProcess = False
                try:
                    print("init cache")                    

                    rootPage = lxml.html.fromstring(self.driver.page_source)                   
                    
                    
                    #self.pbCache.setMaximum(qItems)                    
                    """
                    tmpDictWithIDs = rootPage.xpath('//*[@id]')
                    qItems = len(tmpDictWithIDs)
                    dbg("cantidad de items: %d" % qItems)
                    for i, el in enumerate(tmpDictWithIDs, 1): #dgLista
                        #print("XPAYH-MODE- %s" % el.xpath('./@id')[0])
                        #print("GET-MODE %s" % el.get("id"))
                        #print("ATTRIB-MODE %s" % el.attrib["id"])
                        tagName, tagID = ( el.tag, el.attrib["id"],)                        
                        #dbg("item actual: %d - tagName: [%s] - tagID: [%s] - tagValue: [%s]" % (i, tagName, tagID, ''))
                        #""
                        if tagName in self.tagNameWithValueOrText3:
                            if tagName.lower() not in self.unsuscriptableTags:
                                with open("debug.txt", "a") as f:
                                    f.write("item actual: %d - tagName: [%s] - tagID: [%s] - tagValue: [%s] \r\n" % (i, tagName, tagID, eval("el.%s" % self.tagNameWithValueOrText3[tagName])))
                                    f.write(os.linesep)
                                dbg("item actual: %d - tagName: [%s] - tagID: [%s] - tagValue: [%s]" % (i, tagName, tagID, eval("el.%s" % self.tagNameWithValueOrText3[tagName])))
                                self.elementsWithID[tagID] = [tagName, eval("el.%s" % self.tagNameWithValueOrText3[tagName])] #"""
                        
                        
                    #"""
                    #"""
                    tmpDictWithIDs = self.driver.find_elements_by_xpath("//*[@id]")
                    qItems = len(tmpDictWithIDs)
                    dbg("cantidad de items: %d" % qItems)
                    for i, el in enumerate(tmpDictWithIDs,1):
                    #for el in self.driver.find_elements_by_xpath("//*[@id]"):
                        #self.pbCache.setValue(i)
                        #self.pbCache.setFormat('LOADING ... %d%s' % (i, "%"))

                        tagName, tagID = ( el.tag_name, el.get_attribute("id"),)                        

                        if tagName in self.tagNameWithValueOrText2:
                            if tagName.lower() != self.unsuscriptableTags:
                                with open("debug2.txt", "a") as f:
                                    f.write("item actual: %d - tagName: [%s] - tagID: [%s] - tagValue: [%s] \r\n" % (i, tagName, tagID, eval("el.%s" % self.tagNameWithValueOrText2[tagName])))
                                    f.write(os.linesep)
                                dbg("item actual: %d - tagName: [%s] - tagID: [%s] - tagValue: [%s]" % (i, tagName, tagID, eval("el.%s" % self.tagNameWithValueOrText2[tagName])))
                                self.elementsWithID[tagID] = [tagName, eval("el.%s" % self.tagNameWithValueOrText2[tagName])] #"""
                    print("end cache")

                except Exception as e:
                    dbg(str(e))        
                print("###########################################################")
                print("same level")
                print("###########################################################")
        time.sleep(1000)

    def goToPage(self, urlPage):
        self.driver.get(urlPage)
        self.setWindowTitle("%s - %s" % (self.title, self.driver.title))

        self.pendingProcess = True

        #t1 = threading.Thread(target=self.setIDSInCache)
        #t1.setDaemon(True)
        #t1.start()
        #self.driver.set_window_rect(0,0,800,600)
        self.moveToCorner()
        return True

    def addLogToBox(self, log):
        self.lsbxLog.addItem(log)

    def startBOT(self):
        if self.rbtnFirefox.isChecked():
            self.driverType = "Firefox"
            self.driver = webdriver.Firefox()
        elif self.rbtnChrome.isChecked():
            self.driverType = "Chrome"
            self.driver = webdriver.Chrome()
        else:
            self.driverType = "IE"
            self.driver = webdriver.Ie()

        self.addLogToBox('BOT is ready!!!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #debug = True
    #debug = False
    if not debug:

        #QtCore.QObject.connect(app, SIGNAL("focusChanged(QWidget *, QWidget *)"), changedFocusSlot)

        splashImg = QPixmap(":/img/img/pyBOT-splash.png")
        splash = QSplashScreen(splashImg, QtCore.Qt.WindowStaysOnTopHint)
        splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        splash.setEnabled(False)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/pyBOT.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        splash.setWindowIcon(icon)

        progressBar = QProgressBar(splash)
        progressBar.setMaximum(10)
        progressBar.setAlignment(QtCore.Qt.AlignCenter)
        progressBar.setGeometry(0, splashImg.height()-30, splashImg.width() - 27, 30 )
        #splash.setMask(splashImg.mask())
        splash.show()
        #splash.showMessage("<h1><font color='green'>I'm pyBOT!!!</font></h1>", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)

        for i in range(1, 11):
            progressBar.setValue(i)
            percent = int(progressBar.value()) * 10
            progressBar.setFormat('LOADING ... %d%s' % (percent, "%"))

            t = time.time()
            while time.time() < t + 0.1:
                app.processEvents()

        time.sleep(1)
    form = pyBOT(None)
    form.show()
    if not debug:
        splash.finish(form)
    app.exec_()


"""
mainWindow = QtGui.QWidget()
screenShape = QtGui.QDesktopWidget().screenGeometry()
mainWindow.resize(self.screenShape.width(), self.screenShape.height())
"""
