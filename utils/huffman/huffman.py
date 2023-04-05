import os
import sys
from .utils.priorityqueue import PriorityQueue
from .utils.node import Node
import sys

class Compress:

    def compress(inFile,outFile):
        infp = open(inFile,'r')
        text = infp.read()
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

        #for node in nodes.values():
            #print('Node %s has value %s and code %s'%(node.key,node.value,node.code))
                
        q = PriorityQueue()
        for node in nodes.values():
            q.enQueue(node)
        
        min1 = q.deQueue()
        min2 = q.deQueue()
        while min2:
            q.enQueue(min1+min2)
            min1 = q.deQueue()
            min2 = q.deQueue()
        
        root = min1
        #print(root)
        
        output = ''
        for char in text:
            if char in nodes:
                output += nodes[char].code
            else:
                print('Char object not found!')
                
        #Add psuedo-EOF marker
        output+= nodes[EOF].code
                
        #Build Header to store huffman tree
        header = Compress.traverseTree(root) + '1111111111111111'
        
        #Prepend header to output
        output = header + output
        
        while len(output)%8 != 0:
            output +='0'
        
        hexGrp = []    
        while output:
            hexGrp.append(output[:8])
            output = output[8:]

        output = bytes([int(group,2) for group in hexGrp])
        
        size = outfp.write(output)
        infp.close()
        outfp.close()
        
        return size
    
    def compress_from_storage(outFile, storage: str):
        text = storage
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

        #for node in nodes.values():
            #print('Node %s has value %s and code %s'%(node.key,node.value,node.code))
                
        q = PriorityQueue()
        for node in nodes.values():
            q.enQueue(node)
        
        min1 = q.deQueue()
        min2 = q.deQueue()
        while min2:
            q.enQueue(min1+min2)
            min1 = q.deQueue()
            min2 = q.deQueue()
        
        root = min1
        #print(root)
        
        output = ''
        for char in text:
            if char in nodes:
                output += nodes[char].code
            else:
                print('Char object not found!')
                
        #Add psuedo-EOF marker
        output+= nodes[EOF].code
                
        #Build Header to store huffman tree
        header = Compress.traverseTree(root) + '1111111111111111'
        
        #Prepend header to output
        output = header + output
        
        while len(output)%8 != 0:
            output +='0'
        
        hexGrp = []    
        while output:
            hexGrp.append(output[:8])
            output = output[8:]

        output = bytes([int(group,2) for group in hexGrp])
        
        size = outfp.write(output)
        outfp.close()
        
        return size

    def traverseTree(root):
        code = ''
        if not root:
            return code
        if root.left or root.right:
            code += '0'
        else:
            code += '1'
            #If psuedo-EOF marker
            if len(root.key)==2:
                code += '1111111111111111'
            else:
                ASCII = bin(ord(root.key))[2:]
                while len(ASCII) != 8:
                    ASCII = '0'+ASCII
                code += ASCII
        return code + Compress.traverseTree(root.left)+ Compress.traverseTree(root.right)
    
class decompress:
    def __init__(self,inFile,outFile):
        self.code = ''
        self.EOF = chr(255)+chr(255)
        self.nodes = {}
        self.EOFfound = False
        self.infp = open(inFile,'rb')
        self.outfp = open(outFile,'w')
        self.output = ''
        self.process()
    
    def process(self):
        try:
            self.gatherInput()
            self.rebuildTree()
            self.code = self.code[16:]
            self.decode()
            self.writeFile()
            self.cleanUp()
        except:
            pass
    
    def process_to_var(self):
        try:
            self.gatherInput()
            self.rebuildTree()
            self.code = self.code[16:]
            self.decode()
            return self.writeVar()
        except:
            return self.writeVar()
            pass

    def gatherInput(self):
        text = self.infp.read()
        hexGrp = []
        for char in text:
            hexGrp.append(bin(char)[2:])

        for group in hexGrp:
            while len(group) != 8:
                group = '0'+group
            self.code += group

    def rebuildTree(self,root=None):
        while self.code:
            if self.code[0] == '0':
                if root == None:
                    #print('New Root Node')
                    root = Node()
                    self.code = self.code[1:]
                    self.rebuildTree(root)
                else:
                    if not root.left:
                        if root.code == None:
                            root.left = Node(None,None,'0')
                        else:
                            root.left = Node(None,None,root.code+'0')
                        #print('New Left Node with code: %s'%root.left.code)
                        self.code = self.code[1:]
                        self.rebuildTree(root.left)
                    elif not root.right:
                        if root.code == None:
                            root.right = Node(None,None,'1')
                        else:
                            root.right = Node(None,None,root.code+'1')
                        #print('New Right Node with code: %s'%root.right.code)
                        self.code = self.code[1:]
                        self.rebuildTree(root.right)
                    else:
                        #print('UP')
                        return
            #self.code[0] == '1'
            else:
                if self.code[0:16] == '1'*16 and self.EOFfound:
                    #print('Terminating')
                    return root
                if not root.left:
                    if self.code[1:17] == '1'*16 and not self.EOFfound:
                        leaf = chr(int(self.code[1:9],2))+chr(int(self.code[9:17],2))
                        self.code = self.code[8:]
                        self.EOFfound = True
                    else:
                        leaf = chr(int(self.code[1:9],2))
                    root.left = Node(0,leaf,root.code+'0')
                    self.nodes[root.left.code] = leaf
                    #print('New left leaf Node %s with code: %s'%(leaf,root.left.code))
                    self.code = self.code[9:]
                elif not root.right:
                    if self.code[1:17] == '1'*16 and not self.EOFfound:
                        leaf = chr(int(self.code[1:9],2))+chr(int(self.code[9:17],2))
                        self.code = self.code[8:]
                        self.EOFfound = True
                    else:
                        leaf = chr(int(self.code[1:9],2))
                    root.right = Node(0,leaf,root.code+'1')
                    self.nodes[root.right.code] = leaf
                    #print('New Right Leaf Node %s with code: %s'%(leaf, root.right.code))
                    self.code = self.code[9:]
                else:
                    #print('UP')
                    return
                self.rebuildTree(root)
    
    def decode(self):
        start = 0
        end = 1
        while end <= len(self.code):
            if self.code[start:end] in self.nodes.keys():
                if self.nodes[self.code[start:end]] == self.EOF:
                    #print('Found EOF')
                    #print('Terminating')
                    return
                #print('Found %s'%self.nodes[self.code[start:end]])
                self.output += self.nodes[self.code[start:end]]
                start = end
                end += 1
            else:
                #print('Found Nothing')
                end += 1

    def writeFile(self):
        self.outfp.write(self.output)
    
    def writeVar(self):
        return self.output

    def cleanUp(self):
        self.infp.close()
        self.outfp.close()

class decompress_to_var:
    def __init__(self,inFile):
        self.code = ''
        self.EOF = chr(255)+chr(255)
        self.nodes = {}
        self.EOFfound = False
        self.infp = open(inFile,'rb')
        self.output = ''
        self.process_to_var()
    
    def process_to_var(self):
        try:
            self.gatherInput()
            self.rebuildTree()
            self.code = self.code[16:]
            self.decode()
            self.cleanUp()
            return self.writeVar()
        except:
            return self.writeVar()
            pass

    def gatherInput(self):
        text = self.infp.read()
        hexGrp = []
        for char in text:
            hexGrp.append(bin(char)[2:])

        for group in hexGrp:
            while len(group) != 8:
                group = '0'+group
            self.code += group

    def rebuildTree(self,root=None):
        while self.code:
            if self.code[0] == '0':
                if root == None:
                    #print('New Root Node')
                    root = Node()
                    self.code = self.code[1:]
                    self.rebuildTree(root)
                else:
                    if not root.left:
                        if root.code == None:
                            root.left = Node(None,None,'0')
                        else:
                            root.left = Node(None,None,root.code+'0')
                        #print('New Left Node with code: %s'%root.left.code)
                        self.code = self.code[1:]
                        self.rebuildTree(root.left)
                    elif not root.right:
                        if root.code == None:
                            root.right = Node(None,None,'1')
                        else:
                            root.right = Node(None,None,root.code+'1')
                        #print('New Right Node with code: %s'%root.right.code)
                        self.code = self.code[1:]
                        self.rebuildTree(root.right)
                    else:
                        #print('UP')
                        return
            #self.code[0] == '1'
            else:
                if self.code[0:16] == '1'*16 and self.EOFfound:
                    #print('Terminating')
                    return root
                if not root.left:
                    if self.code[1:17] == '1'*16 and not self.EOFfound:
                        leaf = chr(int(self.code[1:9],2))+chr(int(self.code[9:17],2))
                        self.code = self.code[8:]
                        self.EOFfound = True
                    else:
                        leaf = chr(int(self.code[1:9],2))
                    root.left = Node(0,leaf,root.code+'0')
                    self.nodes[root.left.code] = leaf
                    #print('New left leaf Node %s with code: %s'%(leaf,root.left.code))
                    self.code = self.code[9:]
                elif not root.right:
                    if self.code[1:17] == '1'*16 and not self.EOFfound:
                        leaf = chr(int(self.code[1:9],2))+chr(int(self.code[9:17],2))
                        self.code = self.code[8:]
                        self.EOFfound = True
                    else:
                        leaf = chr(int(self.code[1:9],2))
                    root.right = Node(0,leaf,root.code+'1')
                    self.nodes[root.right.code] = leaf
                    #print('New Right Leaf Node %s with code: %s'%(leaf, root.right.code))
                    self.code = self.code[9:]
                else:
                    #print('UP')
                    return
                self.rebuildTree(root)
    
    def decode(self):
        start = 0
        end = 1
        while end <= len(self.code):
            if self.code[start:end] in self.nodes.keys():
                if self.nodes[self.code[start:end]] == self.EOF:
                    #print('Found EOF')
                    #print('Terminating')
                    return
                #print('Found %s'%self.nodes[self.code[start:end]])
                self.output += self.nodes[self.code[start:end]]
                start = end
                end += 1
            else:
                #print('Found Nothing')
                end += 1

    def writeFile(self):
        self.outfp.write(self.output)
    
    def writeVar(self):
        return self.output

    def cleanUp(self):
        self.infp.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python decompress.py compressedFile.txt originalFile.txt')
        exit()
    if os.path.exists(sys.argv[1]):
        decompress(sys.argv[1],sys.argv[2])
    else:
        print('Path %s does not exist!'%sys.argv[1])
    