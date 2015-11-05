import os
import sys
import pickle
import struct
#from include.Node import Node

class TreeNode:
    def __init__(self,code=None,key=None,left=None,right=None):
        self.key = key
        self.code = code
        self.left = left
        self.right = right

    def __str__(self):
        return "Node key %s, left %s, right %s" % (str(self.key),str(self.left),str(self.right))

    def setkey(self,key):
        self.key = key

class Tree:
    def __init__(self):
        self.root = TreeNode("")

    def is_empty(self):
        if self.root.left == None and self.root.right == None:
            return True
        return False

    def getRoot(self):
        return self.root

    def insert(self,node,code,key):
        if len(code) == 1:
            print "prepare insert "
            print code
            if code[0] == '0' and node.left == None:
                node.left = TreeNode("",key)
                print "Here 1",node.left
            elif code[0] == '0' and node.left != None:
                node.left.setkey(key)
                print "Here 2",node.left

            if code[0] == '1' and node.right == None:
                node.left = TreeNode("",key)
                print "Here 3",node.right
            elif code[0] == '1' and node.right != None:
                node.right.setkey(key)
                print "Here 4",node.right
            return True
        c = code[0]
        newcode = code[1:]
        print newcode
        if c == '0':
            if node.left == None:
                node.left = TreeNode("")
            self.insert(node.left,key,newcode)
        if c == '1':
            if node.right == None:
                node.right = TreeNode("")
            self.insert(node.right,key,newcode)

    def preOrderTree(self,root):
        if root != None:
            print root
        if root.left != None:
            self.preOrderTree(root.left)
        if root.right != None:
            self.preOrderTree(root.right)

def create_Huffman_tree(code_map):
    info = code_map.items()
    info.sort(key = lambda x:len(x[1]))
    TreeObj = Tree()

    for item in info:
        print item[1],item[0]
        TreeObj.insert(TreeObj.getRoot(),item[1],item[0])
        sys.exit(0)
    TreeObj.preOrderTree(TreeObj.getRoot())

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
