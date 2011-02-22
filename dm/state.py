class State:
    def __init__(self):
        self.states = []

    def clear(self)
        self.states[:] = []

    def get_all(self):
        return self.states

    def add_condition(self, dict):
        self.states.append(dict)

    def last_request(self):
        return self.states[-1]

    def resolve_pronoun(self, key):

#    go back one or more steps
#    def del_condition(self, ):
#        self.states.pop()
