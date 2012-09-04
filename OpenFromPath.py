import sublime
import sublime_plugin
import os.path

class OpenCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel('Path:', '', self.open, None, None)

    def open(self, path):

        try:
            if not os.path.isfile(path):
                raise IOError1

            self.window.open_file(path)
        except:
            sublime.error_message('OpenFromPath Error: Could not open this file.')