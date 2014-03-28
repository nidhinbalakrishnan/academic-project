import json
import pickle
from sets import Set

fid=open('dynamic_dictionary','w')
positive = Set([])
negative = Set([])

positive.add(('like',0))
negative.add(('hate',0))

dict =[]
dict.append(positive)
dict.append(negative)

#json.dump(dict,fid)
pickle.dump(dict,fid)
fid.close()
print 'Dictionary Created...'
