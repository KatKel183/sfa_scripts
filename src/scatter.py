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
        self.scatter = Scatter()
        self.create_ui()
        # self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 35px")
        # folder layout line
        self.transform_lay = self._create_transform_ui()
        # button layout line
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        # addLayout for folder layout
        self.main_lay.addLayout(self.transform_lay)
        self.main_lay.addStretch()
        # addLayout button
        self.setLayout(self.main_lay)

    # def create_connections(self):
    #    """Connect our widget signals to slots"""

    def _create_transform_ui(self):
        layout = self._create_transform_headers()
        self.scatter_object_le = QtWidgets.QLineEdit(
            self.scatter.scatter_object)
        self.scatter_object_le.setMinimumWidth(100)
        self.destination_object_le = QtWidgets.QLineEdit(
            self.scatter.destination_object)
        self.destination_object_le.setMinimumWidth(100)
        self.rx_max_sbx = QtWidgets.QSpinBox()
        self.rx_max_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rx_max_sbx.setFixedWidth(100)
        # matching labels to transformations
        layout.addWidget(QtWidgets.QLabel("RotateX"), 2, 1)
        layout.addWidget(QtWidgets.QLabel("RotateY"), 2, 2)
        layout.addWidget(QtWidgets.QLabel("RotateZ"), 2, 3)
        layout.addWidget(QtWidgets.QLabel("ScaleX"), 2, 4)
        layout.addWidget(QtWidgets.QLabel("ScaleY"), 2, 5)
        layout.addWidget(QtWidgets.QLabel("ScaleZ"), 2, 6)
        # matching labels to min/max
        layout.addWidget(QtWidgets.QLabel("min"), 3, 0)
        layout.addWidget(QtWidgets.QLabel("max"), 4, 0)
        # type info about scatter and destination objects
        layout.addWidget(self.scatter_object_le, 0, 2)
        layout.addWidget(self.destination_object_le, 0, 4)
        # type info about transformations
        # definitely need to put a ton more code here
        return (layout)

    def _create_transform_headers(self):
        self.scatter_header_lbl = QtWidgets.QLabel("Choose Scatter Object: ")
        self.scatter_header_lbl.setStyleSheet("font:bold")
        self.destination_header_lbl = QtWidgets.QLabel(
            "Choose Object/Vertices to Scatter To")
        self.destination_header_lbl.setStyleSheet("font:bold")
        self.rotate_header_lbl = QtWidgets.QLabel("Rotate")
        self.rotate_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        # row 0
        layout.addWidget(self.scatter_header_lbl, 0, 0)
        layout.addWidget(self.destination_header_lbl, 0, 3)
        # row 1
        layout.addWidget(self.rotate_header_lbl, 1, 2)
        return (layout)

# CLASS: create logic for program
class Scatter(object):
    """Representation of a Scatter program"""

    #the init has the defaults
    def __init__(self):
        # user_input of shape to scatter
        self.scatter_object = 'pCube1'
        # when is init called?
        self.destination_object = self.vert_selection()
        # call the stuff for rotations and scale


    def transform_adjust(self):
        # these should start out with un-transformed values
        sca_min_x = 1.0
        sca_max_x = 1.0
        sca_min_y = 1.0
        sca_max_y = 1.0
        sca_min_z = 1.0
        sca_max_z = 1.0
        # rotation is 0 to 360.
        r_min_x = 0
        r_max_x = 0
        r_min_y = 0
        r_max_y = 0
        r_min_z = 0
        r_max_z = 0

    def transform_random(self):
        # scale variables
        size_x = random.uniform(1.0, 5.5)
        size_y = random.uniform(1.0, 5.5)
        size_z = random.uniform(1.0, 5.5)

        # rotate variables - replace hard-coded with user-input variables
        rotate_x = random.uniform(0, 360)
        rotate_y = random.uniform(0, 360)
        rotate_z = random.uniform(0, 360)

    def vert_selection(self):
        # --Selecting locations for scatter-object to scatter to
        selection = cmds.ls(orderedSelection=True, flatten=True)
        # select all verts on an object:
        vtx_selection = cmds.polyListComponentConversion(selection,
                                                         toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31,
                                      expand=True)
        # selects or re-selects the vertices previously selected
        cmds.select(vtx_selection)
        return vtx_selection



    def create_instances(self):
        scattered_instances = []
        for vtx in vert_selection():
        # change pCube1 to soft-coded variable - scatter_object
        #scatter_instance = cmds.instance("pCube1", name="instance#")
            scatter_instance = cmds.instance("pCube1", name="instance1")
            scattered_instances.extend(scatter_instance)
            pos = cmds.xform([vtx], query=True, translation=True, worldSpace=True)
            cmds.xform(scatter_instance, translation=pos,
                    rotation=[rotate_x, rotate_y, rotate_z],
                    scale=[size_x, size_y, size_z])
    # group the instances -- arguments = list and a name for the list
        cmds.group(scattered_instances, name="scattered")
