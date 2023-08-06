'''Converts a PBZX file to a TAR file.
Adapted from http://newosxbook.com/src.jl?tree=listings&file=pbzx.c
'''

import struct
import argparse

def bswap64(i):
	'''Does a binary swap on a uint_64.
	'''
	return struct.unpack("<Q", struct.pack(">Q", i))[0]

def asUint64(i):
	'''Converts read string to an unsigned 64-bit integer.
	'''
	return struct.unpack("Q", i)[0]

def pbzxToTar(inFile, outFile):
	'''Converts a PBZX file to a TAR file.
	Parameters:
		* inFile: The file object to unpack.
		* outFile: The destination file object to write output to.
	'''
	#Check it's a PBZX first.
	kPbzxMagic = '\x70\x62\x7A\x78' #pbzx
	fileMagic = inFile.read(4)
	if fileMagic != kPbzxMagic:
		raise RuntimeError("File doesn't have PBZX magic code; is this a PBZX file?")

	#If it is, start reading chunks.
	kUintSize = 8
	flags = 0
	length = 0

	#Get the first flag data.
	flags = bswap64(asUint64(inFile.read(kUintSize)))
	print("Flags: 0x%x" % flags)

	numBadChunks = 0
	numBadHeaders = 0
	numBadFooters = 0
	numBadLength = 0

	#While we have chunks...
	while flags & 0x01000000:
		flags = bswap64(asUint64(inFile.read(kUintSize)))
		#Limit chunk size to 4 GiB.
		kMaxChunkLength = 4 * (1 << 30)
		length = bswap64(asUint64(inFile.read(kUintSize)))

		if length > kMaxChunkLength:
			#Skip any chunks with bad length counts.
			numBadChunks += 1
			numBadLength += 1
		else:
			#Otherwise, go ahead and read.
			chunkBuffer = inFile.read(length)

			#We want the XZ header/footer if it's the payload,
			#but prepare_payload doesn't have that,
			#so just warn.
			header = chunkBuffer[:5]
			kExpectedHeader = "\xFD7zXZ"
			if header != kExpectedHeader:
				numBadChunks += 1
				numBadHeaders += 1
			else:
				#Check the footer too.
				#Footer is "YZ".
				footer = chunkBuffer[-2:]
				kExpectedFooter = "\x59\x5A"
				if footer != kExpectedFooter:
					numBadChunks += 1
					numBadFooters += 1
				else:
					#Only write out valid chunks.
					outFile.write(chunkBuffer)

	if numBadChunks > 0:
		#Report any unread chunks.
		errorString = "File had {0} unreadable chunks that weren't written:\n\tBad headers: {1}\n\tBad footers: {2}\n\tBad length counts: {3}".format(numBadChunks, numBadHeaders, numBadFooters, numBadLength)
		print(errorString)

		#But this is only an error if there
		#are bad footers or length counts; apparently
		#some non-data chunks can have invalid headers?
		if numBadFooters > 0 or numBadLength > 0:
			raise RuntimeError(errorString)

def main():
	'''Entry point when used as a program.
	'''
	parser = argparse.ArgumentParser(description="Converts a PBZX file to a TAR file.")
	parser.add_argument("inFile", help="The PBZX file to read.")
	parser.add_argument("outFile", help="The PBZX file to write.")
	args = parser.parse_args()

	#Try to open both files.
	print("Opening files:\n\tInput: {0}\n\tOutput: {1}".format(args.inFile, args.outFile))
	inFile = open(args.inFile, "rb")
	outFile = open(args.outFile, "wb")
	print("Files open, beginning conversion")

	pbzxToTar(inFile, outFile)
	print("Conversion complete.")

if __name__ == "__main__":
	main()
