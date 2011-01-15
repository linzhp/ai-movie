import chunker

chk = chunker.Chunker(True)

while 1 == 1:

	input_text = raw_input("\nEnter a sentence:  ")
	
	chunked = chk.chunk(input_text)

	print chunked

