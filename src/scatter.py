# import logging
import random
from PySide2 import QtWidgets, QtCore
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
    # create the


# CLASS: create logic for program

# variable to store user-input of shape to scatter (scatter-object).

# scatter_object = QLineEdit.displayText()

# variable to store verts/object that user selects (scatter-to)

# Loop code -- Allows scatter-object to scatter to selected verts only.
selection = cmds.ls(orderedSelection=True, flatten=True)

for obj in selection:
    if 'vtx[' not in obj:
        selection.remove(obj)

# --Selecting locations for scatter-object to scatter to
selection = cmds.ls(orderedSelection=True, flatten=True)
# lines 38-9 select all verts on an object:
vtx_selection = cmds.polyListComponentConversion(selection, toVertex=True)
vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31, expand=True)
# line 40 selects or re-selects the vertices previously selected
cmds.select(vtx_selection)

# -- selecting scale for scatter-object instances - how many variables?
scale_min = user_input
scale_max = user_input

# scale variables
size_x = random.uniform(1.0, 5.5)
size_y = random.uniform(1.0, 5.5)
size_z = random.uniform(1.0, 5.5)


# -- selecting rotation for scatter-object instances
# rotate_min_X = user_input
# rotate_max_X = user_input

# rotate variables
# rotate_x = random.uniform(1.0, 5.5)
# rotate_y = random.uniform(1.0, 5.5)
# rotate_z = random.uniform(1.0, 5.5)

# code that groups the instances
    # empty list so instances can be grouped
    scattered_instances = []
    # this for loop creates instances, stores in list
    for vtx in vtx_selection:
        # change pCube1 to soft-coded variable - scatter_object
        scatter_instance = cmds.instance("pCube1", name="instance1")
        scattered_instances.extend(scatter_instance)
        # this code should include rotate and scale as well VV
        pos = cmds.xform([vtx], query=True, translation=True)
        cmds.xform(scatter_instance, translation=pos, scale=
        [size_x, size_y, size_z])
    # group the instances -- arguments = list and a name for the list
    cmds.group(scattered_instances, name = "scattered")

