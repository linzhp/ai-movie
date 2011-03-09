'''
Created on Mar 7, 2011

@author: linzhp
'''

class ListDict(dict):
    def add(self, key, value):
        """
        For amending dictionaries only
        """
        if self.has_key(key):
            cur_val = self[key]
            if isinstance(cur_val, list):
                cur_val.appent(value)
            else:
                self[key]=[cur_val, value]
        else:
            self[key]=value
            
    def concat(self, other_dict):
        """
        For amending dictionaries only
        """
        for key in other_dict:
            self.add(key, other_dict[key])
            
dictionary={'a':1, 'one':1, 'two':2, 'three':3, 'four':4,'five':5,\
            'six':6, 'seven':7, 'eight':8,'nine':9, 'ten':10,\
            'eleven':11,'twelve':12, 'thirteen':13, 'fourteen':14,\
            'fifteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18,\
            'nineteen':19, 'twenty':20}

def english2int(word):
    number=None
    try:
        number = int(word)
    except ValueError:
        number = dictionary.get(word)
    return number
            
if __name__ == "__main__":
    d = ListDict(title='ha')
    d.add('title', 'foo')
    print d 