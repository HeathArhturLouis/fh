import urwid
import urwid.raw_display
import urwid.web_display
import ffClasses
import sys

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

#updated to contain entries in the feed
feedbox = None


class ItemWidget (urwid.WidgetWrap):
	'''
	item widget for menus
	'''
	def __init__ (self, id, description, offset=False):
		self.colors = ['body0', 'body1']
		self.id = id
		self.content = '%s: %s...' % (str(id), description[:25])
		self.item = urwid.AttrWrap(urwid.Text('%s: %s' % (str(id), description)), self.colors[(id+int(offset)) % 2], 'focus')
		self.__super.__init__(self.item)

	def selectable (self):
		return True

	def keypress(self, size, key):
		return key


class FeedItemWidget (ItemWidget):
	def __init__ (self, id, description, entry, offset=False):
		self.entry = entry
		self.__super.__init__(id, description, offset=offset)


	def keypress(self, size, key):
#TODO: REMOVE THIS AND PUT SOMETHING THAT OPENS CONTENT
		if(key=='enter'):
			sys.exit()
		return key


def dummy_button_press( argument ):
	pass

def unhandled(key):
	if key == 'esc' or key == 'q':
		raise urwid.ExitMainLoop()

def populateFeedbox(ffEntries, offset=False):
	'''
	Return urwid ListBox with list Walker containing the titles of Entries
	'''
	i = 0
	colors = ['body0', 'body1'] 
	feedbox_content = []

	for entry in ffEntries:
		item = FeedItemWidget(i, entry.data.title, entry)
		feedbox_content.append(item)
		i+=1

	walker = urwid.SimpleListWalker(feedbox_content)
	feedbox = urwid.ListBox(walker)
	'''
	def update():
		focus = listbox.get_focus()[0].content
		view.set_header(urwid.AttrWrap(urwid.Text('selected: %s' % str(focus)), 'head'))

	urwid.connect_signal(walker, 'modified', update)
	'''
	return feedbox


def channelFeedbox(ffChannel):
	'''
	generate and return ListBox for ffChannel
	'''
	ffChannel.update()
	return populateFeedbox(ffChannel.entries)


def elementNewsbox(ffElement):
	'''
	generate and return a summary of the news article with relevant information and a button
	to visit the website
	'''
	newsbox_content = []





########################################MAIN##################################

def main():

	urwid.web_display.set_preferences("Urwid Tour")
	# try to handle short web requests quickly
	if urwid.web_display.handle_short_request():
		return


	newChannel = ffClasses.ffChannel('Testing Channel')
	newChannel.addSourceAdress('https://hnrss.org/newest', ffClasses.ffSource.ffSourceT.RSS)
	newChannel.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffClasses.ffSource.ffSourceT.RSS)

	newChannel.update()
	
	feedbox = channelFeedbox(newChannel)

	#####################PERMANENT FEATURES###################

	frame = urwid.Frame(urwid.AttrWrap(feedbox, 'body'))

	# use appropriate Screen class
	if urwid.web_display.is_web_request():
		screen = urwid.web_display.Screen()
	else:
		screen = urwid.raw_display.Screen()

	urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()

if __name__ == '__main__':
	main()

