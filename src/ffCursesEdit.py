'''
Classes partaining to the edditing of newsfeeds
'''
import urwid
import ffCursesClasses

blank = urwid.Divider()
blank1 = urwid.AttrMap(blank, 'fbbody1')

class ffChannelInfoDialog(urwid.WidgetWrap):
	#Dialog allowing the editing of feed information and saving (should check for errors)
	def deleteSource(self, button):
		pass

	def addSource(self, button):
		#go through dialog,
		#generate source
		print('kesi')
		pass

	def saveCh(self):
		pass

	def cancelCh(self):
		pass

	def populateEntries(self, ffChannel):
		#create display with editable options for self.channel and return listbox of it

		#attributes of a cannel are:
		#Title -- name of channel
		#Sources -- list of ffSources
		#	-Each source has:
		#		Name
		#		Adress
		#		Type
		#addSource button
		#Save and Cancel Changes buttons

		titleEdit = urwid.AttrMap(urwid.Edit('TITLE:' , self.channel.title), 'fbbody0')
		sourcesListText = []
		i = 0
		for source in self.channel.sources:
			#add source to sources display
			sourcesListText += [ urwid.Padding(urwid.LineBox(urwid.Pile(
				[urwid.AttrMap(urwid.Text('SOURCE ' + str(i), 'center'), 'fbbody1' ),
				blank1,
				urwid.AttrMap(urwid.Edit('NAME:', source.name), 'fbbody0'),
				blank1,
				urwid.AttrMap(urwid.Edit('ADRESS:', source.adress), 'fbbody0'),
				blank1,
				urwid.AttrMap(urwid.Edit('TYPE:', str(source.type)), 'fbbody0')]
				)), align='center', width=('relative', 90))]
			i += 1


		addSourceButton = urwid.AttrMap(ffCursesClasses.ffIdButton('ADD SOURCE', self.addSource), 'fbbody0')
		deleteSourceButton = urwid.AttrMap(ffCursesClasses.ffIdButton('DELETE SOURCE', self.deleteSource), 'fbbody0')
		saveCancelB = urwid.AttrMap(urwid.Columns([
												('weight',5, addSourceButton),
												('weight',1, blank1),
												('weight',5, deleteSourceButton),
												('weight',1, blank1),
												('weight',5, self.saveB),
												('weight',1, blank1),
												('weight',5, self.cancelB),
												]), 'fbbody0')

		return urwid.AttrMap(urwid.Padding(urwid.AttrMap(urwid.LineBox(urwid.ListBox(
							[
							urwid.LineBox(urwid.Text( 'EDIT CHANNEL ATTRIBUTES:','center')),
							blank1,
							titleEdit,
							blank1,]
							+sourcesListText
							+[urwid.LineBox(saveCancelB)])), 'fbbody1' ), align='center', width=('relative', 50)), 'fbbody0')

	def __init__(self, ffFeedViewer, changeView):
		self.channel = ffFeedViewer.channel
		#change view function
		self.changeView = changeView
		#bind save and cancel buttons
		self.saveB = ffCursesClasses.ffIdButton('SAVE CHANGES', self.saveCh)
		self.cancelB = ffCursesClasses.ffIdButton('CANCEL CHANGES', self.cancelCh)

		#populate dialog
		self.screen = self.populateEntries(self.channel)
		super(ffChannelInfoDialog, self).__init__(self.screen)

class ffEditDialog(urwid.WidgetWrap):
	#Dialog for editing an existing feed or adding a new feed
	#=start
	#choose a feed to edit | ffFeedSelector with some minor modifications (newFeed Option)
	#feed info dialog | ffFeedInfoDialog
	#=write
	#back to choose a feed
	a = 'a'
