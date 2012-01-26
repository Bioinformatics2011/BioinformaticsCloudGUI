import os.path

class Project():
    name = ""
    path = ""
    
    def getFile(self, fileName):
        if os.path.exists(self.path + fileName):
            return File(self.path + fileName, self)
            
    def path(self):
        return self.path
