class State:
    def __init__(self):
        self.states = []

    def clear(self):
        self.states[:] = []

    ### need work
    def get_all(self):
        return self.states

    def add_request(self, dict):
        self.states.append(dict)

    ### need work
    def add_result(self, dict):
        self.states.append(dict)

    def last_request(self):
        dict = self.states[-1]
        if dict['request'] in 'OPINION':
            if dict.has_key('title'):
                return dict['title']
        elif dict['request'] in 'count':
            if dict.has_key('of'):
                return dict['of']
        return dict['request']

    def resolve_pronoun(self, value):
        lists = self.states[:]
        lists.reverse()
        for dict in lists:
            if value == 'PRE_HE':
                if dict.has_key('person'):
                    if dict['person'] != 'PRE_HE':
                        return dict['person']
            elif value == 'PRE_IT':
                if dict.has_key('title'):
                    if dict['title'] != 'PRE_IT':
                        return dict['title']
        return 'error'


def print_dict(dict):
    for key in dict:
        print dict[key]

state = State()
state.add_request({'request':'plot', 'genre':'action', 'keyword':'dream'})
print '1st add => get_all:::::::::'
print state.get_all()
print '1st add => last_request::::'
print state.last_request()

state.add_request({'request':'OPINION', 'title':'Matrix'})
print '2nd add => get_all:::::::::::'
print state.get_all()
print '2nd add => last_request::::::'
print state.last_request()

state.add_request({'request':'OPINION', 'person':'Bill Gates'})
print '3nd add => get_all:::::::::::'
print state.get_all()
print '3nd add => last_request::::::'
print state.last_request()

state.add_request({'request':'OPINION', 'person':'PRE_HE'})
print '4nd add => get_all:::::::::::'
print state.get_all()
print '4nd add => last_request::::::'
print state.last_request()
print '4nd add => resolve:::::::::::'
print state.resolve_pronoun('PRE_HE')

state.add_request({'request':'count', 'of':'Academy Award', 'person':'PRE_IT'})
print '5rd add => get_all:::::::::::'
print state.get_all()
print '5rd add => last_request::::::'
print state.last_request()
print '5nd add => resolve:::::::::::'
print state.resolve_pronoun('PRE_IT')


print 'before clear:::::::::::::::::::::::'
for dict1 in state.states:
    print_dict(dict1)
print 'after clear::::::::::::::::::::::::'
state.clear()
for dict2 in state.states:
    print_dict(dict2)
