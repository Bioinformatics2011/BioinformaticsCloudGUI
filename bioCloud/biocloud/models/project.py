class Project():
    name = ""
    path = ""
    
    def __init__(self, name, path):
        self.name = name
        self.path = path
    
    def file(self, fileName):
        return self.path + '/' + fileName
    
        
    def path(self):
        return self.path
