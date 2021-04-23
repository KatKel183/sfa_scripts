# import logging
import random
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

# log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.scatter = Scatter()
        self.setWindowTitle("Scatter Tool")
        # The pixel settings are adjusted for my computer resolution
        self.setMinimumWidth(750)
        self.setMaximumHeight(350)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatter = Scatter()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        # vertical box layout
        self.main_layout = QtWidgets.QVBoxLayout
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        # title for the box
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 35px")
        # scatter button
        self.main_layout.addWidget(self.scatter_btn)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter)

    @QtCore.Slot()
    def scatter(self):
        self.scatter = Scatter()
        self._set_values_from_ui()
        self.scatter.create_instances()

    def _set_values_from_ui(self):
        self.scatter_slot.rotation_min[1] = self.rotation_y_min_dsbx.value()
        self.scatter_slot.rotation_max[1] = self.rotation_y_max_dsbx.value()



class Scatter(object):
    """Representation of a Scatter program"""

    # the init has the defaults
    def __init__(self):
        self.rotation_min = [0, 0, 0]
        self.rotation_max = [360, 360, 360]

    def vert_selection(self):
        # --Selecting locations for scatter-object to scatter to
        selection = cmds.ls(orderedSelection=True, flatten=True)
        # select all verts on an object:
        vtx_selection = cmds.polyListComponentConversion(selection,
                                                         toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31)
        # selects or re-selects the vertices previously selected
        cmds.select(vtx_selection)
        return vtx_selection

    def create_instances(self):
        scatter_source_object = 'pCube1'
        scattered_instances = []

        for vtx in self.vert_selection():
            # rewrite based on prof's code
            pos = cmds.pointPosition(vert)
            scatter_instance = cmds.instance(scatter_source_object,
                                             name="scatter_1")
            cmds.move(pos[0], pos[1], pos[2], scatter_instance,
                      worldSpace=True)

            scattered_instances.extend(scatter_instance)
            pos = cmds.xform([vtx], query=True, translation=True,
                             worldSpace=True)
            self.rand_rotation()
            #self.rand_scale()
    # group the instances -- arguments = list and a name for the list
        cmds.group(scattered_instances, name="scattered")