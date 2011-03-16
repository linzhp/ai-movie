import pickle

with open('./tagged_fixed', 'r') as infile:
	tagged = infile.readlines()
	with open('./../training_sentences.bin', 'wb') as outfile:

		sentlist = []

		for y in tagged:
			sentence = []
			groups = y.split()
			for x in groups:
				spl = x.split('/')
				pair = spl[0], spl[1]
				sentence.append(pair)

			sentlist.append(sentence)

		pickle.dump(sentlist, outfile)
	outfile.closed
infile.closed

