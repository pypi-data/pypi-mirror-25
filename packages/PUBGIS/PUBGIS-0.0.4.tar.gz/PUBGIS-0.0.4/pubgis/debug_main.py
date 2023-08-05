import logging
import sys

from PyQt5.QtWidgets import QApplication

from pubgis.gui import PUBGISMainWindow

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(relativeCreated)6d %(threadName)s %(message)s')
    APP = QApplication(sys.argv)
    WIN = PUBGISMainWindow()
    sys.exit(APP.exec_())
