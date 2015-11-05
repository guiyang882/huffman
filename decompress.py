import os
import sys
import pickle
import struct
import copy
#from include.Node import Node

class TreeNode:
    def __init__(self,code=None,key=None,left=None,right=None):
        self.key = key
        self.code = code
        self.left = left
        self.right = right

    def __str__(self):
        #return "key %s, left %s, right %s" % (str(self.key),str(self.left),str(self.right))
        if self.key != None:
            return "Key %s" % self.key
        return ""

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

    def insert(self,node,code,key,index):
        #print repr(code),len(code)
        if index == len(code)-1:
            if code[index] == '0' and node.left == None:
                node.left = TreeNode("",key)
            elif code[index] == '0' and node.left != None:
                node.left.setkey(key)

            if code[index] == '1' and node.right == None:
                node.right = TreeNode("",key)
            elif code[index] == '1' and node.right != None:
                node.right.setkey(key)
            return True

        c = code[index]
        index = index + 1
        if c == '0':
            if node.left == None:
                node.left = TreeNode("")
            self.insert(node.left,code,key,index)
        elif c == '1':
            if node.right == None:
                node.right = TreeNode("")
            self.insert(node.right,code,key,index)

    def preOrderTree(self,root):
        if root != None:
            print root
        if root.left != None:
            self.preOrderTree(root.left)
        if root.right != None:
            self.preOrderTree(root.right)
    
    def combine_key_map(self,root,code):
        if root != None and root.left == None and root.right == None:
            print root.key,code
        if root.left != None:
            self.combine_key_map(root.left,code + "0")
        if root.right != None:
            self.combine_key_map(root.right,code + "1")


def create_Huffman_tree(code_map):
    info = code_map.items()
    info.sort(key = lambda x:len(x[1]))
    TreeObj = Tree()
    for item in info:
        TreeObj.insert(TreeObj.getRoot(),item[1],item[0],0)
    root = TreeObj.getRoot()
    #TreeObj.combine_key_map(root,"")
    return root

class decompress:
    def __init__(self,pickle_file,compressedfile,targetFile):
        handle = open(pickle_file,'rb')
        self.key_map = pickle.load(handle)
        handle.close()
        self.root = create_Huffman_tree(self.key_map)
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

    def tree_decode(self):
        page_content = ""
        current = copy.deepcopy(self.root)
        for index in range(0,len(self.decode_content)):
            if self.decode_content[index] == '0':
                current = current.left
                if current != None and current.key != None:
                    if current.key != '\xff\xff':
                        page_content = page_content + current.key
                        current = copy.deepcopy(self.root)
                    if current.key == '\xff\xff':
                        break
                if current == None:
                    print "Tree or Code Error !"
                    raise TypeError

            elif self.decode_content[index] == '1':
                current = current.right
                if current != None and current.key != None:
                    if current.key != '\xff\xff':
                        page_content = page_content + current.key
                        current = copy.deepcopy(self.root)
                    if current.key == '\xff\xff':
                        break
                if current == None:
                    print "Tree or Code Error !"
                    raise TypeError

        handle = open(self.write_dest,"w")
        handle.write(page_content)
        handle.close()
        print "Use Prefix to decode the File Finished !"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python decompress.py compressedFile.bin test.txt'
        sys.exit(0)
    if os.path.exists(sys.argv[1]) == False:
        print 'Path %s does not exist!'%sys.argv[1]
        sys.exit(0)
    obj = decompress("./result/key.pkl","./result/a.bin",sys.argv[2])
    #obj.decode()
    obj.tree_decode()
