class SceneFile(object):
    """An abstract representation of a Scene file"""
    def __init__(self, folder_path, descriptor, task, ver, ext):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.ver = ver
        self.ext = ext


scene_file = SceneFile("D:\\", "tank", "model", 1, ".ma")
print(scene_file.descriptor)
print(scene_file.task)
