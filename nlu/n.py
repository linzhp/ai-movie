
import nlu
nl = nlu.NLU()

while True:

	raw_in = raw_input("Enter a sentence to parse: ")
	if raw_in == 'exit':
		break
	print nl.process(raw_in)

