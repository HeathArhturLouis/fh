import urwid
import urwid.raw_display
import urwid.web_display


class LineReader(urwid.WidgetWrap):
    """Widget wraps a text widget only showing one line at the time"""
    def __init__(self, text_lines, current_line=0):
        self.current_line = current_line
        self.text_lines = text_lines
        self.text = urwid.Text('')
        super(LineReader, self).__init__(self.text)

    def load_line(self):
        """Update content with current line"""
        self.text.set_text(self.text_lines[self.current_line])

    def next_line(self):
        """Show next line"""
        # TODO: handle limits
        self.current_line += 1
        self.load_line()

reader = LineReader(list(open('/etc/passwd')))

filler = urwid.Filler(reader)

def handle_input(key):
    if key in ('j', 'enter'):
        reader.next_line()
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop

urwid.MainLoop(filler, unhandled_input=handle_input).run()