'''
Classes partaining to the edditing of newsfeeds
'''
import urwid
import ffCursesClasses
import ffClasses

blank = urwid.Divider()
blank1 = urwid.AttrMap(blank, 'fbbody1')

class ffChannelInfoDialog(urwid.WidgetWrap):
	#Dialog allowing the editing of feed information and saving (should check for errors)
	def deleteSource(self, button):
		pass

	def addSource(self, button):
		#go through dialog,
		#generate source
		pass

	def saveCh(self, button):
		#Generate new channel with same Id from provided data
		newChannel = ffClasses.ffChannel(self.titleEdit.base_widget.get_edit_text())
		newChannel.id = self.channel.id


		for source in self.sourcesListText:
#TODO: make sure its a legit url address
			source = source.base_widget
			uri = source[2].base_widget.get_edit_text()
			type = source[4].base_widget.get_edit_text()
			newChannel.addSource(ffClasses.ffSource(uri, type))


	#Send new channel back to CUI to replace with new one
		newChannel.update()
		self.replaceChannel(newChannel)


	def cancelCh(self, button):
		pass

	def populateEntries(self, ffChannel):
		#create display with editable options for self.channel and return listbox of it
		self.titleEdit = urwid.AttrMap(urwid.Edit('TITLE:' , self.channel.title), 'fbbody0')
		self.sourcesListText = []
		i = 0
		for source in self.channel.sources:
			#add source to sources display
			self.sourcesListText += [ urwid.Padding(urwid.LineBox(urwid.Pile(
				[urwid.AttrMap(urwid.Text('SOURCE ' + source.name, 'center'), 'fbbody1' ),
				blank1,
				urwid.AttrMap(urwid.Edit('ADRESS:', source.adress), 'fbbody0'),
				blank1,
				urwid.AttrMap(urwid.Edit('TYPE:', str(source.type)), 'fbbody0')]
				)), align='center', width=('relative', 90))]
			i += 1


		self.addSourceButton = urwid.AttrMap(ffCursesClasses.ffIdButton('ADD SOURCE', self.addSource), 'fbbody0')
		self.deleteSourceButton = urwid.AttrMap(ffCursesClasses.ffIdButton('DELETE SOURCE', self.deleteSource), 'fbbody0')
		self.saveCancelB = urwid.AttrMap(urwid.Columns([
												('weight',5, self.addSourceButton),
												('weight',1, blank1),
												('weight',5, self.deleteSourceButton),
												('weight',1, blank1),
												('weight',5, self.saveB),
												('weight',1, blank1),
												('weight',5, self.cancelB),
												]), 'fbbody0')

		return urwid.AttrMap(urwid.Padding(urwid.AttrMap(urwid.LineBox(urwid.ListBox(
							[
							urwid.LineBox(urwid.Text( 'EDIT CHANNEL ATTRIBUTES:','center')),
							blank1,
							self.titleEdit,
							blank1,]
							+self.sourcesListText
							+[urwid.LineBox(self.saveCancelB)])), 'fbbody1' ), align='center', width=('relative', 50)), 'fbbody0')

	def __init__(self, ffFeedViewer, changeView, replaceChannel):
		#values for various sources
		self.replaceChannel = replaceChannel
		self.sourcesListText = []
		self.channel = ffFeedViewer.channel
		#change view function
		self.changeView = changeView
		#bind save and cancel buttons
		self.saveB = ffCursesClasses.ffIdButton('SAVE CHANGES', self.saveCh)
		self.cancelB = ffCursesClasses.ffIdButton('CANCEL CHANGES', self.cancelCh)

		#populate dialog
		self.screen = self.populateEntries(self.channel)
		super(ffChannelInfoDialog, self).__init__(self.screen)
