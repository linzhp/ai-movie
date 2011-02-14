import logging
from nlg import nlg
from nlu.nlu import NLU
from dm import dialogManager

logging.basicConfig(level=logging.DEBUG,
                    filename='session.log',
                    format='%(message)s',
                    filemode='w')
nlu = NLU()

try:
    greeting=nlg.greet()
    logging.info('Bot: '+greeting)
    input = raw_input(greeting+'\n')
    while input is not None:
        logging.info('User: '+input)
        nlu_out = nlu.process(input)
        logging.debug('nlu_out: '+nlu_out)
        dm_out=dialogManager.input(nlu_out)
        logging.debug('dm_out: '+dm_out)
        output=nlg.process(nlu_out,dm_out)
        for dict in nlu_out:
            if dict.get("command")=="exit":
                exit()
        logging.info('Bot: '+output)
        input = raw_input(output+'\n')
except EOFError:
    exit()