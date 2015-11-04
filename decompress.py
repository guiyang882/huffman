import os
import sys
import pickle
import struct
#from include.Node import Node

class decompress:
    def __init__(self,pickle_file,compressedfile,targetFile):
        handle = open(pickle_file,'rb')
        self.key_map = pickle.load(handle)
        handle.close()
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
    
    def test_json(self):
        for key,code in self.key_map.items():
            if key == '\xff\xff':
                print key,code

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python decompress.py compressedFile.bin test.txt'
        sys.exit(0)

    if os.path.exists(sys.argv[1]) == False:
        print 'Path %s does not exist!'%sys.argv[1]
        sys.exit(0)
    obj = decompress("./result/key.pkl","./result/a.bin",sys.argv[2])
    #obj.test_json()
    obj.decode()
