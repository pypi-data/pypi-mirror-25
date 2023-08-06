from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSplashScreen, QProgressBar, QFileDialog, QAction, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
import sys, time, datetime
import threading
import psutil
import pandas as pd
import syntax

from utils import PandasModel

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo



cnx = pymongo.MongoClient()
db = cnx["selenium"]
scripts = db["scripts"]

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
    tagNameWithValueOrText2 = {'div':'text', 'span':'text', 'a':'text', 'li':'text', 'input':'get_attribute("value")', 'textarea':'get_attribute("value")'}
    goNavigateShortcuts = {'google':'https://www.google.com.pe', 'facebook':'https://www.facebook.com', 'elcomercio':'http://elcomercio.pe', 'sisact':'http://intranetsisact/sisact/Index.aspx', 'siacpost':'http://intranetsiacpost/siacpost-frontend'}

    def __init__(self, mixin_arg, **kwds):
        super().__init__(**kwds)
        self.setupUi(self)
        self.setWindowFlags( QtCore.Qt.Window |
                    QtCore.Qt.CustomizeWindowHint |
                    QtCore.Qt.WindowStaysOnTopHint |
                    #QtCore.Qt.WindowMinimizeButtonHint |
                    #QtCore.Qt.WindowCloseButtonHint |
                    QtCore.Qt.WindowTitleHint)
        self.title =  self.windowTitle()
        self.resize(604,370)
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

        #self.btnOpenScript.addAction(self.openFile)

        self.__bind__()
        #self.tabWidget.setStyleSheet("padding-bottom:50px; background-color:red;")
        #self.tabBOT.setStyleSheet("padding-bottom:50px; background-color:red;")
        #self.tabTASKS.setStyleSheet("padding-bottom:50px; background-color:red;")
        #self.debugInit()
    @QtCore.pyqtSlot()
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

    #self.txtScript.viewportEvent.connect(self.copy_the_text)
    def copy_the_text(self, event):
        if isinstance(event, QtGui.QKeyEvent):  # as viewportEvent gets *all* events
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                pass

    def XkeyPressEvent(self, ev):
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
        self.tblScripts.doubleClicked.connect(self.tblScriptsGetSelectedData)
        #self.txtScript.keyPressEvent(self.mbox)
        #self.txtScript.keyPressEvent.connect(self.txtScriptKeypressEvent)
        #self.txtScript.installEventFilter(self.txtScriptKeypressEvent)
        #self.txtScript.installEventFilter(self.keyPressEvent)
        #self.txtScript.keyPressEvent.connect(self.keyPressEvent)
        #self.connect(self.txtScript, SIGNAL("keyPressEvent(event)"), self.keyPressEvent)

    def runScript(self):
        strToCompile = self.txtScript.toPlainText()
        compiled = compile(strToCompile, "<string>", "exec")
        exec(compiled)

    def tblScriptsGetSelectedData(self):
        index = self.tblScripts.selectedIndexes()[0]
        scriptData = str(self.tblScripts.model().data(index))
        #self.txtScript.clear()
        #self.txtScript.insertPlainText(scriptData)
        self.txtScript.setPlainText(scriptData)
        self.txtScript.setReadOnly(True)
        self.txtScript.setStyleSheet("background-color:#C5FDD6;")
        self.pnlScriptsData.hide()

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
        self.manageProcess()
        slug = ""
        for i in self.elementsWithID:
            print(str(i))
            slug += str(i)
        self.mbox(slug)

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
        reply = QMessageBox.question(self, 'Message', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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

    def setIDSInCache(self):
        print("init cache")
        for el in self.driver.find_elements_by_xpath("//*[@id]"):
            tagName, tagID = ( el.tag_name, el.get_attribute("id"),)
            if tagName in self.tagNameWithValueOrText2:
                self.elementsWithID[tagID] = [tagName, eval("el.%s" % self.tagNameWithValueOrText2[tagName])]
        print("end cache")




    def goToPage(self, urlPage):
        self.driver.get(urlPage)
        self.setWindowTitle("%s - %s" % (self.title, self.driver.title))
        t1 = threading.Thread(target=self.setIDSInCache)
        t1.setDaemon(True)
        t1.start()
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
    splashImg = QPixmap("img/BeBOT-splash.png")
    splash = QSplashScreen(splashImg, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)

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
    #form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    form.show()
    splash.finish(form)
    app.exec_()
"""
http://blog.pythonisito.com/2012/05/gridfs-mongodb-filesystem.html
http://api.mongodb.com/python/current/examples/gridfs.html
https://api.mongodb.com/python/1.8/examples/gridfs.html
https://stackoverflow.com/questions/7719466/how-to-convert-a-string-to-a-function-in-python
http://lybniz2.sourceforge.net/safeeval.html

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        startQuiz = QAction("Start Quiz", self)
        startQuiz.triggered.connect(self.startQuizQuestions)

        menubar = self.menuBar()
        quizMenu = menubar.addMenu("&Quiz")
        quizMenu.addAction(startQuiz)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("xyz")
        self.show()

    def startQuizQuestions(self):
        newQuiz = Quiz()
        self.setCentralWidget(newQuiz)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
"""
