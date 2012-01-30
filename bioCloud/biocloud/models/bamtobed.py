from biocloud.models.program import Program
# bamToBed -i /home/bioinfo/bioinfo_2011/NGS/testt.bam > outfile.bed
class BamToBed(Program):

    def run(self, project):
        return ("%(bin)s %(parameters)s -i %(inputs)s > %(outputs)s"
            % { 'bin': self.binaryPath(),
                'parameters': self.getSubmittedParams(),
                'inputs': project.file(self.input[0]),
                'outputs': project.file(self.output[0])})

    @classmethod
    def numberOfInputFiles(cls):
        return 1

    @classmethod
    def fileSemantics(cls):
        # meant for usage in the user interface
        # e.g. to distinguish unambigiously between query and reference seq
        return ["Bam File", "Output (bed) File"]
    
    @classmethod
    def numberOfOutputFiles(cls):
        return 1
    
    @classmethod
    def binaryPath(cls):
        # absolute, if not in /usr/bin
        return "bamToBed"
    
    @classmethod
    def name(cls):
        return 'bamToBed'
        
    @classmethod
    def numberOfParameters(cls):
        return 3
        
    @classmethod
    def parameters(cls):
        # currently just a simple list of lists [["name","flag","type"],...] where type can be either flag or variable
        return [["edit distance","-ed","flag"],["to bedpe","-bedpe","flag"],["test variable submit","-testvar","var"]]

    @classmethod
    def homepage(cls):
        return 'http://code.google.com/p/altanalyze/wiki/BAMtoBED'