import os
import sublime
import sublime_plugin
import subprocess
import functools
import os.path
import time
import re
import sys

class ListGemsCommand(sublime_plugin.WindowCommand):
    """
    A command that shows a list of all installed gems (by bundle list command)
    """
    PATTERN_GEM = "\* (.+) \("
    GEMS_NOT_FOUND = 'Gems Not Found'
    
    def run(self):        
        output = self.rvm_subprocess("bundle list").split('\n')
        gems = []
        for line in output:
            gem_name = re.search(self.PATTERN_GEM, line)
            if gem_name != None:
                gems.append(gem_name.group(1))

        if gems == []:
            gems.append(self.GEMS_NOT_FOUND)
        
        self.gem_list = gems
        self.window.show_quick_panel(self.gem_list, self.on_done)

    def on_done(self, picked):
      if self.gem_list[picked] != self.GEMS_NOT_FOUND:
          bashCommand = "bundle show " + self.gem_list[picked]
          output = self.rvm_subprocess(bashCommand)
          self.sublime_command_line(['-n', output.rstrip()]) 

    def get_sublime_path(self):
        if sublime.platform() == 'osx':
            return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    def rvm_subprocess(self, args):
       
        executable = self.rvm_shell_path()
        if executable != False:
            current_path = os.path.dirname(self.window.active_view().file_name())
            args = 'cd ' + current_path + ';' + args
            process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True, executable= executable)
            return process.communicate()[0]

    #return rvm shell path or False
    def rvm_shell_path(self):
        rvm_shell = subprocess.Popen(" if [ -f $HOME/.rvm/bin/rvm-shell ]; then echo $HOME/.rvm/bin/rvm-shell; fi", stdout=subprocess.PIPE, shell=True)
        rvm_shell_path = rvm_shell.communicate()[0].rsplit()[0]
        if rvm_shell_path != '':
            return rvm_shell_path.split('\n')[0]
        return False

    def sublime_command_line(self, args):
        args.insert(0, self.get_sublime_path())
        return subprocess.Popen(args)





