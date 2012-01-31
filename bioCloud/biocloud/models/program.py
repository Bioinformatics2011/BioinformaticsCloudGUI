import re

class Program():
    # Program class is the object representing the information about a program
    # to be executed via command line
    # an object of this class represents the recipe to be executed in the cluster
    # this is merely the interface to be implemented by every concrete program.
    
    def __init__(self, formContent, workflow, stepNumber):
        self.input = [i for i in range(self.numberOfInputFiles())]
        self.output = [i for i in range(self.numberOfOutputFiles())]
        self.submittedParams = [''] * self.numberOfParameters()
        
        #filter out the files
        for i, twoFiles in formContent['file'].iteritems():
            fileIndex = int(i)
            aFile = twoFiles["select"] if twoFiles["input"] == "" else twoFiles["input"]
            if fileIndex < self.numberOfInputFiles():
                self.setInput(fileIndex, aFile)
            else:
                self.setOutput(fileIndex-self.numberOfInputFiles(), aFile)
        
        #filter parameters
        for i, param in formContent['parameter'].iteritems():
            self.setParam(i, param)
            
            #sself.submittedParams[i] = "  ".join(param.itervalues())
    
    def setInputs(self, inputs):
        # TODO validate?
        self.input = inputs

    def setInput(self, i, fileName):
        # TODO validate?
        self.input[i] = fileName
        
    def setOutput(self, outputs):
        # TODO validate?
        self.output = outputs
        
    def setOutput(self, i, fileName):
        # TODO validate?
        self.output[i] = fileName
        
    def setParam(self, i, param, separator=" "):
        # TODO validate?
        for idx, val in param.iteritems():
            val = val.encode('ascii')
            if idx == 'flag':
                self.submittedParams[int(i)] = val + separator
            else:
                self.submittedParams[int(i)] += self.parseArgument(val, separator)
                
    def parseArgument(self, arg, separator=" "):
        if arg.isdigit():
            return  arg + separator
        else:
            return '"%s"%s' % (re.escape(arg), separator) 
            
    def getSubmittedParams(self):
        return " ".join(self.submittedParams)

    def commandLineScript(self, project):
        return "\n".join([self.prepare(project), self.run(project), self.clear(project)])
    def prepare(self, project):
        return ""
    def run(self, project):
        return ("%(bin)s -i %(inputs)s -o %(outputs)s"
            % { 'bin': self.binaryPath(),
                'inputs': " ".join(self.input),
                'outputs': " ".join(self.output)})
    def clear(self, project):
        return ""

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
        # absolute, if not in /usr/bin
        return "/someProgram"
    
    @classmethod
    def name(cls):
        return 'Abritrary Program'

    @classmethod
    def homepage(cls):
        return 'http://www.google.com'
    
    @classmethod
    def parameters(cls):
        return []
        
    @classmethod
    def asJson(self):
        from django.utils import simplejson as jsonSerializer
        info = {'inputs': self.numberOfInputFiles(),
        'outputs': self.numberOfOutputFiles(),
        'fileNames': self.fileSemantics(),
        'name': self.name(),
        'homepage': self.homepage(),
        'parameters': self.parameters()}
        return jsonSerializer.dumps(info)
            