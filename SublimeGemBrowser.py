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
        output = self.rvm_subprocess("bundle list")
        if output != None:
          gems = []
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
            bashCommand = "bundle show " + gem_name
            output = self.rvm_subprocess(bashCommand)
            if output != None:
                self.sublime_command_line(['-n', output.rstrip()]) 

    def get_sublime_path(self):
        if sublime.platform() == 'osx':
            return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    def rvm_subprocess(self, args):
       
        executable = self.ruby_environment()
        current_path = self.gemfile_folder()
        if executable != False and current_path != None:
            args = 'cd ' + current_path + ';' + args
            process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True, executable= executable)
            return process.communicate()[0]
        return None
    #return rvm shell path or False
    def ruby_environment(self):
        rvm_shell = subprocess.Popen(" if [ -f $HOME/.rvm/bin/rvm-shell ]; then echo $HOME/.rvm/bin/rvm-shell; fi", stdout=subprocess.PIPE, shell=True)
        rvm_shell_path = rvm_shell.communicate()[0]
        if rvm_shell_path != '':
            return rvm_shell_path.rsplit()[0].split('\n')[0]
        return False

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







