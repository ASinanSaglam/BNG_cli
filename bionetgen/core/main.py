import os, subprocess

def run(inp, out):
    '''
    Convenience function to run BNG2.pl from python

    Usage: run(path_to_input_file, output_folder)

    path_to_input_file: this has to point to a BNGL file

    output_folder: this points to a folder to put 
    the results into. If it doesn't exist, it will be 
    created.
    '''
    # pull bngpath relative to our file name
    lib_path = os.path.split(os.path.dirname(__file__))[0]
    bngpath = os.path.join(lib_path, "bng")
    # instantiate a CLI object with the info
    cli = BNGCLI(inp, out, bngpath)
    cli.run()

def runCLI(args):
    # this pulls out the arguments
    inp_file = args.input
    output = args.output
    bngpath = args.bngpath 
    # and instantiates the CLI object
    cli = BNGCLI(inp_file, output, bngpath)
    cli.run()

class BNGCLI:
    def __init__(self, inp_file, output, bngpath):
        self.inp_file = inp_file
        # ensure correct path to the input file
        self.inp_path = os.path.abspath(self.inp_file)
        # pull other arugments out
        self.set_output(output)
        # sedml_file = sedml
        self.bngpath = bngpath
        # setting up bng2.pl
        self.bng_exec = os.path.join(self.bngpath, "BNG2.pl")
        assert os.path.exists(self.bng_exec), "BNG2.pl is not found!"
        if "BNGPATH" in os.environ:
            self.old_bngpath = os.environ["BNGPATH"]
        else:
            self.old_bngpath = None
        os.environ["BNGPATH"] = self.bngpath

    def set_output(self, output):
        # setting up output area
        self.output = output
        if os.path.isdir(output):
            # path exists, let's go there
            os.chdir(output)
        else:
            os.mkdir(output)
            os.chdir(output)

    def run(self):
        # run BNG2.pl
        rc = subprocess.run(["perl", self.bng_exec, self.inp_path])
        # set BNGPATH back
        if self.old_bngpath is not None:
            os.environ["BNGPATH"] = self.old_bngpath