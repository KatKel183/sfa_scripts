import random

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

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
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.scatter_btn)

        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def _create_input_layout(self):
        layout = self._create_ui_headers()
        # ** self.textbox_lay = self._create_ui_textboxes()
        self.rotate_dsbxes()
        # ** self.scale_dsbxes()
        self._create_dsbx_headers(layout)

        # ** self.main_layout.addWidget(self.textbox_lay)
        self.display_dsbxes(layout)

        return layout

    def _create_dsbx_headers(self, layout):
        layout.addWidget(QtWidgets.QLabel("RotateX"), 2, 1)
        layout.addWidget(QtWidgets.QLabel("RotateY"), 2, 2)
        layout.addWidget(QtWidgets.QLabel("RotateZ"), 2, 3)
        layout.addWidget(QtWidgets.QLabel("ScaleX"), 2, 4)
        layout.addWidget(QtWidgets.QLabel("ScaleY"), 2, 5)
        layout.addWidget(QtWidgets.QLabel("ScaleZ"), 2, 6)
        # matching labels to min/max
        layout.addWidget(QtWidgets.QLabel("min"), 3, 0)
        layout.addWidget(QtWidgets.QLabel("max"), 4, 0)
        return layout

    def _create_ui_headers(self):
        self.scatter_header_lbl = QtWidgets.QLabel("Choose Source Object: ")
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

    def _create_ui_textboxes(self):
        layout = self._create_ui_headers()
        self.scatter_object_le = QtWidgets.QLineEdit(
            self.scatter_slot.scatter_source_object)
        self.scatter_object_le.setMinimumWidth(100)
        self.destination_object_le = QtWidgets.QListWidget(
            self.scatter_slot.scatter_where_selected)
        self.destination_object_le.setMinimumWidth(100)

        layout.addWidget(self.scatter_object_le, 0, 2)
        layout.addWidget(self.destination_object_le, 0, 5)
        return(layout)

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
        self.rotation_z_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_z_max_dsbx.setMaximum(360)

    def scale_dsbxes(self):
        self.scale_y_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_y_min_dsbx.setMinimum(1)
        self.scale_y_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.scale_y_max_dsbx.setMinimum(1)

    def display_dsbxes(self, layout):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rotation_x_min_dsbx, 3, 1)
        layout.addWidget(self.rotation_x_max_dsbx, 4, 1)
        layout.addWidget(self.rotation_y_min_dsbx, 3, 2)
        layout.addWidget(self.rotation_y_max_dsbx, 4, 2)
        layout.addWidget(self.rotation_z_min_dsbx, 3, 3)
        layout.addWidget(self.rotation_z_max_dsbx, 4, 3)
        # self.main_layout.addWidget(self.rotation_y_min_dsbx, 3, 2)
        # self.main_layout.addWidget(self.rotation_y_max_dsbx, 4, 2)
        return layout

    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter_slot)

    @QtCore.Slot()
    def _scatter_slot(self):
        self._set_values_from_ui()
        # !-! extract the .rotation into its own method
        self.scatter_slot.create_instances()

    def _set_values_from_ui(self):
        self.scatter_slot.rotation_min[1] = self.rotation_y_min_dsbx.value()
        self.scatter_slot.rotation_max[1] = self.rotation_y_max_dsbx.value()


class Scatter(object):

    def __init__(self):
        self.rotation_min = [0, 0, 0]
        self.rotation_max = [360, 360, 360]
        # self.scale_min = [0, 0, 0]
        # self.scale_max = [360, 360, 360]
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
        cmds.group(scattered_instances, name="scattered")

    def rand_rotation(self, scatter_instance):
        # [1] is for y
        random_y = random.randrange(self.rotation_min[1], self.rotation_max[1])
        cmds.setAttr(scatter_instance + '.rotateY', random_y)
