import urwid
import urwid.raw_display
import urwid.web_display
import regex as re
from urllib.parse import urlparse
import ffClasses
import ffCursesEdit
import pickle

import os
import subprocess


'''
Path to file with pickled list of ffChannels
'''
ffFilePath = '../data/channels.pkl'


blank = urwid.Divider()

###################TOOLS####################
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext



def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False



#############################################

class ffFeedBox(urwid.WidgetWrap):
    def __init__(self):
        pass


class ffEntryBox(urwid.WidgetWrap):
    def __init__(self):
        pass

class ffIdButton(urwid.Button):
    '''
    Clas for buttons in feed menu, id: the id of the button in the channel
    presumably this is what user_data is but the documentation struck me as unclear
    '''
    def __init__(self, label, signal, user_data='', uri='', id=-1):
        self.id = id
        self.uri = uri
        super(ffIdButton, self).__init__(label, signal)
        #change display widget from default thing

        self._w = urwid.AttrMap(urwid.SelectableIcon(
            label, 2), None, 'body')

class ffChannelButton(urwid.Button):
    '''
    Button used in menu for selecting channel to display/edit
    '''
    def __init__(self, label, signal, channel, user_data=''):
        self.channel = channel
        super(ffChannelButton, self).__init__(label, signal)
        #change display widget from default thing

        self._w = urwid.AttrMap(urwid.SelectableIcon(
            label, 2), None, 'body')



def generateEntrybox(ffEntry, uribinding):
    '''
    Return entrybox of buttons
    '''
    newsbox_content = []
    possibleFields = []

    #add title atribute
    for field in ffEntry.data.keys():
        #add description atribute
        try:
            if(uri_validator(ffEntry.data[field])):
                #,make button
                newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( ffIdButton(cleanhtml(ffEntry.data[field]), uribinding, id='field', uri=cleanhtml(ffEntry.data[field])), 'fbbody0' ), align='center',width=('relative', 80) ), ]
            else:
                newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(cleanhtml(ffEntry.data[field])), 'fbbody0' ), align='center',width=('relative', 80) ),]
        except:
            pass

    newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(cleanhtml(ffEntry.source)), 'fbbody0'), align='center',width=('relative', 80) ), ]
#    newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(cleanhtml(ffEntry.source), lambda x: None , id='source'), 'fbbody0' ), align='center',width=('relative', 80) ), ]

    walker = urwid.SimpleListWalker(newsbox_content)

    return urwid.Frame(urwid.AttrWrap(urwid.ListBox(walker), 'fbbody0'))


def generateFeedbox(ffEntries, binding, offset=False):
    '''
    Return urwid ListBox with list Walker containing the titles of Entries
    '''
    i = 0
    colors = ['fbbody0', 'fbbody1']
    feedbox_content = []
    for entry in ffEntries:
            if('link' in entry.data):
                link = entry.data.link
            else:
                link=None
            #item = FeedItemWidget(i, entry.data.title, select_article, entry)
            item = urwid.AttrMap(ffIdButton(entry.data.title, binding, id=i, uri=entry.data.link), colors[i%2])
            feedbox_content.append(item)
            i+=1

    walker = urwid.SimpleListWalker(feedbox_content)
    feedbox = urwid.ListBox(walker)

    return urwid.AttrMap(urwid.Frame(feedbox), 'fbbody1')

class ffFeedViewer(urwid.WidgetWrap):
    '''
    Feed view and display entry data for a datafeed
    '''
    def visitAdress(self, button):
#todo: config this command somewhare lol
        #execute command:
        FNULL = open(os.devnull, 'w')
        self.proc = subprocess.run(["chromium", 'https://outline.com/' + button.uri], stdout=FNULL, stderr=FNULL)

    def switchFocus(self, button):
        self.entrybox = generateEntrybox(self.channel.entries[button.id], self.visitAdress)
        self._w = urwid.Columns([('weight', 7, self.feedbox),('weight', 3, self.entrybox)])

    def entrySelectPress(self, button):
        #when an entry has been selected
        if (self.lastSelected == button.id):
            #virtual button with adress
            self.visitAdress(button)
        else:
            self.switchFocus(button)
            self.lastSelected = button.id

    def update(self):
        self.channel.update()

    def changeChannel(self, ffChannel):
        self.lastSelected = -1
        #track subprocess displaying web content
        self.proc = None

        self.channel = ffChannel
        self.feedbox = generateFeedbox(self.channel.entries, self.entrySelectPress)
        self.entrybox = generateEntrybox(ffChannel.entries[0], self.visitAdress)
        self._w = urwid.Columns([('weight', 7, self.feedbox),('weight', 3, self.entrybox)])

    def __init__(self, ffChannel):
        #keep track of last entry pressed for double click
        self.lastSelected = -1
        #track subprocess displaying web content
        self.proc = None

        self.channel = ffChannel
        self.channel.update()
        self.feedbox = generateFeedbox(self.channel.entries, self.entrySelectPress)
        self.entrybox = generateEntrybox(ffChannel.entries[0], self.visitAdress)
        super(ffFeedViewer, self).__init__(urwid.Columns([('weight', 7, self.feedbox),('weight', 3, self.entrybox)]))

class ffFeedSelector(urwid.WidgetWrap):
    '''
    select a feed, then call signal with selected feed as argument
    '''
    def callSignal(self, Button):
        #set view to selected feed
        self.changeView(ffFeedViewer(Button.channel))

    def __init__(self, channels ,signal, changeView):
        self.changeView = changeView
        self.signal = signal
        #list of ffChannels
        self.channels = channels

        buttons = []
        colors = ['fbbody0', 'fbbody1']

        i = 0
        for channel in self.channels:
            buttons += [
                        urwid.AttrMap(ffChannelButton(channel.title, self.callSignal, channel), colors[i%2]),
                    ]
            i += 1

        box = urwid.LineBox(urwid.ListBox( [urwid.LineBox(urwid.AttrMap(urwid.Text('SELECT A CHANNEL:', 'center'), 'fbbody1' )), urwid.LineBox(urwid.AttrMap(urwid.Pile(buttons), colors[1]) )]))
        box = urwid.AttrMap(urwid.Padding( urwid.AttrMap(box, 'fbbody1'), align='center', width=('relative', 50)),'fbbody0')

        super(ffFeedSelector, self).__init__(box)

class ffMenuBar(urwid.WidgetWrap):
    '''
    Main menu bar to be displayed on top of the application, switches between views

    FEEDS | EDIT | OPTIONS buttons
    '''
    def refresh(self, button):
        #are we currently viewing a feed?
        #refresh contents of viewed feed
        if( isinstance(self.getScreen(), ffFeedViewer)):
            #creating viewer automatically updates
            self.changeView(ffFeedViewer(self.getScreen().channel))

    def openFeeds(self, button):
        self.changeView(ffFeedSelector(self.channels, lambda x : x, self.changeView))
    def openEdit(self, button):
        #TODO: Maybe instead of change view we can put method that opens edit dialog
        self.changeView(ffFeedSelector(self.channels ,lambda x : x ,self.openCID))
    def openOptions(self, button):
        pass
    def __init__(self, feeds, changeView,  getScreen, openCID):
        self.channels = feeds
        self.changeView = changeView
        self.getScreen = getScreen
        self.openCID = openCID
        self.buttons = [
                    ('weight',1,blank),
                        ('weight',20,urwid.AttrMap(ffIdButton('REFRESH', self.refresh, 0), 'fbbody1')),
                        ('weight',1,blank),
                        ('weight',20,urwid.AttrMap(ffIdButton('FEEDS', self.openFeeds, 1), 'fbbody1')),
                        ('weight',1,blank),
                        ('weight',20,urwid.AttrMap(ffIdButton('EDIT', self.openEdit, 2), 'fbbody1')),
                        ('weight',1,blank),
                        ('weight',20,urwid.AttrMap(ffIdButton('OPTIONS',self.openOptions, 3), 'fbbody1')),
                        ('weight',1,blank),]
        box = urwid.ListBox([
            blank,
            urwid.Columns(self.buttons),
            blank,
            ])
        #box = urwid.LineBox(box)
        box = urwid.AttrWrap(box, 'fbbody0')
        super(ffMenuBar, self).__init__(box)


class ffCUI(urwid.WidgetWrap):

    def saveChannels(self):
        f = open(ffFilePath, 'wb')
        pickle.dump(self.channels , f)
        f.close()

    def replaceChannel(self, newChannel):
        #check id'ws
        for chan in self.channels:
            if(chan.id == newChannel.id):
                #replace
                chan = newChannel
        #save changes
        self.saveChannels()
        #go back to channel view
        self.options.openEdit()

    def loadChannels(self):
        f = open(ffFilePath, 'rb')
        self.channels = pickle.load(f)
        i = 0
        for ch in self.channels:
            ch.id = i
            ch.update()
        i += 1
        f.close()

    def getCurrent(self):
        return self.screen

    def openEditDialog(self, ffChannel):
        self.changeView(ffCursesEdit.ffChannelInfoDialog(ffChannel, self.changeView, self.replaceChannel))

    def changeView(self, nScreen):
        '''
        change crrent screen widget wth new ine
        '''
        self.screen = nScreen
        self._w = urwid.Pile([(3 , self.options), self.screen])

    #Top most widget, contains all elements on screen
    def __init__(self):
        #start by loading channels
        self.loadChannels()
        #menu up top
        self.options = ffMenuBar(self.channels, self.changeView, self.getCurrent, self.openEditDialog)

        #display down below
        self.channels = []
        #open on first channel
        #self.screen = ffFeedViewer(self.channels[0])
#TODO: COOL TITLE SCREEN
        self.screen = urwid.AttrMap(urwid.SolidFill(), 'fbbody1')

        super(ffCUI, self).__init__(urwid.Pile([(3 , self.options), self.screen]))


'''
        newChannel = ffClasses.ffChannel('Testing Channel')
        newChannel.addSourceAdress('https://hnrss.org/newest', ffClasses.ffSource.ffSourceT.RSS)
        newChannel.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffClasses.ffSource.ffSourceT.RSS)
        newChannel.addSourceAdress('https://feedpress.me/drudgereportfeed', ffClasses.ffSource.ffSourceT.RSS)

        newChannel.update()
'''
