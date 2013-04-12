import os
import os.path
import sublime
import sublime_plugin
import subprocess
import re
import sys
import fnmatch

class ListGemsCommand(sublime_plugin.WindowCommand):
    """
    A command that shows a list of all installed gems (by bundle list command)
    """
    PATTERN_GEM_VERSION = "\* (.*)"
    PATTERN_GEM_NAME = "(.*)\("
    GEMS_NOT_FOUND = 'Gems Not Found'
    
    def run(self):        
        self.app_path_mac = None
        output = self.run_subprocess("bundle list")
        if output != None:
          gems = []

          if sys.version_info < (3, 0):
            output = str(output)
          else:
            output = str(output, encoding = 'utf-8')

          for line in output.split('\n'):
              gem_name_version = re.search(self.PATTERN_GEM_VERSION, line)
              if gem_name_version != None:
                  gems.append(gem_name_version.group(1))

          if gems == []:
              gems.append(self.GEMS_NOT_FOUND)

          self.gem_list = gems
          self.window.show_quick_panel(self.gem_list, self.on_done)
        else:
          sublime.error_message('Error getting the output, the shell could probably not be loaded or There are no Gemfile in this project.')
    
    def on_done(self, picked):
        if self.gem_list[picked] != self.GEMS_NOT_FOUND and picked != -1:
            gem_name = re.search(self.PATTERN_GEM_NAME,self.gem_list[picked]).group(1)
            output = self.run_subprocess("bundle show " + gem_name)
            if output != None:
                self.sublime_command_line(['-n', output.rstrip()]) 

    def get_sublime_path(self):
        if sublime.platform() == 'osx':
            if not self.app_path_mac:
                # taken from https://github.com/freewizard/SublimeGotoFolder/blob/master/GotoFolder.py:
                from ctypes import cdll, byref, Structure, c_int, c_char_p, c_void_p
                from ctypes.util import find_library
                Foundation = cdll.LoadLibrary(find_library('Foundation'))
                CFBundleGetMainBundle = Foundation.CFBundleGetMainBundle
                CFBundleGetMainBundle.restype = c_void_p
                bundle = CFBundleGetMainBundle()
                CFBundleCopyBundleURL = Foundation.CFBundleCopyBundleURL
                CFBundleCopyBundleURL.argtypes = [c_void_p]
                CFBundleCopyBundleURL.restype = c_void_p
                url = CFBundleCopyBundleURL(bundle)
                CFURLCopyFileSystemPath = Foundation.CFURLCopyFileSystemPath
                CFURLCopyFileSystemPath.argtypes = [c_void_p, c_int]
                CFURLCopyFileSystemPath.restype = c_void_p
                path = CFURLCopyFileSystemPath(url, c_int(0))
                CFStringGetCStringPtr = Foundation.CFStringGetCStringPtr
                CFStringGetCStringPtr.argtypes = [c_void_p, c_int]
                CFStringGetCStringPtr.restype = c_char_p
                self.app_path_mac = CFStringGetCStringPtr(path, 0)
                CFRelease = Foundation.CFRelease
                CFRelease.argtypes = [c_void_p]
                CFRelease(path)
                CFRelease(url)
            return self.app_path_mac.decode() + '/Contents/SharedSupport/bin/subl'
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    def run_subprocess(self, command):
        current_path = self.gemfile_folder()
        if current_path == None: return None
        command_with_cd = 'cd ' + current_path + ' && ' + command

        # Search for RVM
        shell_process = subprocess.Popen(" if [ -f $HOME/.rvm/bin/rvm-auto-ruby ]; then echo $HOME/.rvm/bin/rvm-auto-ruby; fi", stdout=subprocess.PIPE, shell=True)
        rvm_executable = shell_process.communicate()[0].rstrip()
        
        if rvm_executable != '':
            rvm_command = 'cd ' + current_path + ' && $HOME/.rvm/bin/rvm-auto-ruby -S ' + command
            process = subprocess.Popen(rvm_command, stdout=subprocess.PIPE, shell=True)
            return process.communicate()[0]
        else: #Search for rbenv
            rbenv_command = 'cd ' + current_path + ' && ~/.rbenv/shims/' + command
            process = subprocess.Popen(rbenv_command, stdout=subprocess.PIPE, shell=True)
            output = process.communicate()[0]
            if output != '':
              return output
            else: # Try for a windows output
              process = subprocess.Popen(command_with_cd, stdout=subprocess.PIPE, shell=True)
              output = process.communicate()[0]
              if output != '':
                  return output
    def sublime_command_line(self, args):
        args.insert(0, self.get_sublime_path())
        return subprocess.Popen(args)

    def gemfile_folder(self):
        root = self.window.folders()[0]
        matches = []
        for root, dirnames, filenames in os.walk(root):
            for filename in fnmatch.filter(filenames, 'Gemfile'):
                matches.append(os.path.join(root, filename))
                break
        if matches == []: return None
        return os.path.dirname(matches[0])







