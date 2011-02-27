class State:
    def __init__(self):
        self.states = []

    def clear(self):
        self.states[:] = []

    def get_all(self):
        # Note: need clarification for this funtion, for example:
        # sen1 is "I like action and Jet Lee." // slot1 in states
        # sen2 is "I also like drama and Johnny Deep." // slot2 in states
        # get_all can only return a dict however we need to return "action"
        # + "drama"(2 genres) and "Jet Lee" + "Johnny Deep"(2 actors) since
        # all of them are required.
        dict = self.states[-1].copy()
        return dict

    def add_request(self, dict):
        self.states.append(dict)

    def add_result(self, dict):
        # same clarification needed as get_all()
        self.states.append(dict)

    def last_request(self):
        # I'm assuming every sentence has a 'request'!
        # Let me know if there are examples that don't.
        dict = self.states[-1]
        if dict['request'] == 'OPINION':
            if dict.has_key('title'):
                return dict['title']
        elif dict['request'] == 'COUNT':
            if dict.has_key('of'):
                return dict['of']
        return dict['request']

    def resolve_pronoun(self, value):
        # Find the last PRE_HE/PRE_IT.
        lists = self.states[:]
        lists.reverse()
        for dict in lists:
            if value == 'PRE_HE':
                # Assuming actor/director is the only person we care about!
                if dict.has_key('actor') and dict['actor'] != 'PRE_HE':
                    return dict['actor']
                elif dict.has_key('director') and dict['director'] != 'PRE_HE':
                    return dict['director']
            elif value == 'PRE_IT':
                # Assuming title is the only attribute PRE_IT will refer!
                if dict.has_key('title') and dict['title'] != 'PRE_IT':
                    return dict['title']
        # user entered it/he/she but state doesn't have their info.
        return 'error'


#################################### Tests ####################################
def print_dict(dict):
    for key in dict:
        print dict[key]

state = State()
state.add_request({'request':'director', 'title':'Titanic'})
print '1st add => get_all:::::::'
print state.get_all()
print '1st add => last_request::::'
print state.last_request() + '\n'

state.add_request({'request':'title', 'director':'James Cameron'})
print '2nd add => get_all:::::::'
print state.get_all()
print '2nd add => last_request::::::'
print state.last_request() + '\n'

state.add_request({'request':'OPINION', 'genre':'action', 'keyword':'dream'})
print '3nd add => get_all:::::::'
print state.get_all()
print '3nd add => last_request::::::'
print state.last_request() + '\n'

state.add_request({'request':'OPINION', 'character':'Batman'})
print '4nd add => get_all:::::::'
print state.get_all()
print '4nd add => last_request::::::'
print state.last_request() + '\n'

state.add_request({'request':'COUNT', 'of':'Academy Award', 'actor':'Kate Winslet'})
print '5rd add => get_all:::::::'
print state.get_all()
print '5rd add => last_request::::::'
print state.last_request() + '\n'


print 'resolve PRE_IT ::::::::::::::::::::::::::'
print state.resolve_pronoun('PRE_IT')
print 'resolve PRE_HE ::::::::::::::::::::::::::'
print state.resolve_pronoun('PRE_HE') + '\n'


print 'before clear:::::::::::::::::::::::'
print 'len(states) = ', len(state.states)
for dict1 in state.states:
    print_dict(dict1)
print 'after clear::::::::::::::::::::::::'
state.clear()
print 'len(states) = ', len(state.states), '\n'
