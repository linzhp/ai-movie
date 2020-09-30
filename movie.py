import logging
from nlg import nlg
from nlu import NLUnderstanding
from dm import DialogManager, chatbot

logging.basicConfig(level=logging.DEBUG,
                    filename='session.log',
                    format='%(message)s',
                    filemode='a')

nlu = NLUnderstanding()
dialogManager = DialogManager()

#TODO test MORE PREF

try:
    greeting="Hi, I am NIMROD, and you can ask me to help you find movies,\nPlease Tell me your preferences, and i can find movies that match them\n\
please put movie titles in quotes, although you do not have to capitalize names, although you certainly may if you wish. \n\
you can also ask me trivia questions, and i will answer to the best of my ability"#nlg.greet()
    logging.info('Bot: '+greeting)
#    print('Bot: '+greeting)
    input = raw_input(greeting+'\n')
    while input is not None:
        if len(input)==0:
            input = raw_input("Could you speak louder? I can't hear you\n")
            continue
        try:
            # NLU processing
            logging.info('User: '+input)
            nlu_out = nlu.process(input)
            print nlu_out
            logging.debug('nlu_out: '+str(nlu_out))
            # Dialog manager processing
            dm_out=dialogManager.input(nlu_out)
            logging.debug('dm_out: '+str(dm_out))
            # Dialog manager gives feed back to NLU
            nlu.expect = dialogManager.pending_question
            # Generate response to user
            output=nlg.process(nlu_out,dm_out)
        except "nothing":#Exception, ex:
#            logging.debug('error: '+ex)
            dialogManager.state.clear()
            output = chatbot.reply
        # Print and log response  
        logging.info('Bot: '+str(output))
#        print('Bot: '+str(output))
        # Decide whether to continue
        for dict in nlu_out:
            if dict.get("command")=="EXIT":
                exit()
        #Get user input
        input = raw_input(output+'\n')
except EOFError:
    exit()
