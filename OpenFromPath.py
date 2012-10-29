import sublime
import sublime_plugin
import os.path

history = []

class OpenFromPathCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        panel = self.view.window().show_input_panel(
            'Open from ...',
            history[0] if history else '',
            self.open,
            None,
            None,
        )

    def open(self, path):
        try:
            self.view.window().open_file(path)
            history.append(path)
        except Exception as e:
            sublime.error_message('OpenFromPath [Error]: Could not open this file.')

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

            self.view.window().open_file(history[index])
        except Exception as e:
            sublime.error_message('OpenFromPath [Error]: Could not open this file.')