import urwid
import urwid.raw_display
import urwid.web_display

blank = urwid.Divider()

class ffCUI(urwid.WidgetWrap):
	'''
	Top most widget, contains all elements on screen
	'''
	def __init__(self):
		#super(ffUI, self).__init__(urwid.Columns())
		pass

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
	def __init__(self, label, signal, user_data='', id=-1):
		self.id = id
		super(ffIdButton, self).__init__(label, signal)
		#change display widget from default thingie

		self._w = urwid.AttrMap(urwid.SelectableIcon(
            label, 2), None, 'body')
def generateEntrybox(ffEntry):
	'''
	generate and return a summary of the news article with relevant information and a button
	to visit the website
	'''
	newsbox_content = []
	possibleFields = []

	#add title atribute
	for field in ffEntry.data.keys():
		#add description atribute
		try:
			newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(ffEntry.data[field], align='center', wrap='space'), 'fbbody0' ), align='center',width=('relative', 80) ),]
		except:
			pass	

	newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(ffEntry.source, align='center', wrap='space'), 'fbbody0' ), align='center',width=('relative', 80) ), ]
	return urwid.AttrWrap(urwid.ListBox(newsbox_content), 'fbbody0')


def generateFeedbox(ffEntries, binding, offset=False):
	'''
	Return urwid ListBox with list Walker containing the titles of Entries
	'''
	i = 0
	colors = ['fbbody0', 'fbbody1'] 
	feedbox_content = []
	for entry in ffEntries:
			#item = FeedItemWidget(i, entry.data.title, select_article, entry)
			item = urwid.AttrMap(ffIdButton(entry.data.title, binding, id=i), colors[i%2])
			feedbox_content.append(item)
			i+=1

	walker = urwid.SimpleListWalker(feedbox_content)
	feedbox = urwid.ListBox(walker)
	return urwid.Frame(feedbox)

class ffFeedViewer(urwid.WidgetWrap):
	'''
	Feed view and display entry data for a datafeed
	'''
	def switchFocus(self, button):
		self.entrybox = generateEntrybox(self.channel.entries[button.id])
		self._w = urwid.Columns([('weight', 7, self.feedbox),('weight', 3, self.entrybox)])

	def __init__(self, ffChannel):
		self.channel = ffChannel
		self.feedbox = generateFeedbox(self.channel.entries, self.switchFocus)
		self.entrybox = generateEntrybox(ffChannel.entries[0])
		super(ffFeedViewer, self).__init__(urwid.Columns([('weight', 7, self.feedbox),('weight', 3, self.entrybox)]))