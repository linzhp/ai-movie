import logging
from nlg import nlg
from nlu.nlu import NLU
from dm import dialogManager

logging.basicConfig(level=logging.DEBUG,
                    filename='session.log',
                    format='%(message)s',
                    filemode='w')
nlu = NLU()

greeting=nlg.greet()
logging.info(greeting)
input = raw_input(greeting+'\n')
while input is not None:
    nlu_out = nlu.process(input)
    for dict in nlu_out:
        if dict.get("command")=="exit":
            exit(0)
    dm_out=dialogManager.input(nlu_out)
    output=nlg.process(dm_out)
    input = raw_input(output+'\n')