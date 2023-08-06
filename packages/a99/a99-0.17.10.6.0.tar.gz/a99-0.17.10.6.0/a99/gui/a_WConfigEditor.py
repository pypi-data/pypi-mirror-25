from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from .a_XLogDialog import XLogDialog
from .a_XLogMainWindow import XLogMainWindow
from .a_WEditor import *
from . import xmisc
import os
import traceback


# Margin for main layout
EDITOR_LAYMN_MAIN = 9
# Spacing for main layout
EDITOR_LAYSP_MAIN = 9

__all__ = ["WConfigEditor", "EDITOR_LAYMN_MAIN", "EDITOR_LAYSP_MAIN", "CEMapItem"]



# # https://stackoverflow.com/questions/3681272/can-i-get-a-reference-to-a-python-property
# def _get_dict_attr(obj, attr):
#     """I used this to get a property object from an object, not the property value"""
#     for obj in [obj] + obj.__class__.mro():
#         if attr in obj.__dict__:
#             return obj.__dict__[attr]
#     raise AttributeError
#
# # Short because it is going to be called many times
# GDA = _get_dict_attr()



class CEMapItem(object):
    """Config Editor map item

    There to way to get-set values. The order of precedence is as follows:

        (getter, setter) > (guiobj, propertyname)
    """

    def __init__(self, fieldname, guiobj, propertyname=None, getter=None, setter=None):
        self.fieldname = fieldname
        # GUI object that has property called propertyname or getter-setter methods
        self.guiobj = guiobj
        self.propertyname = propertyname if propertyname is not None else fieldname
        self.getter = getter
        self.setter = setter

    def get_value(self):
        if self.getter:
            return self.getter()
        return self.guiobj.__getattribute__(self.propertyname)

    def set_value(self, value):
        if self.setter:
            self.setter(value)
        else:
            self.guiobj.__setattr__(self.propertyname, value)



class WConfigEditor(WEditor):
    """Base class for FileConfig editors"""

    def __init__(self, *args, **kwargs):
        WEditor.__init__(self, *args, **kwargs)
        
        # To prevent recursive GUI updating by triggered signals
        self._flag_updating_gui = False

        # [(fieldname, read-write property object), ...]
        self._map = []

    def _do_load(self, fobj):
        self._f = fobj
        self._update_gui()
        self._flag_valid = True
        self.setEnabled(True)

    def _update_gui(self):
        "Updates GUI from fobj. Opposite of _update_fobj()"
        if self._flag_updating_gui:
            return

        self._flag_updating_gui = True

        try:
            for item in self._map:
                value = self._f.obj[item.fieldname]
                item.set_value(value)

        finally:
            self._flag_updating_gui = False

    def _update_fobj(self):

        """Updates fobj from GUI. Opposite of _update_gui()"""

        # print("PPPPPPPPPPPPPPPPPPPRINTANDO O STACK")
        # traceback.print_stack()

        emsg, flag_error = "", False
        fieldname = None
        try:
            for item in self._map:
                fieldname = item.fieldname
                value = item.get_value()
                self._f.obj[fieldname] = value

        except Exception as E:
            flag_error = True
            if fieldname is not None:
                emsg = "Field '{}': {}".format(fieldname, str(E))
            else:
                emsg = str(E)
            self.add_log_error(emsg)

        self._flag_valid = not flag_error
        if not flag_error:
            self.status("")

