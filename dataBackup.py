from postFB import *
import pickle

##f = open('backupData.pickle','rb')
##listToReturn = pickle.load(f)
##f.close()

listToReturn = []

while len(listToReturn) is not 20:
    print len(listToReturn)
    value = fbSinglePost()
    if value is not None:
        listToReturn.append(value)
    
f = open('backupData.pickle','wb')
pickle.dump(listToReturn, f)
f.flush()
f.close()
