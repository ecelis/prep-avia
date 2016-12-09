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
from vendor import vlc
from PyQt4 import Qt, QtGui, QtCore

import txt
import ico
import gui

class PPPMainWindow(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        super(PPPMainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self, master)
        gui._initGui(self)
        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        
        self.createUI()
        self.isPaused = False

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        #self.propertiesPanel = QtGui.QDockWidget(self)
        #self.setCentralWidget(self.vlcplayer)
        #self.setCentralWidget(self.vlcplayer)
        # Get the main video frame
        self.videoframe = gui._getVideoWidget()
        self.vlcp()
        self.menu()
        self.toolBar()
        self.statusBar()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)


        #self.horizontalLayout_2.addLayout(self.baseLayout)
        #MainWindow.setCentralWidget(self.centralwidget)

    def menu(self):
        self.open = QtGui.QAction(QtGui.QIcon(ico.OPEN_PROJECT),
                txt.OPEN_PROJECT, self)
        self.open.setShortcut("Ctrl+O")
        self.connect(self.open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        exit.setShortcut("Ctrl+Q")
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(self.open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

    def toolBar(self):
        self.toolbar = self.addToolBar(txt.OPEN_PROJECT)
        self.toolbar.addAction(self.open)

    def statusBar(self):
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def explorerWidget(self):
        """File and project explorer dock panel"""
        self.ExplorerWidget = QtGui.QDockWidget(self)
        self.ExplorerWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.ExplorerWidget.setObjectName("ExplorerWidget")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.ExplorerWidget.setWidget(self.dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1),
                self.ExplorerWidget)

    def vlcp(self):
        """Create the main vlc player widget"""
        self.vlcplayer = QtGui.QWidget(self)
        # Player Controls
        ps_config = dict(orientation = QtCore.Qt.Horizontal,
                tooltip = 'Position', max = 1000)
        self.positionslider = gui._getSliderWidget(self, ps_config)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.playbutton = gui._getButton({'label':txt.PLAY})
        self.stopbutton = gui._getButton({"label":txt.STOP})

        self.vlc_controls = QtGui.QHBoxLayout()
        self.vlc_controls.addWidget(self.playbutton)
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)
        self.vlc_controls.addWidget(self.stopbutton)
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)

        self.vlc_controls.addStretch(1)
        self.volumeslider = gui._getSliderWidget(self,
                {'orientation':QtCore.Qt.Horizontal,
                'tooltip':'Volume',
                'max':100})
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.vlc_controls.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vlc_layout = QtGui.QVBoxLayout()
        self.vlc_layout.addWidget(self.videoframe)
        self.vlc_layout.addWidget(self.positionslider)
        self.vlc_layout.addLayout(self.vlc_controls)

        self.vlcplayer.setLayout(self.vlc_layout)


    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

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
    ppp = PPPMainWindow()
    ppp.show()
    ppp.resize(640, 480)
    if sys.argv[1:]:
        ppp.OpenFile(sys.argv[1])
    sys.exit(app.exec_())
