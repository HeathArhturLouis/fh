import ffClasses
import ffCursesClasses
import pickle

'''
Create 3 demo feeds and pickle them to the save file

'''


f = open('../data/channels.pkl', 'wb')

#create example channels
newChannel1 = ffClasses.ffChannel('Testing Channel 1')
newChannel1.addSourceAdress('https://hnrss.org/newest', ffClasses.ffSource.ffSourceT.RSS)
#newChannel1.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffClasses.ffSource.ffSourceT.RSS)
#newChannel1.addSourceAdress('https://feedpress.me/drudgereportfeed', ffClasses.ffSource.ffSourceT.RSS)
newChannel1.update()


newChannel2 = ffClasses.ffChannel('Testing Channel 2')
#newChannel2.addSourceAdress('https://hnrss.org/newest', ffClasses.ffSource.ffSourceT.RSS)
newChannel2.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffClasses.ffSource.ffSourceT.RSS)
#newChannel2.addSourceAdress('https://feedpress.me/drudgereportfeed', ffClasses.ffSource.ffSourceT.RSS)
newChannel2.update()


newChannel3 = ffClasses.ffChannel('Testing Channel 3')
#newChannel3.addSourceAdress('https://hnrss.org/newest', ffClasses.ffSource.ffSourceT.RSS)
#newChannel3.addSourceAdress('http://rss.slashdot.org/Slashdot/slashdotMain', ffClasses.ffSource.ffSourceT.RSS)
newChannel3.addSourceAdress('https://feedpress.me/drudgereportfeed', ffClasses.ffSource.ffSourceT.RSS)
newChannel3.update()

pickle.dump([newChannel1, newChannel2, newChannel3], f)
