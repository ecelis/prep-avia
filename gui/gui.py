##
##     AViA Prep - Ingest and tagging of A/V media assets
##     Copyright (C) 2016 Ernesto Angel Celis de la Fuente
##                          <developer@celisdelafuente.net>
##
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
##
##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import sys
import qdarkstyle
from txt import txt
import ico
from PyQt4 import Qt, QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def _setGuiTheme(self, theme = 'dark'):
    """Sets PatitoPro GUI visual style"""
    if theme != 'dark':
        pass
    else:
        self.setStyleSheet(qdarkstyle.load_stylesheet(pyside = False))

def _baseLayout(self):
    self.baseLayout = QtGui.QHBoxLayout()
    self.baseLayout.setObjectName(_fromUtf8("baseLayout"))

def _explorerLayout(self):
    self.explorerLayout = QtGui.QVBoxLayout()
    self.explorerLayout.setObjectName(_fromUtf8("explorerLayout"))
    ## File browser
    self.fileBrowserView = QtGui.QTreeWidget(self.explorerContents)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            self.fileBrowserView.sizePolicy().hasHeightForWidth())
    self.fileBrowserView.setSizePolicy(sizePolicy)
    self.fileBrowserView.setObjectName(_fromUtf8("fileBrowserView"))


    ## Clipas
    self.projectClips = QtGui.QTableWidget(self.explorerContents)
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            self.projectClips.sizePolicy().hasHeightForWidth())
    self.projectClips.setSizePolicy(sizePolicy)
#    self.projectClips.setWidgetResizable(True)
    self.projectClips.setObjectName(_fromUtf8("projectClips"))
    self.explorerLayout.addWidget(self.projectClips)


def _initGui(self):
    """Initialize PatitoPro GUI"""
    _setGuiTheme(self)
    self.setWindowTitle(_fromUtf8(txt.APP_TITLE))
    self.setWindowIcon(QtGui.QIcon(ico.PPP))
    _baseLayout(self)

def _setFont(self, target, style):
    pass

def _getVideoWidget():
    """In this widget, the video will be drawn"""
    videoframe = None
    if sys.platform == "darwin": # for MacOS
        videoframe = QtGui.QMacCocoaViewContainer(0)
    else:
        videoframe = QtGui.QFrame()

    palette = videoframe.palette()
    palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
    videoframe.setPalette(palette)
    videoframe.setAutoFillBackground(True)

    return videoframe

def _getTimeLine():
    if sys.platform == "darwin":
        timeline = QtGui.QMacCocoaViewContainer(0)
    else:
        timeline = QtGui.QScrollArea()
        timeline.setFrameStyle(QtGui.QFrame.StyledPanel)
        timeline.setFrameStyle(QtGui.QFrame.Sunken)
        timeline.setGeometry(QtCore.QRect(0,0,200,200))

    return timeline

def _getSliderWidget(self, options):
    """Returns a slider"""
    slider = QtGui.QSlider(options['orientation'], self)
    slider.setToolTip(options['tooltip'])
    slider.setMaximum(options['max'])
    return slider

def _getButton(options):
    button = QtGui.QPushButton(options['label'])
    button.resize(button.minimumSizeHint())
    return button
