import random
import pickle
from fabric.api import execute as fab_exec

class Shirt:
    file_name = "fab_temp.py"
    
    def __init__(self):
        pass
        
    def setup(self):
        fabfile = open(self.file_name, "w")
        new_string = ""
        new_string = new_string + "from fabric.api import *\nfrom tailor.decorators import *\n\n\nimport fabric\n\n\n"
        
        
        new_string = new_string + '''fabric.state.output["status"] = True\nfabric.state.output["running"] = True\nfabric.state.output["user"] = True\nfabric.state.output["warnings"] = True\nfabric.state.output["stderr"] = True\nfabric.state.output['stdout'] = True\nfabric.state.output['aborts'] = False\n\n'''
        fabfile.write(new_string)
        fabfile.close()
    
    def add_vars(self, env_dict):
        new_string = ""
        for _varname, _var in env_dict.iteritems():
            if isinstance(_var, str):
                new_string = new_string + "env.%s = \"%s\"" % (_varname, _var) + "\n"
            else:
                new_string = new_string + "env.%s = %s" % (_varname, _var) + "\n"
        new_string = new_string + "\n\n"
        
        fabfile = open(self.file_name, "a")
        fabfile.write(new_string)
        fabfile.close()
        
    def add_methods(self, method_dict):
        new_string = ""
        for method_name, method in method_dict:
            new_string = new_string + pickle.loads(str(method)) + "\n\n"
        fabfile = open(self.file_name, "a")
        fabfile.write(new_string)
        fabfile.close()
        
    def execute(self, commands):
        import fab_temp
        for command in commands:
            print command
            try:
                output = fab_exec(eval("fab_temp." + command))
                print("output")
                print output
            except AttributeError:
                return False
        return True
        
    def cleanup(self):
        import os
        os.remove("fab_temp.py")
        