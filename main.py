#
# main.py
# ?
#
# Jonatan H Sundqvist
# August 13 2015
#

# TODO | - Allow encoding and decoding of arbitrary byte sequences
#        - Documentation, test coverage

# SPEC | -
#        -



from SwiftUtils.SwiftUtils import chunks # TODO: Use ichunks instead
from PIL import Image
from itertools import chain, islice



def bitchunks(n, size, chunksize):

	'''
	Docstring goes here

	'''

	# assert size % chunksize is 0, 'Chunks don\'t fit.'
	# assert n <= 2**size,          'Number {0} doesn\'t fit inside {1} bits.'.format(n, size)
	mask = 2**chunksize - 1
	return (mask & (n >> d) for d in range(size-chunksize, -chunksize, -chunksize))



def unbitchunks(chunks, size, chunksize):

	'''
	Docstring goes here

	'''

	# assert size % chunksize is 0, 'Chunks don\'t fit.'
	return sum(chunk << d for d, chunk in zip(range(size-chunksize, -chunksize, -chunksize), chunks))



def pixelstream(pixels, imagesize):

	'''
	Docstring goes here

	'''

	for x in range(imagesize[0]):
		for y in range(imagesize[1]):
			yield pixels[(x, y)], (x, y)



def setbits(n, bits, size=2):

	'''
	Docstring goes here

	'''

	# TODO: Parameters (not just last two bits)
	# TODO: Validate arguments
	# TODO: Test
	# assert bits <= 2**size, '{n} doesn\'t fit in {size} bits.'.format(n=n, size=size)
	return (n >> size << size) | bits



def hide(image, data, encode, size, chunksize):

	'''
	Hides data in the last two bits of the blue channel

	'''

	# TODO: Arbitrary Unicode or binary data
	# TODO: Ensure that data fits in image
	# TODO: Return stats (?)
	# TODO: Tweak parameters

	stream = chain(*[bitchunks(encode(c), size, chunksize) for c in data]) # Iterator over bit chunks
	pixels = image.load()

	for datachunk, ((r, g, b), (x,y)) in zip(stream, pixelstream(pixels, image.size)):
		pixels[(x, y)] = (r, g, setbits(b, bits=datachunk, size=chunksize))

	return image



def bitstream(pixels, size, imagesize):

	'''
	Docstring goes here

	'''

	return (b & (2**size - 1) for (_, _, b), _ in pixelstream(pixels, imagesize)) # Last two bits of blue channel


	
def unhide(image, length, decode, size, chunksize):

	'''
	Recovers hidden data in an image.

	'''

	return (decode(unbitchunks(chunk, size, chunksize)) for chunk in islice(chunks(list(bitstream(image.load(), chunksize, image.size)), size//chunksize), 0, length))



def bitchunkSuite():
	
	'''
	Docstring goes here

	'''

	# 
	n         = 123 # Number to be smeared out
	chunksize = 2   # Size of each chunk (in bits)
	size      = 8   # Size of the number (in bits)

	# 
	# TODO: Clean this up
	print(*(('{:>%d}' % chunksize).format(str(n)) for n in range(size//chunksize)))
	print(*chunks(('{:0%sb}' % size).format(n), chunksize))
	print(*(('{:0%sb}' % chunksize).format(bits) for bits in bitchunks(n, size, chunksize)))
	for n, c in enumerate(chain(*(bitchunks(ord(c), size, chunksize) for c in 'Hello World!'))):
		print(('{:0%sb}' % chunksize).format(c), end='|' if ((n+1) % (size//chunksize)) is 0 else '')
	print()



def hideunhide(data, length, targetimage, encode, decode, pack, unpack, size, chunksize):

	'''
	Docstring goes here

	'''

	# TODO: Make copy of target image (?)
	# TODO: Compute length automatically (?)
	hidden   = hide(targetimage, pack(data), encode=encode, size=size, chunksize=chunksize)
	revealed = unpack(unhide(hidden, length=length, decode=decode, size=size, chunksize=chunksize))

	return {

		'hidden':      hidden,   #
		'revealed':    revealed, #

		'data':        data,        #
		'targetimage': targetimage, #
		'encode':      encode,      #
		'decode':      decode,      #
		'pack':        pack,        #
		'unpack':      unpack,      #
		'size':        size,        # TODO: Rename
		'chunksize':   chunksize    #

	}



def unpackImage(pixelstream, imagesize):

	'''
	Docstring goes here

	'''

	canvas = Image.new('RGB', imagesize, 'black')
	pixels = canvas.load()

	for n, pixel in enumerate(pixelstream):
		pixels[(n//canvas.size[1], n%canvas.size[1])] = pixel

	return canvas



def main():

	'''
	Docstring goes here

	'''

	# Hide some text
	message = '\'No Shit Sherlock\' is a fairly common - but vulgar - phrase. It is roughly equivalent to \'You don\'t say\'.'
	result = hideunhide(data        = message,
	                    length      = len(message),
	                    targetimage = Image.open('assets/mont-sainte-victoire-3.jpg'),
	                    encode      = ord,
	                    decode      = chr,
	                    pack        = lambda x: x,
	                    unpack      = lambda s: ''.join(s),
	                    size        = 8,
	                    chunksize   = 2)

	result['hidden'].save('assets/sainte-victoire-hidden-text.png') # It's very important to use a non-destructive encoding.
	assert result['revealed'] == message, 'Something went wrong. That\'s all I know.'
	print(result['revealed'])

	# Hide an image
	secretimage = Image.open('assets/anothersecret.jpg')
	message     = (rgb for rgb, _ in pixelstream(secretimage.load(), secretimage.size))

	result = hideunhide(data        = message,
	                    length      = secretimage.size[0]*secretimage.size[1],
	                    targetimage = Image.open('assets/Munch.jpg'),
	                    encode      = lambda p: sum(ch << ((2-n)*8) for n, ch in enumerate(p)),
	                    decode      = lambda n: tuple((n >> o*8) & (2**8-1) for o in range(2, -1, -1)),
	                    pack        = lambda x: x,
	                    unpack      = lambda pixels: unpackImage(pixels, secretimage.size),
	                    size        = 8*3,
	                    chunksize   = 4)

	result['hidden'].save('assets/Munch-hidden-image.png') # It's very important to use a non-destructive encoding.
	result['revealed'].show()



if __name__ == '__main__':
	main()