from django.db import models
from observer import Subject
import os.path

def content_file_name(instance, filename):
    return '/'.join([instance.userName, filename])


class UserFile(models.Model):
    userFile = models.FileField(upload_to=content_file_name)
    userName = models.CharField(max_length=30)
    
    def filename(self):
        return os.path.basename(self.userFile.name)


class Project():
    name = ""
    path = ""
    
    def getFile(self, fileName):
        if os.path.exists(self.path + fileName):
            return File(self.path + fileName, self)
            
    def path(self):
        return self.path

class File(Subject):
    path = ""
    project = ""
    
    def __init__(self, path, project):
        self.path = path
        self.project = project
    
    def path(self):
        return self.path
    
    def name(self):
        return os.path.basename(self.path())
        
class Program():
    # some explicit files, according to
    input = []
    output = []
    
    # Program class is the object representing the information about a program
    # to be executed via command line
    # an object of this class represents the recipe to be executed in the cluster
    # this is merely the interface to be implemented by every concrete program.
    
    def __init__(self, formContent, workflow, stepNumber):
        #filter out the files
        pass
    
    def set_inputs(self, inputs):
        # TODO validate?
        self.input = inputs
        
    def set_output(self, outputs):
        # TODO validate?
        self.output = outputs
        
    def commandLineScript(self):
        return ''
    def prepare(self):
        pass
    def run(self):
        pass
    def clear(self):
        pass

    @classmethod
    def numberOfInputFiles(cls):
        return 1

    @classmethod
    def fileSemantics(cls):
        # meant for usage in the user interface
        # e.g. to distinguish unambigiously between query and reference seq
        return ["Input File", "Output File"]
    
    @classmethod
    def numberOfOutputFiles(cls):
        return 1
    
    @classmethod
    def binaryPath(cls):
        # absolute
        return "/"
    
    @classmethod
    def name(cls):
        return 'Abritrary Program'
    
    @classmethod
    def parameters(cls):
        return {}
        
    @classmethod
    def asJson(self):
        from django.utils import simplejson as jsonSerializer
        info = {'inputs': self.numberOfInputFiles(),
        'outputs': self.numberOfOutputFiles(),
        'fileNames': self.fileSemantics(),
        'name': self.name(),
        'parameters': self.parameters()}
        return jsonSerializer.dumps(info)
            