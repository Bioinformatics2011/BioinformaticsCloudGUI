import os.path

class File():
    path = ""
    project = ""
    
    def __init__(self, path, project):
        self.path = path
        self.project = project
    
    def path(self):
        return self.path
    
    def name(self):
        return os.path.basename(self.path())