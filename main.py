#
# main.py
# ?
#
# None
# August 13 2015
#

# TODO | - 
#        - 

# SPEC | -
#        -



from SwiftUtils.SwiftUtils import chunks
from math import log
from PIL import Image
from itertools import chain



def bitchunks(n, size, chunksize):
	assert size % chunksize is 0, 'Chunks don\'t fit.'
	assert size > log(n, 2),      'Number doesn\'t fit inside {0} bits.'.format(size)
	mask = 2**chunksize - 1
	return (mask & (n >> d) for d in range(size-chunksize, -chunksize, -chunksize))


def unbitchunks(chunks, size, chunksize):
	assert size % chunksize is 0, 'Chunks don\'t fit.'
	return sum(chunk << (n-size/) for n, chunk in enumerate(chunks))



# def pixels(image): pass



def setbits(n, bits):
	# TODO: Parameters (not just last two bits)
	# TODO: Validate arguments
	# TODO: Test
	return (n >> 2 << 2) | bits



def hide(image, data):

	'''
	Hides data in the last two bits of the blue channel

	'''

	# TODO: Arbitrary Unicode or binary data
	# TODO: Ensure that data fits in image
	# TODO: Tweak parameters

	pixels = image.load()

	stream = chain(*(bitchunks(ord(c), 8, 2) for c in data)) # Iterator over bit chunks

	for x in range(image.size[0]):
		for y in range(image.size[1]):
			r, g, b = pixels[(x, y)]
			pixels[(x, y)] = (r, g, setbits(b, next(stream)))

	return image



def bitstream(pixels):
	# 
	for x in range(image.size[0]):
		for y in range(image.size[1]):
			yield 0b11 & pixels[(x, y)][2] # Last two bits of blue channel


	
def unhide(image):

	'''
	Recovers hidden data in an image.

	'''

	return ''.join(unbitchunks(chunk, 8, 2) for chunk in chunks(list(bitstream(image.load())), 4) #) 



def bitchunkSuite():
	
	# 
	n         = 2134 # Number to be smeared out
	chunksize = 2    # Size of each chunk (in bits)
	size      = 16   # Size of the number (in bits)

	# 
	print(*chunks(('{:0%sb}' % size).format(n), chunksize))
	print(*(('{:0%sb}' % chunksize).format(bits) for bits in bitchunks(n, chunksize, size)))



def main():
	
	'''
	Docstring goes here

	'''

	pass



if __name__ == '__main__':
	main()