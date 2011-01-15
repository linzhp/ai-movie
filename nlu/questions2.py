import chunker


def who(list):
    #print list
    #print type(list)

    for x in list:
        if str(type(x)) != "<type 'tuple'>":
            #print type(x)
            for y in x:
                if "VP" in str(x.node):            

                    if "directed" in str(y[0]).lower():
                        print 'director'
                    elif "made" in str(y[0]).lower():
                        print 'director'
                    elif "starred" in str(y[0]).lower():
                        print 'actor'
                    elif "was in" in str(y[0]).lower():
                        print 'actor'

chk = chunker.Chunker()
control = True


while control:
    input = raw_input('Please enter a question: ')
    print " " +  input + "\n"

    if input == "exit":
        control = False
    else:
        chk_tree = chk.chunk(input)

        #print chk_tree

        list = chk_tree.subtrees()
        #print type(list)

        for x in chk_tree:

            #print type(x)
            #print str(type(x))

            if str(type(x)) != "<type 'tuple'>":
                for y in x:

                    if "B-QUESTION" in str(x.node):
                    #print "B-QUESTION found \n"

                        if "who" in str(y[0]).lower():
                            print "who"
                            who(chk_tree)

                        elif "what" in str(y[0]).lower():
                            print 'what'

                        elif "when" in str(y[0]).lower():
                            print 'when'



