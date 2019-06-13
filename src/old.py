import urwid
import urwid.raw_display
import urwid.web_display
import ffClasses
import sys

#Ugly fixes with global vars
frame = None
screen = None
#index of current news article being displayed
index = 0

blank = urwid.Divider()

palette = [
	('body','black','light gray', 'standout'),
	('body0', 'light gray', 'black',  'standout'),
	('body1', 'light gray', 'dark gray', 'standout'),
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


def update_main_display():
	global frame
	global screen
	global index
	urwid.ExitMainLoop()
	frame.changeEntryBox(frame.channel.entries[index])
	urwid.MainLoop(frame.frame, palette, screen, unhandled_input=unhandled).run()

def select_article(button):
	update_main_display()

def unhandled(key):
	if(key=='esc' or key=='q'):
		urwid.ExitMainLoop()
		sys.exit()
	return key
	'''
	global frame
	global screen

	urwid.ExitMainLoop()	
	urwid.MainLoop(frame.frame, palette, screen, unhandled_input=unhandled).run()
	'''

class ItemWidget (urwid.Button):
	'''
	item widget for menus
	'''
	def __init__ (self, id, description, signal, offset=False):
		self.colors = ['body0', 'body1']
		self.id = id
		self.content = '%s: %s...' % (str(id), description[:25])
		self.item = urwid.AttrWrap(urwid.Text('%s: %s' % (str(id), description), align='left', wrap='clip'), self.colors[(id+int(offset)) % 2], 'focus')
		self.__super.__init__(description, signal)

	def selectable (self):	
		return True
	def keypress(self, size, key):
		return key

class FeedItemWidget(ItemWidget):
	def __init__ (self, id, description, signal,  entry, offset=False):
		self.entry = entry
		self.__super.__init__(id, description, signal, offset=offset)

	def keypress(self, size, key):
	#TODO: REMOVE THIS AND PUT SOMETHING THAT OPENS CONTENT
	#DONE: REAL UGLY GLOBAL VARIABLE HACK; GLOBAL VARS CONSIDERED HARMFULL
		if(key=='enter'):
			#frame.entrybox = urwid.Frame(urwid.AttrWrap(frame.generateEntrybox(frame.channel.entries[0], 0), 'body'))
			#frame.frame = urwid.Columns([ ( 'weight', 7 ,frame.feedbox) , ('weight', 3, frame.entrybox)])
			pass
		return key


class ffMainFeed:
	'''
	holds and handles updates/input to a feedbox and entrybox pair
	'''
	#----------------------DATA--------------------

	#updated to contain entries in the feed
	feedbox = None
	
	#contains infomation about selected entry in feed
	entrybox = None

	#feed currently being tracked
	channel = None

	#Highest level widget to be displayed
	frame = None

	#-----------------------METHODS---------------------------

	def input_filter(self, keys, raw):
		global index
		for key in keys:
			if(key=='up'):
				index -= 1
			if(key=='down'):
				index += 1
		return keys

	def populateFeedbox(self, ffEntries, offset=False):
		'''
		Return urwid ListBox with list Walker containing the titles of Entries
		'''
		i = 0
		colors = ['body0', 'body1'] 
		feedbox_content = []

		for entry in ffEntries:
				#item = FeedItemWidget(i, entry.data.title, select_article, entry)
				item = urwid.Button(entry.data.title, select_article)
				feedbox_content.append(item)
				i+=1

		walker = urwid.SimpleListWalker(feedbox_content)
		feedbox = urwid.ListBox(walker)

		return feedbox


	def generateFeedbox(self, ffChannel):
		'''
		generate and return ListBox for ffChannel
		'''
		ffChannel.update()
		return self.populateFeedbox(ffChannel.entries)


	def generateEntrybox(self, ffEntry, entryIndex):
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
				newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(ffEntry.data[field], align='center', wrap='space'), 'body0' ), align='center',width=('relative', 80) ),]
			except:
				pass	

		newsbox_content += [blank, urwid.Padding(urwid.AttrWrap( urwid.Text(ffEntry.source, align='center', wrap='space'), 'body0' ), align='center',width=('relative', 80) ), ]
		return urwid.ListBox(newsbox_content)

	def __init__(self, ffChannel):
		self.channel = ffChannel
		#initialize feed and entry boxes
		self.feedbox = urwid.Frame(urwid.AttrWrap(self.generateFeedbox(ffChannel), 'body'))
		self.entrybox = urwid.Frame(urwid.AttrWrap(self.generateEntrybox(ffChannel.entries[0], 0), 'body'))

		self.frame = urwid.Columns([ ( 'weight', 7 ,self.feedbox) , ('weight', 3, self.entrybox)])

	def changeEntryBox(self, ffEntry):
		self.entrybox = urwid.Frame(urwid.AttrWrap(self.generateEntrybox(ffEntry, 0), 'body'))
		self.frame = urwid.Columns([ ( 'weight', 7 ,self.feedbox) , ('weight', 3, self.entrybox)])

	def updateEntryBox(self):
		global index
		self.changeEntryBox(self.entries[index])

	def getFrame(self):
		return self.frame

########################################MAIN##################################

def main():
	global frame
	global screen
	global index

	urwid.web_display.set_preferences("Urwid Tour")
	# try to handle short web requests quickly
	if urwid.web_display.handle_short_request():
		return

	def button_press(button):
		select_article(button)

	newChannel = ffClasses.ffChannel('Testing Channel')
	newChannel.addSourceAdress('https://hnrss.org/newest', ffClasses.ffSource.ffSourceT.RSS)
	newChannel.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffClasses.ffSource.ffSourceT.RSS)
	newChannel.addSourceAdress('https://feedpress.me/drudgereportfeed', ffClasses.ffSource.ffSourceT.RSS)

	newChannel.update()

	#####################PERMANENT FEATURES###################

	# use appropriate Screen class
	if urwid.web_display.is_web_request():
		screen = urwid.web_display.Screen()
	else:
		screen = urwid.raw_display.Screen()

	feedbox = 
	entrybox = 

	frame = urwid.Columns([ ( 'weight', 7 ,feedbox) , ('weight', 3, self.entrybox)])

	urwid.MainLoop(frame, palette, screen, input_filter=input_filter , unhandled_input=unhandled).run()

if __name__ == '__main__':
	main()

