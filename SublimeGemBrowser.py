import os
import sublime
import sublime_plugin
import threading
import subprocess
import functools
import os.path
import time


class ListGemsCommand(sublime_plugin.WindowCommand):
    """
    A command that shows a list of all installed gems (by bundle list command)
    """

    def run(self):
        ListGemsThread(self.window).start()

class ListGemsThread(threading.Thread, ExistingGemsCommand):
    """
    A thread to prevent the listing of existing packages from freezing the UI
    """

    def __init__(self, window):
        """
        :param window:
            An instance of :class:`sublime.Window` that represents the Sublime
            Text window to show the list of installed gems in.
        """

        self.window = window
        threading.Thread.__init__(self)
        ExistingGemsCommand.__init__(self)

    def run(self):
        """
        self.package_list = self.make_package_list()

        def show_quick_panel():
            if not self.package_list:
                sublime.error_message(('%s: There are no packages ' +
                    'to list.') % __name__)
                return
            self.window.show_quick_panel(self.package_list, self.on_done)
        sublime.set_timeout(show_quick_panel, 10)
        """
    
    def on_done(self, picked):
        """
        Quick panel user selection handler - opens the homepage for any
        selected package in the user's browser

        :param picked:
            An integer of the 0-based package name index from the presented
            list. -1 means the user cancelled.
        """
        """
        if picked == -1:
            return
        package_name = self.package_list[picked][0]

        def open_dir():
            self.window.run_command('open_dir',
                {"dir": os.path.join(sublime.packages_path(), package_name)})
        sublime.set_timeout(open_dir, 10)
        """


class ExistingGemsCommand():
    """
    Allows listing installed packages and their current version
    """

    def __init__(self):

    def make_gems_list(self, action=''):
        """
        Returns a list of installed packages suitable for displaying in the
        quick panel.

        :param action:
            An action to display at the beginning of the third element of the
            list returned for each package

        :return:
            A list of lists, each containing three strings:
              0 - package name
              1 - package description
              2 - [action] installed version; package url
        """
        """  
        if self.working_dir != "":
			os.chdir(self.working_dir)

		proc = subprocess.Popen(self.command,
 			stdout=self.stdout, stderr=subprocess.STDOUT,
 			stdin=subprocess.PIPE,
 			shell=shell, universal_newlines=True)
            output = proc.communicate(self.stdin)[0]

        gems = 

        if action:
            action += ' '

        gems_list = []
        for package in sorted(packages, key=lambda s: s.lower()):
            package_entry = [package]
            metadata = self.manager.get_metadata(package)
            package_dir = os.path.join(sublime.packages_path(), package)

            description = metadata.get('description')
            if not description:
                description = 'No description provided'
            package_entry.append(description)

            version = metadata.get('version')
            if not version and os.path.exists(os.path.join(package_dir,
                    '.git')):
                installed_version = 'git repository'
            elif not version and os.path.exists(os.path.join(package_dir,
                    '.hg')):
                installed_version = 'hg repository'
            else:
                installed_version = 'v' + version if version else \
                    'unknown version'

            url = metadata.get('url')
            if url:
                url = '; ' + re.sub('^https?://', '', url)
            else:
                url = ''

            package_entry.append(action + installed_version + url)
            package_list.append(package_entry)

        return package_list
        """