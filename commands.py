# https://www.sublimetext.com/docs/3/api_reference.html
import sublime
import sublime_plugin

import os
import sys
import webbrowser
from subprocess import call
from urllib.parse import urlparse


def check_sublime_version():
    if sys.version_info[0] < 3:
        raise ImportWarning("UrlOpener doesn't support Sublime Text 2")


def prepend_scheme(s):
    o = urlparse(s)
    if not o.scheme:
        s = 'http://' + s
    return s


class UrlOpenerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Open file/directory locally if one exists, or open URL with webbrowser.
        """
        check_sublime_version()
        self.config = sublime.load_settings('UrlOpener.sublime-settings')
        start, end = self.get_selection_boundaries()
        url = self.view.substr(sublime.Region(start, end)).strip()
        path = self.abs_path(url)

        if os.path.isdir(path):
            call(['open', path])
            return

        if os.path.isfile(path):
            self.view.window().open_file(path)
            return

        url = prepend_scheme(url)
        return webbrowser.open(url)

    def get_selection_boundaries(self):
        """Returns start and end indices of selection. If selection contains no
        characters, expand it until hitting delimeter chars.
        """
        s = self.view.sel()[0]

        start = s.begin()
        end = s.end()

        if start != end:
            return start, end

        # nothing is selected, so expand selection to nearest delimeters
        view_size = self.view.size()
        delimeters = list(self.config.get('delimeters'))

        # move the selection back to the start of the url
        while start > 0:
            if self.view.substr(start - 1) in delimeters:
                break
            start -= 1

        # move end of selection forward to the end of the url
        while end < view_size:
            if self.view.substr(end) in delimeters:
                break
            end += 1
        return start, end

    def abs_path(self, path):
        """Converts `path` into absolute path and returns it.
        """
        if os.path.isabs(path):
            return path

        file_path = self.view.file_name()
        if file_path:
            return os.path.join(os.path.dirname(file_path), path)

        project = self.view.window().project_data()
        if project is not None:
            try:
                return os.path.join(project['folders'][0]['path'], path)
            except (KeyError, IndexError):
                return path

        return path
