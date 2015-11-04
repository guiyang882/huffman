import os
import sys
import pickle
import struct
from include.Node import Node

class TreeNode:
    def __init__(self,code=None,left=None,right=None):
        self.code = code
        self.left = left
        self.right = right

    def __str__(self):
        return "Node code %s, left %s, right %s" % (str(self.code),str(self.left),str(self.right))

class Tree:
    def __init__(self):
        self.root = TreeNode("")
    
    def is_empty(self):
        if self.root.left == None and self.root.right == None:
            return True
        return False
    
    def insert(self,key,code):
        for index in range(0,len(code)):
            direct = code[index]
            if direct == '0':
                pass
            if direct == '1':
                pass

def create_Huffman_tree(code_map):
    info = code_map.items()
    info.sort(key = lambda x:len(x[1]))
    node_list = []
    for item in info:
        node_list.append(Node(1,item[0],item[1]))

class decompress:
    def __init__(self,pickle_file,compressedfile,targetFile):
        handle = open(pickle_file,'rb')
        self.key_map = pickle.load(handle)
        handle.close()

        create_Huffman_tree(self.key_map)

        #print self.key_map
        self.code_content = []
        #print compressedfile
        handle = open(compressedfile,'rb')
        code_content = handle.read()
        handle.close()
        #print type(code_content),len(code_content)
        index = 0
        seg_list = []
        while index < len(code_content):
            sub_str = code_content[index:index+4]
            index = index + 4
            if index >= len(code_content):
                seg_list.append(bin(struct.unpack("I",sub_str)[0])[2:])
            else:
                seg_list.append(bin(struct.unpack("I",sub_str)[0])[2:].zfill(32))
        self.decode_content = "".join(seg_list)
        self.str_content = ""
        self.write_dest = targetFile
    
    def decode(self):
        index = 0
        total_length = len(self.decode_content)
        while index < total_length:
            flag = False
            for key,code in self.key_map.items():
                length = len(code)
                #print code,self.decode_content[index:index+length]
                if code == self.decode_content[index:index+length]:
                    #self.str_content = self.str_content + key
                    index = index + length
                    #print self.str_content
                    flag = True
                    if key == '\xff\xff':
                        index = total_length
                        break
                    self.str_content = self.str_content + key
                    break
            if flag == False:
                break
        #print self.str_content
        handle = open(self.write_dest,"w")
        handle.write(self.str_content)
        handle.close()
        print "Decode Finished !"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python decompress.py compressedFile.bin test.txt'
        sys.exit(0)

    if os.path.exists(sys.argv[1]) == False:
        print 'Path %s does not exist!'%sys.argv[1]
        sys.exit(0)
    obj = decompress("./result/key.pkl","./result/a.bin",sys.argv[2])
    #obj.decode()
