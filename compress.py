import os
import sys
from include.Priority_Queue import PriorityQueue
from include.Node import Node
import struct
import pickle

def saveKey(nodes):
    key_map = {}
    for key in nodes.keys():
        value = nodes[key]
        #print key,value.code
        key_map[key] = value.code
    handle = open("./result/key.json",'wb')
    handle.write(str(key_map))
    handle.close()

    ## save pickle
    handle = open("./result/key.pkl",'wb')
    pickle.dump(key_map,handle)
    handle.close()

def convert_str2hex(content):
    '''
    from the begin to the end, we get 32bit(char) means
    the subpart of the content, we should convert the 32(char) to 32bit
    convert to hex
    '''
    hex_list = []
    index = 0
    length = len(content)
    #last_size = -1
    while index < length:
        sub_str = content[index:index+32]
        index = index + 32
        #if len(sub_str) != 32:
        #    last_size = len(sub_str)
        hex_list.append(struct.pack("I",int(sub_str,base=2)))
    #hex_list.append(struct.pack("I",last_size))
    return "".join(hex_list)

def change_file_type(filename):
    name_list = filename.split(".")
    if len(name_list) == 2:
        name_list[-1] = "bin"
    return ".".join(name_list)

def compress(inFile,outFile):
    infp = open(inFile,'r')
    text = infp.read()
    outFile = change_file_type(outFile)
    outfp = open(outFile,'wb')
    
    nodes = {}
    
    for char in text:
        if char in nodes:
            nodes[char].value += 1
        else:
            nodes[char] = Node(1,char)
            
    #Add in psuedo-EOF marker symbol
    EOF = chr(255)+chr(255)
    nodes[EOF] = Node(1,EOF)

    q = PriorityQueue()
    for node in nodes.values():
        q.enQueue(node)

    min1 = q.deQueue()
    min2 = q.deQueue()
    while min2:
        q.enQueue(min1+min2)
        min1 = q.deQueue()
        min2 = q.deQueue()
    #root = min1
    saveKey(nodes)
    output = ''
    for char in text:
        if char in nodes:
            output += nodes[char].code
        else:
            print 'Char object not found!'
            
    #Add psuedo-EOF marker
    output += nodes[EOF].code
    save_content = convert_str2hex(output)
    outfp.write(save_content)
    outfp.close()
    print "Please Check the compressed File !"
    return len(save_content)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python compress.py originalFile.txt compressedFile.bin'
        exit()
    if os.path.exists(sys.argv[1]):
        uncompressedSize = os.stat(sys.argv[1]).st_size
        compressedSize = compress(sys.argv[1],sys.argv[2])
        print 'Uncompressed Size: %s bytes' % uncompressedSize
        print 'Compressed Size: %s bytes' % compressedSize
        print 'Precent Space Saved: %f' % (1-(float(compressedSize)/float(uncompressedSize)))
    else:
        print 'Path %s does not exist!' % sys.argv[1]
    
