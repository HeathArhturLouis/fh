'''
Definitions of a forcefeed channel


A channel is a feed with multiple sources
'''
import feedparser
#enmerated source types

class ffEntry:
	def __init__(self, eData, eSource):
		#Feed parser entry structure
		self.data = eData
		#name of the source
		self.source = eSource

class ffSource:
	'''
	'''
	#enum type for possible source types
	class ffSourceT:
		RSS = -1
		ATOM = -2

	def __init__(self, sAdress, sType):
		self.adress = sAdress
		self.name = sAdress
		self.type = sType

	def parse(self):
		'''
		parse source and return entries
		'''
		if(self.type == self.ffSourceT.RSS or self.type == self.ffSourceT.ATOM):
			pFeed = feedparser.parse(self.adress)
			#set source name to origin feeds title
			self.name = pFeed.feed.title
			#return list of [entry, sourceName] pairs
			return [ ffEntry( entry , self.name) for entry in pFeed.entries]

class ffChannel:
	def __init__(self, fTitle):
		#channel title
		self.title = fTitle
		#sources/feeds in channel, list of html adresses saved as strings
		self.sources = []
		#list of parsed entries and their associated source feeds
		# Supposed to be list of entry_source pairs
		self.entries = []


	def addSourceAdress(self, htmlAdress, sType):
		self.sources.append(ffSource(htmlAdress , sType))

	def addSource(self, ffSource):
		self.sources.append(ffSource)

	def update(self):
		'''
		Update channel entries from sources
		'''
		for source in self.sources:
			self.entries += source.parse()

	def printTitles(self):
		for entry in self.entries:
			print(entry.data.title)

############################### TESTING CODE ##############################

def main():
	newChannel = ffChannel('Testing Channel')
	newChannel.addSourceAdress('https://hnrss.org/newest', ffSource.ffSourceT.RSS)
	newChannel.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffSource.ffSourceT.RSS)

	newChannel.update()

	newChannel.printTitles()

if __name__ == '__main__':
	main()
	pass