import os
import os.path
import sublime
import sublime_plugin
import subprocess
import re
import sys

class ListGemsCommand(sublime_plugin.WindowCommand):
    """
    A command that shows a list of all installed gems (by bundle list command)
    """
    PATTERN_GEM_VERSION = "\* (.*)"
    PATTERN_GEM_NAME = "(.*)\("
    GEMS_NOT_FOUND = 'Gems Not Found'
    
    def run(self):        
        output = self.rvm_subprocess("bundle list").split('\n')
        gems = []
        for line in output:
            gem_name_version = re.search(self.PATTERN_GEM_VERSION, line)
            if gem_name_version != None:
                gems.append(gem_name_version.group(1))

        if gems == []:
            gems.append(self.GEMS_NOT_FOUND)

        self.gem_list = gems
        self.window.show_quick_panel(self.gem_list, self.on_done)

    def on_done(self, picked):
        if self.gem_list[picked] != self.GEMS_NOT_FOUND and picked != -1:
            gem_name = re.search(self.PATTERN_GEM_NAME,self.gem_list[picked]).group(1)
            bashCommand = "bundle show " + gem_name
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
            current_path = self.window.folders()[0]
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





