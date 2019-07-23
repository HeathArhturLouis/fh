import urwid
import urwid.raw_display
import urwid.web_display
import sys
import ffCursesClasses
import ffClasses

palette = [
    ('body','black','light gray', 'standout'),
    ('fbbody0', 'light gray', 'black',  'standout'),
    ('fbbody1', 'light gray', 'dark gray', 'standout'),
    ('reverse','light gray','black'),
    ('header','white','dark red', 'bold'),
    ('important','dark blue','light gray',('standout','underline')),
    ('editfc','white', 'dark blue', 'bold'),
    ('editbx','light gray', 'dark blue'),
    ('editcp','black','light gray', 'standout'),
    ('bright','dark gray','light gray', ('bold','standout')),
    ('buttn','black','dark cyan'),
    ('buttnf','white','dark blue','bold'),
    ]

def unhandled(key):
    if(key=='esc' or key=='q'):
        urwid.ExitMainLoop()
        sys.exit()
    #if(key=='enter' or key == 'f'):
    #    global frame
    #    frame.switchFocus
    return key

def input_filter(keys, raw):
    return keys


frame = []

###############################MAIN LOOP######################
def main():
    ###############################################
    ###############################################
    # use appropriate Screen class
    if urwid.web_display.is_web_request():
        screen = urwid.web_display.Screen()
    else:
        screen = urwid.raw_display.Screen()

    def select_article(button):
        '''
        new entry selected
        '''
        #feedbox.footer = urwid.AttrWrap(urwid.Text([u"Pressed: ", button.get_label()]), 'header')
        feedbox.footer = generateEntrybox(newChannel.entries[3], 3)

    #feedbox = ffCursesClasses.ffFeedViewer(newChannel)
    feedbox = ffCursesClasses.ffCUI()
    #feedbox = ffCursesClasses.ffFeedSelector([newChannel, newChannel, newChannel], lambda x : x)

    global frames
    #frame = urwid.Columns([ ( 'weight', 7 , feedbox) , ('weight', 3, entrybox)])
    frame = feedbox


    urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()


if __name__ == '__main__':
    main()
