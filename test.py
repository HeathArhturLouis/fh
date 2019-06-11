import feedparser

feed0 = feedparser.parse('https://hnrss.org/newest')
feed1 = feedparser.parse('http://rss.slashdot.org/Slashdot/slashdotMain')

'''
for i in range(len(feed1.entries)):
	print(str(feed1.entries[i].title))


entries01 = feed0.entries + feed1.entries

for i in range(len(entries01)):
	print(str(entries01[i].title))

'''
print(feed0.feed.title)
