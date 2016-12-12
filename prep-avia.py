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
import os.path
from vlc import vlc
from PyQt4 import Qt, QtGui, QtCore
import qdarkstyle
from txt import txt
from gui import ico, short

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

class MainWindow(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        super(MainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self, master)
        self._setGuiTheme()
        #self._setFont()
        self.setWindowTitle(_fromUtf8(txt.APP_TITLE))
        self.setWindowIcon(QtGui.QIcon(ico.PPP))
        # creating a basic vlc instansce
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.createUI()
        self.isPaused = False

    def _setGuiTheme(self, theme = 'dark'):
        """Sets PatitoPro GUI visual style"""
        if theme != 'dark':
            pass
        else:
            self.setStyleSheet(qdarkstyle.load_stylesheet(pyside = False))

    def _setFont(self, target, style):
        pass

    def _baseLayout(self):
        self.baseLayout = QtGui.QHBoxLayout()
        self.baseLayout.setObjectName(_fromUtf8("baseLayout"))

    def _getVideoWidget(self):
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

    def _getButton(self, options):
        button = QtGui.QPushButton(options['label'])
        button.resize(button.minimumSizeHint())
        return button

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.videoframe = self._getVideoWidget()
        self.menu()
        self.toolBar()
        self.statusBar()
        self.vlcp()
        self.explorerWidget()
        self.propertiesWidget()
        self.setCentralWidget(self.vlcplayer)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def menu(self):
        self.open = QtGui.QAction(QtGui.QIcon(ico.OPEN_PROJECT),
                _fromUtf8(txt.OPEN_PROJECT), self)
        self.open.setShortcut(short.OPEN_PROJECT)
        self.connect(self.open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction(txt.MENU_EXIT, self)
        exit.setShortcut(short.QUIT)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu(txt.MENU_OPEN_PROJECT)
        filemenu.addAction(self.open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

    def toolBar(self):
        self.toolbar = self.addToolBar(_fromUtf8(txt.OPEN_PROJECT))
        self.toolbar.addAction(self.open)

    def statusBar(self):
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

    def explorerWidget(self):
        """File and project explorer dock panel"""
        self.explorer = QtGui.QDockWidget(self)
        self.explorer.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.explorer.setObjectName(_fromUtf8("explorer"))
        self.explorerContent = QtGui.QWidget()
        self.explorerContent.setObjectName(
                _fromUtf8("explorerContents"))
        self.explorer.setWidget(self.explorerContent)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1),
                self.explorer)
        # Explorer Layout
        self.explorerLayout = QtGui.QVBoxLayout()
        self.explorerLayout.setObjectName(_fromUtf8("explorerLayout"))
        ## File browser
        self.fileBrowserView = QtGui.QTreeView(self.explorerContent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                self.fileBrowserView.sizePolicy().hasHeightForWidth())
        self.fileBrowserView.setSizePolicy(sizePolicy)
        self.fileBrowserView.setObjectName(_fromUtf8("fileBrowserView"))
        model = QtGui.QFileSystemModel(self.fileBrowserView)
        model.setRootPath(QtCore.QDir.currentPath())
        self.fileBrowserView.setModel(model)
        ## Clips
        self.projectClips = QtGui.QTableWidget(self.explorerContent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                self.projectClips.sizePolicy().hasHeightForWidth())
        self.projectClips.setSizePolicy(sizePolicy)
        ##self.projectClips.setWidgetResizable(True)
        self.projectClips.setObjectName(_fromUtf8("projectClips"))

    def propertiesWidget(self):
        self.properties = QtGui.QDockWidget(self)
        self.properties.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.properties.setObjectName(_fromUtf8("PropertiesWidget"))
        self.propertiesContent = QtGui.QWidget()
        self.propertiesContent.setObjectName(_fromUtf8("propertiesContent"))
        self.properties.setWidget(self.propertiesContent)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2),
                self.properties)

    def vlcp(self):
        """Create the main vlc player widget"""
        self.vlcplayer = QtGui.QWidget(self)
        # Player Controls
        ps_config = dict(orientation = QtCore.Qt.Horizontal,
                tooltip = 'Position', max = 1000)
        self.positionslider = self._getSliderWidget(ps_config)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.playbutton = self._getButton({'label':_fromUtf8(txt.PLAY)})
        self.stopbutton = self._getButton({"label":_fromUtf8(txt.STOP)})

        self.vlc_controls = QtGui.QHBoxLayout()
        self.vlc_controls.addWidget(self.playbutton)
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)
        self.vlc_controls.addWidget(self.stopbutton)
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)

        self.vlc_controls.addStretch(1)
        self.volumeslider = self._getSliderWidget(
                {'orientation':QtCore.Qt.Horizontal,
                'tooltip':'Volume',
                'max':100})
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.vlc_controls.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        # TODO self.timeline = gui._getTimeLine()
        self.vlc_layout = QtGui.QVBoxLayout()
        self.vlc_layout.addWidget(self.videoframe)
        self.vlc_layout.addWidget(self.positionslider)
        self.vlc_layout.addLayout(self.vlc_controls)
        #self.vlc_layout.addWidget(self.timeline)
        self.vlcplayer.setLayout(self.vlc_layout)


    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText(_fromUtf8(txt.PLAY))
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText(_fromUtf8(txt.PAUSE))
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText(_fromUtf8(txt.PLAY))

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self,
                    "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ppp = MainWindow()
    ppp.show()
    ppp.resize(640, 480)
    if sys.argv[1:]:
        ppp.OpenFile(sys.argv[1])
    sys.exit(app.exec_())
