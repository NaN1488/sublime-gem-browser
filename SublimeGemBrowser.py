import os
import sublime
import sublime_plugin
import subprocess
import functools
import os.path
import time
import re

class ListGemsCommand(sublime_plugin.WindowCommand):
    """
    A command that shows a list of all installed gems (by bundle list command)
    """
    
    def run(self):
        os.chdir(os.path.dirname(self.window.active_view().file_name()))
        bashCommand = "bundle list "
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        output = output.split('\n')
        gems = []
        for line in output:
            gem_name = re.search("\* (.+) \(", line)
            if gem_name != None:
                gems.append(gem_name.group(1))

        if gems == []:
            gems.append('Gems Not Found')
        
        self.gem_list = gems
        self.window.show_quick_panel(self.gem_list, self.on_done)

    def on_done(self, picked):
      print 'Ok'