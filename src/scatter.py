# import logging
import random
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

# log = logging.getLogger(__name__)

# make sure the window appears above the maya window
def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

# CLASS: create the GUI
class ScatterUI(QtWidgets.QDialog):
    """ Smart Save UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter")
        # The pixel settings are adjusted for my computer resolution
        self.setMinimumWidth(750)
        self.setMaximumHeight(350)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        # load the logic class here
        self.create_ui()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 35px")
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.setLayout(self.main_lay)


# CLASS: create logic for program
class Scatter(object):
    """Representation of a Scatter program"""

    #the init has the defaults
    def __init__(self):
        self.r_min_x = 0
        self.r_max_x = 360
        self.r_min_y = 0
        self.r_max_y = 360
        self.r_min_z = 0
        self.r_max_z = 360

    #def __init__(self):
    # variable to store user-input of shape to scatter (scatter-object).

    # scatter_object = QLineEdit.displayText()

    # variable to store verts/object that user selects (scatter-to)

    # Loop code -- Allows scatter-object to scatter to selected verts only.
    # selection = cmds.ls(orderedSelection=True, flatten=True)

    # for obj in selection:
        # if 'vtx[' not in obj:
            # selection.remove(obj)

    # --Selecting locations for scatter-object to scatter to
    selection = cmds.ls(orderedSelection=True, flatten=True)
    # lines 38-9 select all verts on an object:
    vtx_selection = cmds.polyListComponentConversion(selection, toVertex=True)
    vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31,
                                      expand=True)
    # line 40 selects or re-selects the vertices previously selected
    cmds.select(vtx_selection)

    # -- selecting scale for scatter-object instances - how many variables?
    # scale_min = user_input
    # scale_max = user_input

    # scale variables
    size_x = random.uniform(1.0, 5.5)
    size_y = random.uniform(1.0, 5.5)
    size_z = random.uniform(1.0, 5.5)


    # -- selecting rotation for scatter-object instances
    # ro_min_X = user_input
    # ro_max_X = user_input
    # ro_min_Y = user_input
    # ro_max_Y = user_input
    # ro_min_Z = user_input
    # ro_max_Z = user_input

    # rotate variables - replace hard-coded with user-input variables
    rotate_x = random.uniform(0, 360)
    rotate_y = random.uniform(0, 360)
    rotate_z = random.uniform(0, 360)

    # code that groups the instances
    # empty list so instances can be grouped
    scattered_instances = []
    # this for loop creates instances, stores in list
    for vtx in vtx_selection:
        # change pCube1 to soft-coded variable - scatter_object
        # I think "instance#" is causing problems--# is special python
        scatter_instance = cmds.instance("pCube1", name="instance#")
        scattered_instances.extend(scatter_instance)
        pos = cmds.xform([vtx], query=True, translation=True, worldSpace=True)
        cmds.xform(scatter_instance, translation=pos,
                   rotation=[rotate_x, rotate_y, rotate_z],
                   scale=[size_x, size_y, size_z])
    # group the instances -- arguments = list and a name for the list
    cmds.group(scattered_instances, name="scattered")
