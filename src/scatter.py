import logging

import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

log = logging.getLogger(__name__)

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.scatter_slot = Scatter()
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(750)
        self.setMaximumHeight(350)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()

        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 35px")

        self.input_layout = self._create_input_layout()

        self.scatter_btn = QtWidgets.QPushButton("Scatter Objects")

        self.main_layout.addWidget(self.title_lbl)
        # self.main_layout.addLayout(self.textbox_lay)
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.scatter_btn)

        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def _create_input_layout(self):
        layout = self._create_ui_headers()

        self.rotate_dsbxes()
        self.scale_dsbxes()
        self._create_dsbx_headers(layout)
        self._create_selection_headers(layout)
        self._create_transform_headers(layout)

        return layout

    def _create_dsbx_headers(self, layout):
        layout.addWidget(QtWidgets.QLabel("RotateX"), 2, 1)
        layout.addWidget(QtWidgets.QLabel("RotateY"), 2, 2)
        layout.addWidget(QtWidgets.QLabel("RotateZ"), 2, 3)
        layout.addWidget(QtWidgets.QLabel("ScaleX"), 2, 4)
        layout.addWidget(QtWidgets.QLabel("ScaleY"), 2, 5)
        layout.addWidget(QtWidgets.QLabel("ScaleZ"), 2, 6)

        layout.addWidget(QtWidgets.QLabel("min"), 3, 0)
        layout.addWidget(QtWidgets.QLabel("max"), 4, 0)

        layout.addWidget(self.rotation_x_min_dsbx, 3, 1)
        layout.addWidget(self.rotation_x_max_dsbx, 4, 1)
        layout.addWidget(self.rotation_y_min_dsbx, 3, 2)
        layout.addWidget(self.rotation_y_max_dsbx, 4, 2)
        layout.addWidget(self.rotation_z_min_dsbx, 3, 3)
        layout.addWidget(self.rotation_z_max_dsbx, 4, 3)

        layout.addWidget(self.scale_x_min_dsbx, 3, 4)
        layout.addWidget(self.scale_x_max_dsbx, 4, 4)
        layout.addWidget(self.scale_y_min_dsbx, 3, 5)
        layout.addWidget(self.scale_y_max_dsbx, 4, 5)
        layout.addWidget(self.scale_z_min_dsbx, 3, 6)
        layout.addWidget(self.scale_z_max_dsbx, 4, 6)

        return layout

    def _create_ui_headers(self):
        self.scatter_header_lbl = QtWidgets.QLabel("Choose Source Object: ")
        self.scatter_header_lbl.setStyleSheet("font:bold")
        self.destination_header_lbl = QtWidgets.QLabel(
            "Choose Object/Vertices to Scatter To")

        self.scatter_object_le = QtWidgets.QLineEdit(
            self.scatter_slot.scatter_source_object)
        self.scatter_object_le.setMinimumWidth(100)
        self.destination_object_le = QtWidgets.QLineEdit()
        self.destination_object_le.setMinimumWidth(50)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_header_lbl, 0, 0)
        layout.addWidget(self.scatter_object_le, 0, 2)
        return (layout)

    def _create_transform_headers(self, layout):
        self.destination_header_lbl.setStyleSheet("font:bold")
        self.rotate_header_lbl = QtWidgets.QLabel("Rotate")
        self.rotate_header_lbl.setStyleSheet("font: bold")
        self.scale_header_lbl = QtWidgets.QLabel("Scale (default is 1)")
        self.scale_header_lbl.setStyleSheet("font: bold")

        layout.addWidget(self.destination_header_lbl, 0, 3)
        layout.addWidget(self.destination_object_le, 0, 5)
        layout.addWidget(self.rotate_header_lbl, 1, 2)
        layout.addWidget(self.scale_header_lbl, 1, 5)

    def _create_selection_headers(self, layout):
        self.random_percent_lbl = QtWidgets.QLabel("Percentage Selection")
        self.random_percent_lbl.setStyleSheet("font: bold")

        layout.addWidget(self.random_percent_lbl, 5, 2)

    def rotate_dsbxes(self):
        self.rotation_x_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_x_min_dsbx.setMaximum(360)
        self.rotation_x_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_x_max_dsbx.setMaximum(360)

        self.rotation_y_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_y_min_dsbx.setMaximum(360)
        self.rotation_y_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_y_max_dsbx.setMaximum(360)

        self.rotation_z_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_z_min_dsbx.setMaximum(360)
        self.rotation_z_min_dsbx.setFixedWidth(100)
        self.rotation_z_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_z_max_dsbx.setMaximum(360)
        self.rotation_z_max_dsbx.setFixedWidth(100)

    def scale_dsbxes(self):
        self.scale_x_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_x_min_dsbx.setMinimum(0.1)
        self.scale_x_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_x_max_dsbx.setMinimum(0.1)

        self.scale_y_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_y_min_dsbx.setMinimum(0.1)
        self.scale_y_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_y_max_dsbx.setMinimum(0.1)

        self.scale_z_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_z_min_dsbx.setMinimum(0.1)
        self.scale_z_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_z_max_dsbx.setMinimum(0.1)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter_slot)

    @QtCore.Slot()
    def _scatter_slot(self):
        self._set_values_from_ui()
        self.scatter_slot.create_instances()

    def _set_values_from_ui(self):
        self.scatter_slot.rotation_min[0] = self.rotation_x_min_dsbx.value()
        self.scatter_slot.rotation_max[0] = self.rotation_x_max_dsbx.value()
        self.scatter_slot.rotation_min[1] = self.rotation_y_min_dsbx.value()
        self.scatter_slot.rotation_max[1] = self.rotation_y_max_dsbx.value()
        self.scatter_slot.rotation_min[2] = self.rotation_z_min_dsbx.value()
        self.scatter_slot.rotation_max[2] = self.rotation_z_max_dsbx.value()

        self.scatter_slot.scale_min[0] = self.scale_x_min_dsbx.value()
        self.scatter_slot.scale_max[0] = self.scale_x_max_dsbx.value()
        self.scatter_slot.scale_min[1] = self.scale_y_min_dsbx.value()
        self.scatter_slot.scale_max[1] = self.scale_y_max_dsbx.value()
        self.scatter_slot.scale_min[2] = self.scale_z_min_dsbx.value()
        self.scatter_slot.scale_max[2] = self.scale_z_max_dsbx.value()


class Scatter(object):

    def __init__(self):
        self.rotation_min = [0, 0, 0]
        self.rotation_max = [360, 360, 360]
        self.scale_min = [1, 1, 1]
        self.scale_max = [10, 10, 10]
        # Neither of these are editable in the GUI
        self.scatter_source_object = 'pCube1'
        self.scatter_where_selected = []


    def vert_selection(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vtx_selection = cmds.polyListComponentConversion(selection,
                                                         toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31,
                                          expand=True)
        cmds.select(vtx_selection)
        return vtx_selection

    def rand_selection(self):
        seed = 1235
        percentage_selection = []
        for idx in range(0, len(self.vert_selection)):
            random.seed(idx + seed)
            rand_value = random.random()
            if rand_value <= 0.1:
                percentage_selection.append(self.vert_selection[idx])
        cmds.select(percentage_selection)

    def create_instances(self):
        scattered_instances = []
        for vtx in self.vert_selection():
            self.scatter_where_selected.append(vtx)
            pos = cmds.pointPosition(vtx)
            scatter_instance = cmds.instance(self.scatter_source_object,
                                             name="scatter_1")
            scattered_instances.extend(scatter_instance)
            cmds.move(pos[0], pos[1], pos[2], self.scatter_source_object,
                      worldSpace=True)
            self.rand_rotation(scatter_instance[0])
            self.rand_scale(scatter_instance[0])
        cmds.group(scattered_instances, name="scattered")

    def rand_rotation(self, scatter_instance):
        try:
            random_x = random.randrange(self.rotation_min[0],
                                        self.rotation_max[0])
            cmds.setAttr(scatter_instance + '.rotateX', random_x)
        except ValueError:
            random_x = self.rotation_min[0]
            cmds.setAttr(scatter_instance + '.rotateX', random_x)

        try:
            random_y = random.randrange(self.rotation_min[1],
                                        self.rotation_max[1])
            cmds.setAttr(scatter_instance + '.rotateY', random_y)
        except ValueError:
            random_y = self.rotation_min[1]
            cmds.setAttr(scatter_instance + '.rotateY', random_y)

        try:
            random_z = random.randrange(self.rotation_min[2],
                                        self.rotation_max[2])
            cmds.setAttr(scatter_instance + '.rotateZ', random_z)
        except ValueError:
            random_z = self.rotation_min[2]
            cmds.setAttr(scatter_instance + '.rotateZ', random_z)

    def rand_scale(self, scatter_instance):
        scale_x = random.uniform(self.scale_min[0], self.scale_max[0])
        cmds.setAttr(scatter_instance + '.scaleX', scale_x)

        scale_y = random.uniform(self.scale_min[1], self.scale_max[1])
        cmds.setAttr(scatter_instance + '.scaleY', scale_y)

        scale_z = random.uniform(self.scale_min[2], self.scale_max[2])
        cmds.setAttr(scatter_instance + '.scaleZ', scale_z)
