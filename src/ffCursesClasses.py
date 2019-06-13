import urwid
import urwid.raw_display
import urwid.web_display
import regex as re
from urllib.parse import urlparse

import os
import subprocess


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
	def __init__(self, label, signal, user_data='', uri='', id=-1):
		self.id = id
		self.uri = uri
		super(ffIdButton, self).__init__(label, signal)
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
#	newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(cleanhtml(ffEntry.source), lambda x: None , id='source'), 'fbbody0' ), align='center',width=('relative', 80) ), ]

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
	return urwid.Frame(feedbox)

class ffFeedViewer(urwid.WidgetWrap):
	'''
	Feed view and display entry data for a datafeed
	'''

	def visitAdress(self, button):
#todo: config this command somewhare lol
		#execute command:
		#redicrect output to stop annoying echo
		FNULL = open(os.devnull, 'w')
		subprocess.run(["chromium", 'https://outline.com/' + button.uri], stdout=FNULL, stderr=FNULL)

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


	def __init__(self, ffChannel):
		#keep track of last entry pressed for double click
		self.lastSelected = -1

		self.channel = ffChannel
		self.feedbox = generateFeedbox(self.channel.entries, self.entrySelectPress)
		self.entrybox = generateEntrybox(ffChannel.entries[0], self.visitAdress)
		super(ffFeedViewer, self).__init__(urwid.Columns([('weight', 7, self.feedbox),('weight', 3, self.entrybox)]))

