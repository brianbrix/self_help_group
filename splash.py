
from multiprocessing import Pool

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot, QEventLoop
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QDialog, QTextBrowser, QSplashScreen, QApplication


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.setWindowTitle('Just a dialog')

class MySplashScreen(QSplashScreen):
    def __init__(self, animation, flags):
        # run event dispatching in another thread
        QSplashScreen.__init__(self, QPixmap(), flags)
        self.movie = QMovie(animation)
        self.movie.frameChanged.connect(self.onNextFrame)
        self.movie.start()

    @pyqtSlot()
    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

# Put your initialization code here
def longInitialization(arg):
    time.sleep(arg)
    return 0
if __name__ == "__main__":
    import sys, time

    app = QApplication(sys.argv)

    # Create and display the splash screen
#   splash_pix = QPixmap('a.gif')
    splash = MySplashScreen("images/giphy2.gif", Qt.Qt.WindowStaysOnTopHint)
#   splash.setMask(splash_pix.mask())
    #splash.raise_()
    splash.show()
    app.processEvents()

    # this event loop is needed for dispatching of Qt events
    initLoop = QEventLoop()
    pool = Pool(processes=1)
    pool.apply_async(longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
    initLoop.exec_()

    form = Form()
    form.show()
    splash.finish(form)
    app.exec_()