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
        os.chdir(os.path.dirname(self.window.active_view().file_name()))
        bashCommand = "bundle list "
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
        output = process.communicate()[0]
        output = output.split('\n')
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
          process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,shell=True)
          output = process.communicate()[0]
          self.sublime_command_line(['-n', output.rstrip()]) 

    def get_sublime_path(self):
        if sublime.platform() == 'osx':
            return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
        if sublime.platform() == 'linux':
            return open('/proc/self/cmdline').read().split(chr(0))[0]
        return sys.executable

    def sublime_command_line(self, args):
        args.insert(0, self.get_sublime_path())
        print args
        return subprocess.Popen(args)





