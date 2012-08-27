import pickle
import sys

from fabric.api import execute as fab_exec
from django.conf import settings
from tailor.servent import defaults as tailor_defaults

class Sew:

    def __init__(self, affix):
        self.fabfile_module = 'tailor_fabfile'
        fabfile_name = '%s.py' % self.fabfile_module
        fabfile_dir  = getattr(settings, 'TAILOR_TEMP_DIR', tailor_defaults.TAILOR_TEMP_DIR)

        self.fabfile_path = "%s%s" % (fabfile_dir, fabfile_name)
        sys.path.append(fabfile_dir)        

    def setup(self):
        
        fabfile = open(self.fabfile_path, "w")
        new_string = ""
        new_string = new_string + "from fabric.api import *\nfrom tailor.client.decorators import *\n\n\nimport fabric\n\n\n"
        
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
        
        fabfile = open(self.fabfile_path, "a")
        fabfile.write(new_string)
        fabfile.close()
        
    def add_methods(self, method_list):
        new_string = ""
        for method_task_dict in method_list:
            new_string = new_string + pickle.loads(str(method_task_dict['task'])) + "\n\n"
        fabfile = open(self.fabfile_path, "a")
        fabfile.write(new_string)
        fabfile.close()
        
    def execute(self, commands):
        # TODO: Don't like how this must match 'self.fabfile_module', but fine for now -G
        #import tailor_fabfile
        tailor_fabfile = __import__('tailor_fabfile')

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
                sys.stdout = mystdout = StringIO()
                output = fab_exec(eval("%s.%s" % (self.fabfile_module, exe_command)), **param_dict)
                sys.stdout = old_stdout
                command_dict['command'] = exe_command
                command_dict['response'] = mystdout.getvalue()
                command_response.append(command_dict)
            except AttributeError:
                response_dict = {'command': exe_command, "repsonse": "The command %s could not be found by the tailor fabric execution model." % exe_command}
                command_response.append(response_dict)
                return False, command_response
        return True, command_response
        
    def cleanup(self):
        import os
        os.remove(self.fabfile_path)
        try:
            os.remove("%sc" % self.fabfile_path)
        except:
            pass
        