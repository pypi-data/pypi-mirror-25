#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication

from logging import getLogger, INFO, StreamHandler, Formatter

lg = getLogger('sleepytimes')
FORMAT = '%(asctime)s %(filename)s/%(funcName)s (%(levelname)s): %(message)s'
DATE_FORMAT = '%H:%M:%S'

formatter = Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)
handler = StreamHandler()
handler.setFormatter(formatter)

lg.handlers = []
lg.addHandler(handler)

lg.setLevel(INFO)

from os.path import abspath, dirname, join
from types import MethodType

from numpy import arange
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from .widgets.creation import (create_menubar, create_toolbar,
                               create_actions, create_widgets)
from .widgets.settings import DEFAULTS
from .widgets.utils import keep_recent_datasets

settings = QSettings("JOB", "sleepytimes")
here = abspath(dirname(__file__))
with open(join(here, 'VERSION')) as f:
    VERSION = f.read()


class MainWindow(QMainWindow):
    """Create an instance of the main window.

    """
    def __init__(self):
        super().__init__()

        self.info = None
        self.channels = None
        self.spectrum = None
        self.overview = None
        self.notes = None
        self.video = None
        self.traces = None
        self.settings = None
        self.spindle_dialog = None

        self.action = {}  # actions was already taken
        self.menu_window = None

        # I prefer to have these functions in a separate module, for clarify
        self.create_widgets = MethodType(create_widgets, self)
        self.create_actions = MethodType(create_actions, self)
        self.create_menubar = MethodType(create_menubar, self)
        self.create_toolbar = MethodType(create_toolbar, self)

        self.create_widgets()
        self.create_actions()
        self.create_menubar()
        self.create_toolbar()

        self.statusBar()
        self.setWindowTitle('Sleepytimes v' + VERSION)

        window_geometry = settings.value('window/geometry')
        if window_geometry is not None:
            self.restoreGeometry(window_geometry)
        window_state = settings.value('window/state')
        if window_state is not None:
            self.restoreState(window_state, float(VERSION[:3]))

        self.show()
        """
        #JOB working file
        self.info.open_dataset(
                debug_filename='/Users/jonobe/Documents/00_recs/rec/test_01_EEG.edf')
        self.channels.load_channels(
                debug_filename='/Users/jonobe/Documents/00_recs/rec/newtest_channels.json')
        self.notes.update_notes(
                '/Users/jonobe/Documents/00_recs/rec/newtest_scores.xml')
        """
    def update(self):
        """Functions to re-run once settings have been changed."""
        self.create_menubar()

    def value(self, parameter, new_value=None):
        """This function is a shortcut for any parameter. Instead of calling
        the widget, its config and its values, you can call directly the
        parameter.

        Parameters
        ----------
        parameter : str
            name of the parameter of interest
        new_value : str or float, optional
            new value for the parameter

        Returns
        -------
        str or float
            if you didn't specify new_value, it returns the current value.

        Notes
        -----
        It's important to maintain an organized dict in DEFAULTS which has to
        correspond to the values in the widgets, also the name of the widget.
        DEFAULTS is used like a look-up table.
        """
        for widget_name, values in DEFAULTS.items():
            if parameter in values.keys():
                widget = getattr(self, widget_name)
                if new_value is None:
                    return widget.config.value[parameter]
                else:
                    lg.debug('setting value {0} of {1} to {2}'
                             ''.format(parameter, widget_name, new_value))
                    widget.config.value[parameter] = new_value

    def reset(self):
        """Remove all the information from previous dataset before loading a
        new dataset."""

        # store current dataset
        max_dataset_history = self.value('max_dataset_history')
        keep_recent_datasets(max_dataset_history, self.info)

        # reset all the widgets
        self.channels.reset()
        self.info.reset()
        self.notes.reset()
        self.overview.reset()
        self.spectrum.reset()
        self.traces.reset()

    def show_settings(self):
        """Open the Setting windows, after updating the values in GUI. """
        self.notes.config.put_values()
        self.overview.config.put_values()
        self.settings.config.put_values()
        self.spectrum.config.put_values()
        self.traces.config.put_values()
        self.video.config.put_values()

        self.settings.show()

    def show_merge_dialog(self):
        """Create the event merging dialog."""
        self.merge_dialog.update_event_types()
        self.merge_dialog.show()
            
    def show_spindle_dialog(self):
        """Create the spindle detection dialog."""
        self.spindle_dialog.update_groups()
        self.spindle_dialog.show()
        
    def show_slow_wave_dialog(self):
        """Create the SW detection dialog."""
        self.slow_wave_dialog.update_groups()
        self.slow_wave_dialog.show()        

    def show_event_analysis_dialog(self):
        """Create the event analysis dialog."""
        self.event_analysis_dialog.update_types()
        self.event_analysis_dialog.update_groups()
        self.event_analysis_dialog.update_cycles()
        self.event_analysis_dialog.show()
        
    def show_spindle_help(self):
        self.spindle_help.show()
        
    def show_slowwave_help(self):
        self.slowwave_help.show()
        
    def show_evt_analysis_help(self):
        self.evt_analysis_help.show()

    def about(self):
        s = ('<b>PHYPNO Version {version}</b><br />'
             '<p>You can download the latest version at '
             '<a href="https://github.com/gpiantoni/phypno">'
             'https://github.com/gpiantoni/phypno</a> '
             'or you can upgrade to the latest release with:'
             '</p><p>'
             '<code>pip install --upgrade phypno</code>'
             '</p><p>'
             'Copyright &copy; 2013-2016 '
             '<a href="http://www.gpiantoni.com">Gio Piantoni</a>'
             '</p><p>'
             'With contributions from Jordan O\'Byrne'
             '</p>')
        t = ('<b>SLEEPYTIMES Version {version}</b><br />'
             'Copyright &copy; 2013-2016 '
             '<a href="http://www.gpiantoni.com">Gio Piantoni</a><br />'
             'Copyright &copy; 2017 '
             'Jordan O\'Byrne'
             '<p> This is a collaborative work, first built by GP as PHYPNO, '
             'then forked, modified and renamed by JOB.</p>'
             '<p>You can download the latest version of PHYPNO at '
             '<a href="https://github.com/gpiantoni/phypno">'
             'https://github.com/gpiantoni/phypno</a>.')
        u = ('<p>'
             'This program is free software: you can redistribute it '
             'and/or modify it under the terms of the GNU General Public '
             'License as published by the Free Software Foundation, either '
             'version 3 of the License, or (at your option) any later version.'
             '</p><p>'
             'This program is distributed in the hope that it will be useful, '
             'but WITHOUT ANY WARRANTY; without even the implied warranty of '
             'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the '
             'GNU General Public License for more details.'
             '</p><p>'
             'You should have received a copy of the GNU General Public '
             'License along with this program.  If not, see '
             '<a href="http://www.gnu.org/licenses/">'
             'http://www.gnu.org/licenses/</a>.'
             '</p><p>'
             'Other licenses available, contact the author.'
             '</p>')
        QMessageBox.about(self, 'SLEEPYTIMES', 
                          t.format(version=VERSION) + u)

    def closeEvent(self, event):
        """save the name of the last open dataset."""
        max_dataset_history = self.value('max_dataset_history')
        keep_recent_datasets(max_dataset_history, self.info)

        settings.setValue('window/geometry', self.saveGeometry())
        settings.setValue('window/state', self.saveState(float(VERSION[:3])))

        event.accept()


app = None


def main():
    global app
    app = QApplication([])

    q = MainWindow()
    q.show()

    app.exec_()
