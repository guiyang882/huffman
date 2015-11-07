# huffman

## usage example:
    python compress.py result/Lorem_ipsum.txt result/a.bin
    python decompress.py result/a.bin result/decode_test.txt

## use copy.deepcopy()
### Use voilence search method to decode the file
	time python decompress.py result/a.bin result/decode_test.txt 
	Decode Finished !

	real	1m6.263s
	user	1m5.760s
	sys	0m0.440s

### Use Prefix search method to decode the file
	time python decompress.py result/a.bin result/decode_test.txt 
	Decode Finished !

	real	15m14.708s
	user	14m50.864s
	sys	0m8.756s

## use copy.copy()
### use Prefix search method to decode the file 
	time python decompress.py result/a.bin result/decode_test.txt 
	Use Prefix to decode the File Finished !

	real	0m13.688s
	user	0m13.292s
	sys	0m0.200s
