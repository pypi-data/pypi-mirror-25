from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from .a_XLogDialog import XLogDialog
from .a_XLogMainWindow import XLogMainWindow
from .a_WBase import *
import os


__all__ = ["WEditor"]


class WEditor(WBase):
    """Base class for editor widgets"""

    @property
    def f(self):
        # DataFile instance
        return self._f

    @property
    def flag_valid(self):
        return self._flag_valid

    # Emitted by load()
    loaded = pyqtSignal()

    def __init__(self, *args, **kwargs):
        WBase.__init__(self, *args, **kwargs)

        # Datafile instance
        self._f = None

        self._flag_valid = True

    def load(self, fobj):
        self._do_load(fobj)
        self.update_gui_label_fn()
        self.loaded.emit()

    def update_gui_label_fn(self):
        if hasattr(self, "label_fn"):
            self.label_fn.setText(self._make_fn_text())

    def _make_fn_text(self):
        """Makes filename text"""
        if not self._f:
            text = "(not loaded)"
        elif self._f.filename:
            text = os.path.relpath(self._f.filename, ".")
        else:
            text = "(filename not set)"
        return text

    def _do_load(self, fobj):
        raise NotImplementedError("Please implement {}._do_load()".format(self.__class__.__name__))