from subprocess import call
from biocloud.models.program import Program

class CloudBurst(Program):
	
    def run(self, project):
        command = "%(bin)s %(refpath)s %(qrypath)s %(outputpath)s %(parameters)s" % {'bin':self.binaryPath(), 
            'refpath':project.file(self.input[0]), 
            'qrypath':project.file(self.input[1]), 
            'parameters':self.getSubmittedParams(), 
            'outputpath':project.file(self.output[0])}
        #call(command, shell=True)
        return command

    @classmethod
    def numberOfInputFiles(cls):
        return 2

    @classmethod
    def fileSemantics(cls):
        # meant for usage in the user interface
        # e.g. to distinguish unambigiously between query and reference seq
        return ["Reference File","Query File", "Output (bed) File"]
    
    @classmethod
    def numberOfOutputFiles(cls):
        return 1
    
    @classmethod
    def binaryPath(cls):
        # absolute, if not in /usr/bin
        return "cloudburstpathhere"
    
    @classmethod
    def name(cls):
        return 'CloudBurst'
        
    @classmethod
    def numberOfParameters(cls):
        return 10
        
    @classmethod
    def parameters(cls):
        # currently just a simple list of lists [["name","flag","type","compulsory","default"],...] 
        #where type can be either flag or variable and compulsory is boolean value stating
        #wether this needs to be set or filled and default is default value for field (left blank for just flags)
        
        #note that cloudburst doesn't really have flags
        
        #readlen:          minimum length of the reads
 		#k:                number of mismatches / differences to allow (higher number requires more time)
 		#allowdifferences: 0: mismatches only, 1: indels as well 
 		#filteralignments: 0: all alignments, 1: only report unambiguous best alignment (results identical to RMAP)
 		#mappers:         number of mappers to use.              suggested: #processor-cores * 10
 		#reduces:         number of reducers to use.             suggested: #processor-cores * 2
 		#fmappers:        number of mappers for filtration alg.  suggested: #processor-cores
 		#freducers:       number of reducers for filtration alg. suggested: #processor-cores
 		#blocksize:        number of qry and ref tuples to consider at a time in the reduce phase. suggested: 128 
 		#redundancy:       number of copies of low complexity seeds to use. suggested: # processor cores
        return [["readlen","","var",True,"24"],
        		["k","","var",True,"2"],
        		["allowdifferences","","var",True,"0"],
        		["filteralignments","","var",True,"0"],
        		["mappers","","var",True,"10"],
        		["reducers","","var",True,"10"],
        		["fmappers","","var",True,"1"],
        		["freducers","","var",True,"1"],
        		["blocksize","","var",True,"128"],
        		["redundancy","","var",True,"1"]]

    @classmethod
    def homepage(cls):
        return 'http://sourceforge.net/apps/mediawiki/cloudburst-bio/index.php?title=CloudBurst'