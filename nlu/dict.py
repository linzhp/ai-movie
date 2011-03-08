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
            
def negativate(self):
    """
    For amending dictionaries only
    """ 
    new_dict = ListDict()    
    for key in self:
        new_dict['!'+key]=self[key]
    return new_dict
            
if __name__ == "__main__":
    d = ListDict(title='ha')
    d.add('title', 'foo')
    print d 