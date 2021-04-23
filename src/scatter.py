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
        self.scatter_btn = QtWidgets.QPushButton("Scatter Tool")
        # visuals for the rotation boxes
        self.rotation_y_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_y_min_dsbx.setMaximum(360)
        self.rotation_y_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_y_max_dsbx.setMaximum(360)
        # -----what I coded
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 35px")
        self.transform_lay = self._create_transform_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.transform_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)


    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter_slot)

    @QtCore.Slot()
    def _scatter_slot(self):
        """Scatter objects onto vertices"""
        self._set_scatter_properties_from_ui()
        self._set_values_from_ui()
        self.scatter.create_instances()

    def _set_scatter_properties_from_ui(self):
        self.scatter.scatter_object = self.scatter_object_le.text()
        self.scatter.destination_object = self.destination_object_le.text()

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter Objects")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_transform_ui(self):
        layout = self._create_ui_headers()
        self.scatter_object_le = QtWidgets.QLineEdit(
            self.scatter.scatter_object)
        self.scatter_object_le.setMinimumWidth(100)
        # QtWidgets.QLineEdit vs QtWidgets.QListWidget
        self.destination_object_le = QtWidgets.QListWidget(
            self.scatter.destination_object)
        self.destination_object_le.setMinimumWidth(100)
        # transform spinboxes now in two separate methods
        self.rotate_sbxes()
        self.scale_sbxes()
        # matching labels to min/max
        layout.addWidget(QtWidgets.QLabel("min"), 3, 0)
        layout.addWidget(QtWidgets.QLabel("max"), 4, 0)
        # user input lines for scatter and destination objects
        layout.addWidget(self.scatter_object_le, 0, 2)
        layout.addWidget(self.destination_object_le, 0, 4)
        self._create_transform_headers(layout)
        return (layout)

    def _create_transform_headers(self, layout):
        # matching labels to transformations
        layout.addWidget(QtWidgets.QLabel("RotateX"), 2, 1)
        layout.addWidget(QtWidgets.QLabel("RotateY"), 2, 2)
        layout.addWidget(QtWidgets.QLabel("RotateZ"), 2, 3)
        layout.addWidget(QtWidgets.QLabel("ScaleX"), 2, 4)
        layout.addWidget(QtWidgets.QLabel("ScaleY"), 2, 5)
        layout.addWidget(QtWidgets.QLabel("ScaleZ"), 2, 6)
        # user input for max
        layout.addWidget(self.rx_min_dsbx, 3, 1)
        layout.addWidget(self.ry_min_dsbx, 3, 2)
        layout.addWidget(self.rz_min_dsbx, 3, 3)
        layout.addWidget(self.sx_min_dsbx, 3, 4)
        layout.addWidget(self.sy_min_dsbx, 3, 5)
        layout.addWidget(self.sz_min_dsbx, 3, 6)
        # user input for max
        layout.addWidget(self.rx_max_dsbx, 4, 1)
        layout.addWidget(self.ry_max_dsbx, 4, 2)
        layout.addWidget(self.rz_max_dsbx, 4, 3)
        layout.addWidget(self.sx_max_dsbx, 4, 4)
        layout.addWidget(self.sy_max_dsbx, 4, 5)
        layout.addWidget(self.sz_max_dsbx, 4, 6)
        return layout

    def scale_sbxes(self):
        # sx min and max
        self.sx_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.sx_min_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sx_min_dsbx.setFixedWidth(100)
        self.sx_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.sx_max_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sx_max_dsbx.setFixedWidth(100)
        # sy min and max
        self.sy_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.sy_min_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sy_min_dsbx.setFixedWidth(100)
        self.sy_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.sy_max_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sy_max_dsbx.setFixedWidth(100)
        # sz min and max
        self.sz_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.sz_min_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sz_min_dsbx.setFixedWidth(100)
        self.sz_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.sz_max_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sz_max_dsbx.setFixedWidth(100)

    def rotate_sbxes(self):
        # settings for rx spinboxes
        self.rx_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rx_min_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rx_min_dsbx.setFixedWidth(100)
        self.rx_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rx_max_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rx_max_dsbx.setFixedWidth(100)
        # settings for ry spinboxes
        self.ry_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.ry_min_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ry_min_dsbx.setFixedWidth(100)
        self.ry_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.ry_max_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ry_max_dsbx.setFixedWidth(100)
        # settings for rz spinboxes
        self.rz_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rz_min_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rz_min_dsbx.setFixedWidth(100)
        self.rz_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rz_max_dsbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.rz_max_dsbx.setFixedWidth(100)

    def _create_ui_headers(self):
        self.scatter_header_lbl = QtWidgets.QLabel("Choose Scatter Object: ")
        self.scatter_header_lbl.setStyleSheet("font:bold")
        self.destination_header_lbl = QtWidgets.QLabel(
            "Choose Object/Vertices to Scatter To")
        self.destination_header_lbl.setStyleSheet("font:bold")
        self.rotate_header_lbl = QtWidgets.QLabel("Rotate")
        self.rotate_header_lbl.setStyleSheet("font: bold")
        self.scale_header_lbl = QtWidgets.QLabel("Scale")
        self.scale_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_header_lbl, 0, 0)
        layout.addWidget(self.destination_header_lbl, 0, 3)
        layout.addWidget(self.rotate_header_lbl, 1, 2)
        layout.addWidget(self.scale_header_lbl, 1, 5)
        return (layout)


class Scatter(object):

    def __init__(self):
        self.rotation_min = [0, 0, 0]
        self.rotation_max = [360, 360, 360]
        self.scale_min = [1, 1, 1]
        self.scale_max = [20, 20, 20]
        # source and destination
        self.scatter_object = 'pCube1'
        self.destination_object = self.vert_selection()

    def transform_random(self):
        self.size_x = random.uniform(sx_min, sx_max)
        self.size_y = random.uniform(sy_min, sy_max)
        self.size_z = random.uniform(sz_min, sz_max)
        self.rotate_x = random.uniform(rx_min, rx_max)
        self.rotate_y = random.uniform(ry_min, ry_max)
        self.rotate_z = random.uniform(rz_min, rz_max)

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
        for vtx in self.vert_selection():
            pos = cmds.pointPosition(vtx)
            scatter_instance = cmds.instance(self.scatter_object,
                                             name="scatter_1")
            scattered_instances.extend(scatter_instance)
            cmds.move(pos[0], pos[1], pos[2], self.scatter_object,
                      worldSpace=True)

    # group the instances -- arguments = list and a name for the list
        cmds.group(scattered_instances, name="scattered")
