import codecs
import platform
import subprocess
import os, os.path
from chardet import detect

class OSManager():

    def __init__(self):
        pass

    # Create a set of arguments which make a ``subprocess.Popen`` (and
    # variants) call work with or without Pyinstaller, ``--noconsole`` or
    # not, on Windows and Linux. Typical use::
    #
    #   subprocess.call(['program_to_run', 'arg_1'], **subprocess_args())
    #
    # When calling ``check_output``::
    #
    #   subprocess.check_output(['program_to_run', 'arg_1'],
    #                           **subprocess_args(False))
    def subprocess_args(self, include_stdout=True):
        # The following is true only on Windows.
        if hasattr(subprocess, 'STARTUPINFO'):
            # On Windows, subprocess calls will pop up a command window by default
            # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
            # distraction.
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # Windows doesn't search the path by default. Pass it an environment so
            # it will.
            env = os.environ
        else:
            si = None
            env = None

        # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
        #
        #   Traceback (most recent call last):
        #     File "test_subprocess.py", line 58, in <module>
        #       **subprocess_args(stdout=None))
        #     File "C:\Python27\lib\subprocess.py", line 567, in check_output
        #       raise ValueError('stdout argument not allowed, it will be overridden.')
        #   ValueError: stdout argument not allowed, it will be overridden.
        #
        # So, add it only if it's needed.
        if include_stdout:
            ret = {'stdout': subprocess.PIPE}
        else:
            ret = {}

        # On Windows, running this from the binary produced by Pyinstaller
        # with the ``--noconsole`` option requires redirecting everything
        # (stdin, stdout, stderr) to avoid an OSError exception
        # "[Error 6] the handle is invalid."
        ret.update({'stdin': subprocess.PIPE,
                    'stderr': subprocess.PIPE,
                    'startupinfo': si,
                    'env': env})
        return ret


    # Get Sitem Type [windows, linux, darwin]
    # Return string
    def getSystemType(self):
        res = platform.system()
        return res


    def encodeCMD(self, cmd):
        ## Byppass / Set-ExecutionPolicy -Scope Process -ExecutionPolicy Restricted -Force / Set-ExecutionPolicy -Scope
        print(cmd)
        bypassed_cmd = subprocess.Popen(['powershell','$bytes = [System.Text.Encoding]::Unicode.GetBytes("' + cmd + '") ; [Convert]::ToBase64String($bytes)'], shell=True, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
        output, errors = bypassed_cmd.communicate()
        if errors != '':
            print(errors)
            return False

        return output


    # Execute complex cmd comands like powershell cmd-lets
    # Return string or False
    def executeAdminCMD(self, cmd, clear_data=True):
        res = subprocess.Popen(cmd, shell=True, universal_newlines=True, **self.subprocess_args(True))
        output, errors = res.communicate()

        if errors != '':
            return False
        else:
            res = output
            if clear_data == True:
                res = output.replace('\r', '')
                res = res.replace('\n', '')
            return res


    # Execute subprocess comands
    # Return string or False
    def executeCMD(self, cmd, clear_data=True, new_shell=True):
        try:
            res = subprocess.run(cmd, check=True, shell=new_shell, universal_newlines=True, **self.subprocess_args(True))
        except Exception as e:
            #print(e)
            return False

        if res.returncode == 0:
            result = res.stdout
            if clear_data == True:
                result = result.replace('\r', '')
                result = result.replace('\n', '')
            return result
        else:
            return False


    ## Normal methods for pyinstaller with console
    def executeCMDOriginal(self, cmd, clear_data=True):
        res = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)

        if res.returncode == 0:
            result = res.stdout
            if clear_data == True:
                result = result.replace('\r', '')
                result = result.replace('\n', '')
            return result
        else:
            return False