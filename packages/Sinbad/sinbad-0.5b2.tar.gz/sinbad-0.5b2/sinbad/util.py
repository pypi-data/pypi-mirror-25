
import hashlib
import time
import urllib.request

from os import system
from platform import system as platform


def hash_string(str):
    '''Return a simple hash of the given string.
    
    The hash itself is a string of at most 25 characters.
    '''
    h = hashlib.sha1(str.encode('utf_8')).hexdigest()
    return h[:25]


def current_time_millis():
    '''Return the current time in milliseconds'''
    return int(time.time() * 1000)


def current_time():
    '''Return the current time in seconds'''
    return int(time.time())


def smells_like_url(path):
    '''Determine if the given path seems like a URL.
    
    Currently, only things that start off http://
    https:// or ftp:// are treated as URLs.
    '''
    return path.find("://") >= 0 and \
        (path.startswith("http") or path.startswith("ftp")) 


def smells_like_zip(path):
    return path.find(".zip") >= 0


def create_input(path):
    '''Returns a triple, ( fp, path, enc ), containing a file-type object
    for the given path, a potentially redirected path name, and an encoding.
    
    If the path is a normal file, produces a file-object for that file.
    
    If the path is a URL, makes a request to that URL and
    returns an input stream to read the response.
    
    In the process of processing the response from the URL,
    if a modified name for the file is found (e.g. in 
    a Content-Disposition header), that is produced. 
    Otherwise the path is produced back as is.
    
    If an encoding is determined from the URL response
    headers, it is included, otherwise the third element 
    of the triple is None.    
    '''
    if not path: return None
    
    charset = None
    if smells_like_url(path):
        req = urllib.request.Request(path, 
                                     data=None,
                                     headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
        file = urllib.request.urlopen(req)
        charset = file.info().get_content_charset()
    elif path.startswith("wss:"):
        return (path, path, charset)
    else:
        file = open(path, 'rb')  # binary to be consistent with urlopen 

    return (file, path, charset)
    


def normalize_keys(data):
    '''Ensures that keys in the dictionary follow identifier naming rules. 
    
    (This is required because the jsonpath parser is picky.) 
    '''
    if isinstance(data, list):
        for i in range(len(data)):
            data[i] = normalize_keys(data[i])
    elif isinstance(data, dict):
        for k, v in data.items():
            #if k.find("-") >= 0:
            #    del data[k]
            #    k = k.replace("-", "_")
            #    data[k] = v
            
            if k[0].isdigit():
                del data[k]
                k = "_" + k
                data[k] = v
                
            normalize_keys(v)
    
    return data
    

def collapse_dicts(data):
    '''
    Removes extraneous levels of dictionary nesting.
    
    For example,
         { 'a' : { 'b' : { 'c' : "blah", 'd' : "blah" } } }
    turns into
         { 'c' : "blah", 'd' : "blah" }
    '''
    if not isinstance(data, dict):
        return data
    else:
        for k, v in data.items():
            data[k] = collapse_dicts(v)
            
        first_item = None
        first_value = None
        for first_item, first_value in data.items(): break          # https://stackoverflow.com/questions/59825/how-to-retrieve-an-element-from-a-set-without-removing-it
        if len(data.keys()) == 1 and first_item and isinstance(first_value, dict) and \
                len(first_value.keys()) == 1:
            for _, first_value_value in first_value.items(): break
            data[first_item] = first_value_value
        
        if len(data.keys()) == 1:
            data = first_value
        
        return data



def tk_to_front(root):
    root.focus_force()
    
    if platform() == 'Darwin':  # How Mac OS X is identified by Python
        system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

