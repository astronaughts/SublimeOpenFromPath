import sublime
import sublime_plugin
import sys
import os
import subprocess


history = []


def get_sublime_path():
    if sublime.platform() == 'osx':
        return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
    if sublime.platform() == 'linux':
        return open('/proc/self/cmdline').read().split(chr(0))[0]
    return sys.executable


def sublime_command_line(args):
    args.insert(0, get_sublime_path())
    return subprocess.Popen(args)


def open_given(window, path):
    p = os.path.expanduser(path)
    if os.path.isdir(p):
        sublime_command_line(['-a', p])
    else:
        window.open_file(path)


class OpenFromPathCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.window().show_input_panel(
            'Open from ...',
            history[0] if history else '',
            self.open,
            None,
            None,
        )

    def open(self, path):
        try:
            open_given(self.view.window(), path)
            history.append(path)
        except Exception as e:
            sublime.error_message('OpenFromPath [Error]: Could not open this file. ' + e.message)


class OpenFromHistoryCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if not history:
            sublime.error_message('OpenFromPath [Error]: There is no history.')
            return

        summary = [item.strip()[:100] for item in history]
        self.view.window().show_quick_panel(summary, self.open)

    def open(self, index):
        try:
            if not history:
                return
            open_given(self.view.window(), history[index])
        except Exception:
            sublime.error_message('OpenFromPath [Error]: Could not open this file.')
