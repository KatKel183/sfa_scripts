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
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(750)
        self.setMaximumHeight(350)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        # scatter connection goes in further down
        self.create_ui()
        self.create_connections()

    # self.scatter = Scatter()
    def create_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()

        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 35px")

        self.rotation_y_min_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_y_min_dsbx.setMaximum(360)
        self.rotation_y_max_dsbx = QtWidgets.QDoubleSpinBox()
        self.rotation_y_min_dsbx.setMaximum(360)

        self.scatter_btn = QtWidgets.QPushButton("Scatter Objects")
        # ** self.main_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addWidget(self.rotation_y_min_dsbx)
        self.main_layout.addWidget(self.rotation_y_max_dsbx)
        self.main_layout.addWidget(self.scatter_btn)

        # create transform ui
        # create button ui??
        # ** self.main_layout = QtWidgets.QVBoxLayout()

        # display create transform ui
        self.main_layout.addStretch()
        # display create button ui

        self.setLayout(self.main_layout)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter_slot)

    @QtCore.Slot()
    def _scatter_slot(self):
        scatter_slot = Scatter()
        # !-! extract the .rotation into its own method
        scatter_slot.rotation_min[1] = self.rotation_y_min_dsbx.value()
        scatter_slot.rotation_max[1] = self.rotation_y_max_dsbx.value()
        scatter_slot.create_instances()


class Scatter(object):

    def __init__(self):
        self.rotation_min = [0, 0, 0]
        self.rotation_max = [360, 360, 360]
        # self.scale_min = [0, 0, 0]
        # self.rotation_max = [360, 360, 360]
        # self.scatter_source_object = 'pCube1'
        # self.destination_object = self.vert_selection()

    def vert_selection(self):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vtx_selection = cmds.polyListComponentConversion(selection,
                                                         toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31,
                                          expand=True)
        cmds.select(vtx_selection)
        return vtx_selection

    def create_instances(self):
        scatter_source_object = 'pCube1'
        scattered_instances = []
        for vtx in self.vert_selection():
            pos = cmds.pointPosition(vtx)
            scatter_instance = cmds.instance(scatter_source_object,
                                             name="scatter_1")
            scattered_instances.extend(scatter_instance)
            cmds.move(pos[0], pos[1], pos[2], scatter_source_object,
                      worldSpace=True)
        cmds.group(scattered_instances, name="scattered")

    def rand_rotation(self, scatter_instance):
        # [1] is for y
        random_y = random.randrange(self.rotation_min[1], self.rotation_max[1])
        cmds.setAttr(scatter_instance + '.rotateY', random_y)