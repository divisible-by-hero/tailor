import random
import pickle
from fabric.api import execute as fab_exec

class Sew:
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
        
    def add_methods(self, method_list):
        new_string = ""
        for method_task_dict in method_list:
            new_string = new_string + pickle.loads(str(method_task_dict['task'])) + "\n\n"
        fabfile = open(self.file_name, "a")
        fabfile.write(new_string)
        fabfile.close()
        
    def execute(self, commands):
        import fab_temp
        param_dict = {}
        command_response = []
        for command in commands:
            # Capture command name
            exe_command = command['command']
            # Capture params and pack them in a dict.
            for param in command['params']:
                param_dict[param['name']] = param['value']
            
            try:
                # Pass in a dict and eval.
                command_dict = {}
                import sys
                from cStringIO import StringIO
                old_stdout = sys.stdout
                #sys.stdout = sys.stderr
                sys.stdout = mystdout = StringIO()
                output = fab_exec(eval("fab_temp." + exe_command), **param_dict)
                sys.stdout = old_stdout
                command_dict['command'] = exe_command
                command_dict['response'] = mystdout.getvalue()
                command_response.append(command_dict)
            except AttributeError:
                return False, command_response
        return True, command_response
        
    def cleanup(self):
        import os
        os.remove("fab_temp.py")
        