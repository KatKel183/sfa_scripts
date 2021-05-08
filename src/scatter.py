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

        layout.addWidget(QtWidgets.QLabel("minimum"), 3, 0)
        layout.addWidget(QtWidgets.QLabel("maximum"), 4, 0)

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
        self.scatter_object_le = QtWidgets.QLineEdit()

        self.scatter_object_le.setMinimumWidth(100)

        self.source_object_btn = QtWidgets.QPushButton("Update Source Object")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_header_lbl, 0, 0)
        layout.addWidget(self.scatter_object_le, 0, 2)
        layout.addWidget(self.source_object_btn, 0, 5)
        return (layout)

    def _create_transform_headers(self, layout):
        self.rotate_header_lbl = QtWidgets.QLabel("Rotate")
        self.rotate_header_lbl.setStyleSheet("font: bold")
        self.scale_header_lbl = QtWidgets.QLabel("Scale (default is 1)")
        self.scale_header_lbl.setStyleSheet("font: bold")

        layout.addWidget(self.rotate_header_lbl, 1, 2)
        layout.addWidget(self.scale_header_lbl, 1, 5)

    def _create_selection_headers(self, layout):
        self.rand_percent_header_lbl = QtWidgets.QLabel("Percentage Selected:")
        self.rand_percent_header_lbl.setStyleSheet("font: bold")

        layout.addWidget(QtWidgets.QLabel("Out of 100% (1.00)"), 6, 0)
        self.rand_percent_select_dsbx = QtWidgets.QDoubleSpinBox()
        self.rand_percent_select_dsbx.setMaximum(1.00)

        layout.addWidget(self.rand_percent_header_lbl, 5, 0)
        layout.addWidget(self.rand_percent_select_dsbx, 6, 1)

        self._create_seed_ui(layout)

    def _create_seed_ui(self, layout):
        self.seed_header_lbl = QtWidgets.QLabel("Set Seed:")
        self.seed_header_lbl.setStyleSheet("font: bold")

        self.set_seed_sbx = QtWidgets.QSpinBox()
        self.set_seed_sbx.setMaximum(9999)
        self.set_seed_sbx.setFixedWidth(100)

        layout.addWidget(self.seed_header_lbl, 5, 3)
        layout.addWidget(self.set_seed_sbx, 6, 3)

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
        self.source_object_btn.clicked.connect(self._source_obj_btn_slot)

    @QtCore.Slot()
    def _scatter_slot(self):
        self._set_transform_values_from_ui()
        self._set_selection_values_from_ui()
        self.scatter_slot.create_instances()

    @QtCore.Slot()
    def _source_obj_btn_slot(self):
        print("it worked")

    def _set_transform_values_from_ui(self):
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

    def _set_selection_values_from_ui(self):
        self.scatter_slot.percent_set = self.rand_percent_select_dsbx.value()
        self.scatter_slot.set_seed = self.set_seed_sbx.value()


class Scatter(object):

    def __init__(self):
        self.rotation_min = [0, 0, 0]
        self.rotation_max = [360, 360, 360]
        self.scale_min = [1, 1, 1]
        self.scale_max = [10, 10, 10]
        # Neither of these are editable in the GUI
        self.scatter_source_object = 'pCube1'
        # percentage selection, checkbox, etc
        self.percent_set = 0.1
        self.set_seed = 1235

    def vert_selection(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vtx_selection = cmds.polyListComponentConversion(selection,
                                                         toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31,
                                          expand=True)
        cmds.select(vtx_selection)
        return vtx_selection

    def rand_selection(self):
        percentage_selection = []
        verts_selected = self.vert_selection()
        random.seed(self.set_seed)

        for idx in range(0, len(verts_selected)):
            rand_value = random.random()
            if rand_value <= self.percent_set:
                percentage_selection.append(verts_selected[idx])
        cmds.select(percentage_selection)
        return percentage_selection

    def create_instances(self):
        scattered_instances = []
        for vtx in self.rand_selection():
            pos = cmds.pointPosition(vtx)
            scatter_instance = cmds.instance(self.scatter_source_object,
                                             name="scatter_1")
            scattered_instances.extend(scatter_instance)
            cmds.move(pos[0], pos[1], pos[2], scatter_instance,
                      worldSpace=True)
            self.rand_rotation(scatter_instance[0])
            self.rand_scale(scatter_instance[0])
            # self.constrain_instance(scatter_instance[0])
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

    def constrain_instance(self, scatter_instance):
        constraint = cmds.normalConstraint(['pSphere1.vtx[37]'], 'scatter_36')
        # print(constraint)
        cmds.delete(constraint)
       # cmds.pointOnPolyConstraint
