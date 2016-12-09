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

import qdarkstyle
import txt, ico
from PyQt4 import Qt, QtGui, QtCore

def _setGuiTheme(self, theme = 'dark'):
    """Sets PatitoPro GUI visual style"""
    if theme != 'dark':
        pass
    else:
        self.setStyleSheet(qdarkstyle.load_stylesheet(pyside = False))

def _initGui(self):
    """Initialize PatitoPro GUI"""
    _setGuiTheme(self)
    self.setWindowTitle(txt.APP_TITLE)
    self.setWindowIcon(QtGui.QIcon(ico.PPP))
