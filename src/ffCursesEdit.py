'''
Classes partaining to the edditing of newsfeeds
'''
import urwid
import ffCursesClasses

blank = urwid.Divider()

class ffChannelInfoDialog(urwid.WidgetWrap):
	#Dialog allowing the editing of feed information and saving (should check for errors)
	
	def addSource(self):
		#go through dialog,
		#generate source
		print('kesi')
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

		titleEdit = urwid.Edit('TITLE:\t' , self.channel.title)
		sourcesListText = []
		for source in self.channel.sources:
			#add source to sources display
			sourcesListText += [
				urwid.Edit('NAME:\t', source.name),
				blank,
				urwid.Edit('ADRESS:\t', source.adress),
				blank,
				urwid.Edit('TYPE:\t', str(source.type)),
				blank,
				blank,
			]

		addSourceButton = ffCursesClasses.ffIdButton('Add Source', self.addSource)

		saveCancelB = urwid.Columns([('weight',5,self.saveB ), ('weight',1, blank),('weight',5 ,self.cancelB)])

		return urwid.ListBox(
							[titleEdit,
							blank,]
							+sourcesListText
							+[addSourceButton, blank, saveCancelB])


	def saveCh(self):
		pass

	def cancelCh(self):
		pass

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