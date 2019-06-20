
'''
Classes partaining to the edditing of newsfeeds
'''


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

		titleEdit = urwid.Edit('TITLE' , self.channel.title)
		sourcesListText = []
		for source in self.channel.sources:
			#add source to sources display
			sourcesListText += urwid.ListBox([
								urwid.Edit('NAME:', source.name),
								blank,
								urwid.Edit('TITLE:', source.title),
								blank,
								urwid.Edit('TYPE:', source.type),
								])

		addSourceButton = ffIdButton('Add Source', addSource)

		saveCancelB = urwid.Columns([('weight',5,self.saveB ), ('weight', 1, blank),('weight',5 ,self.cancelB)])


	def saveCh():
		pass

	def cancelCh():
		pass

	def __init__(self, ffChannel, changeView):
		self.channel = ffChannel
		#change view function
		self.changeView = changeView
		#bind save and cancel buttons
		self.saveB = ffIdButton('SAVE CHANGES', self.saveCh)
		self.cancelB = ffIdButton('CANCEL CHANGES', self.cancelCh)

		#populate dialog
		self.screen = populateEntries()
		super(ffCUI, self).__init__(self.screen)



class ffEditDialog(urwid.WidgetWrap):
	#Dialog for editing an existing feed or adding a new feed
	#=start
	#choose a feed to edit | ffFeedSelector with some minor modifications (newFeed Option)
	#feed info dialog | ffFeedInfoDialog
	#=write
	#back to choose a feed
	a = 'a'