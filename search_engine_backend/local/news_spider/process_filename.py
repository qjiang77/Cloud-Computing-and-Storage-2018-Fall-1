import os
import re

path = os.path.dirname(os.path.abspath(__file__))

path = os.path.join(path, 'articles')

regex = re.compile('[^a-zA-Z_]')

#print regex.sub('', 'I_am_the_king_god?!,')

for subdir in os.listdir(path):
    p = os.path.join(path, subdir)
    if not os.path.isdir(p):
        continue
    for filename in os.listdir(p):
        filename = filename.decode('utf-8')
        old_name = os.path.join(p, filename)
        tmp = open(old_name, 'r')
        lines = tmp.readlines()
        tmp.close()
        if not all(ord(char) < 128 for char in filename) or len(lines) <= 1: # filename contains non ascii chars, or this file has no actual content
    	    print "Remove %s" % old_name
            #input()
    	    os.remove(old_name)
            continue 
		
        #First parameter is the replacement, second parameter is your input string	
        new_name = os.path.join(p, regex.sub('', filename.replace(' ', '_')))
        #print new_name

        #print old_name, [ord(char) for char in filename]
        os.rename(old_name, new_name)

