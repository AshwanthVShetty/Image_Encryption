import time
start_time = time.time()

import base64
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from threading import Thread
from time import sleep
from multiprocessing import Process

prog=1

#Initial permut matrix for the datas
PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

#Initial permut made on the key
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

#Permut applied on shifted key to get Ki+1
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

#Expand matrix to get a 48bits matrix of datas to apply the xor with Ki
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

#SBOX
S_BOX = [
         
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
], 

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]

#Permut made after each SBox substitution for each round
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

#Final permut for datas after the 16 rounds
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

#Matrix that determine the shift for each round of keys
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]






def string_to_bit_array(text):#Convert a string into a list of bits
    array = list()
    for char in text:
        binval = binvalue(char, 8)#Get the char value on one byte
        array.extend([int(x) for x in list(binval)]) #Add the bits to the final list
    return array

def bit_array_to_string(array): #Recreate the string from the bit array
    res = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in  nsplit(array,8)]])   
    return res

def binvalue(val, bitsize): #Return the binary value as a string of the given size 
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0"+binval #Add as many 0 as needed to get the wanted size
    return binval

def nsplit(s, n):#Split a list into sublists of size "n"
    return [s[k:k+n] for k in range(0, len(s), n)]


def tostring(l):
    s=""
    for i in l:
        s=s+str(i)
    return s
def compliment(l):
    l1=[]
    for i in l:
        if i==0:
            l1.append(1)
        else:
            l1.append(0)
    return l1

def genMainKeys(Key_list,ki):
    l=[]
    for i in Key_list:
        s=list(i)
        s[ki]=bit_array_to_string(compliment(string_to_bit_array(s[ki])))
        l.append(tostring(s))
    return l

def substitute(d_e):#Substitute bytes using SBOX
        subblocks = nsplit(d_e, 6)#Split bit array into sublist of 6 bits
        result = list()
        for i in range(len(subblocks)): #For all the sublists
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2)#Get the row with the first and last bit
            column = int(''.join([str(x) for x in block[1:][:-1]]),2) #Column is the 2,3,4,5th bits
            val = S_BOX[i][row][column] #Take the value in the SBOX appropriated for the round (i)
            bin = binvalue(val, 4)#Convert the value to binary
            result += [int(x) for x in bin]#And append it to the resulting list
        return result
        
def permut(block, table):#Permut the given block using the given table (so generic method)
    return [block[x-1] for x in table]
    
def expand(block, table):#Do the exact same thing than permut but for more clarity has been renamed
    return [block[x-1] for x in table]
    
def xor(t1, t2):#Apply a xor and return the resulting list
    return [x^y for x,y in zip(t1,t2)]

def shift(g, d, n): #Shift a list of the given value
    return g[n:] + g[:n], d[n:] + d[:n]
    

ENCRYPT=1
DECRYPT=0

#class structure

class des():
    def __init__(self,password,g,d,action):
        self.password = password
        # self.text = None
        self.keys = list()
        self.g=g
        self.d=d     
        self.action=action 
        self.padding=False 


    def generatekeys(self):#Algorithm that generates all the keys
        self.keys = []
        key = string_to_bit_array(self.password)
        key =permut(key, CP_1) #Apply the initial permut on the key
        g, d = nsplit(key, 28) #Split it in to (g->LEFT),(d->RIGHT)
        for i in range(16):#Apply the 16 rounds
            g, d = shift(g, d, SHIFT[i]) #Apply the shift associated with the round (not always 1)
            tmp = g + d #Merge them
            self.keys.append(permut(tmp, CP_2)) #Apply the permut to get the Ki 
        
    def run(self,i):

        tmp = None

        d_e =expand(self.d, E) #Expand d to match Ki size (48bits)
        if self.action == ENCRYPT:
            tmp =xor(self.keys[i], d_e)#If encrypt use Ki
        else:
            tmp =xor(self.keys[15-i], d_e)#If decrypt start by the last key
        tmp = substitute(tmp) #Method that will apply the SBOXes
        tmp = permut(tmp, P)
        tmp = xor(self.g, tmp)
        self.g = self.d
        self.d = tmp
        
#end of class

def parallelRun(l,k):
    for i in range(16):
        l[i].run(k)

def shiftBlocks(l,act):
    if act==0:
        a=l[15].g
        b=l[15].d
        for i in reversed(range(15)):
            l[i+1].g=l[i].g
            l[i+1].d=l[i].d
        l[0].g=a
        l[0].d=b
    else:
        a=l[0].g
        b=l[0].d
        for i in range(15):
            l[i].g=l[i+1].g
            l[i].d=l[i+1].d
        l[15].g=a
        l[15].d=b

def getblock(a):
    result = permut(a.d+a.g, PI_1)
    final_res = bit_array_to_string(result)
    return final_res

def shiftbits(l,act):
    for i in l:
        l1=i.g+i.d
        # print l1
        if act==1:
            a=l1[63]
            for j in reversed(range(63)):
                l1[j+1]=l1[j]
            l1[0]=a
            i.g=l1[:32]
            i.d=l1[32:]
        else:
            a=l1[0]
            for j in range(63):
                l1[j]=l1[j+1]
            l1[63]=a
            i.g=l1[:32]
            i.d=l1[32:]





def encrypt(l,gen_keys):
    objects=[]
    for i in range(16):
        block=string_to_bit_array(l[i])
        block=permut(block,PI)
        g,d=nsplit(block,32)
        obj=des(gen_keys[i],g,d,ENCRYPT)
        obj.generatekeys()
        objects.append(obj)
    for i in range(16):
        parallelRun(objects,i)
        if i<15:
            shiftbits(objects,0)
            shiftBlocks(objects,0)
    res=[]
    for i in range(16):
        res.append(getblock(objects[i]))
    return res

def decrypt(l,gen_keys):
    objects=[]
    for i in range(16):
        block=string_to_bit_array(l[i])
        block=permut(block,PI)
        g,d=nsplit(block,32)
        obj=des(gen_keys[i],g,d,DECRYPT)
        obj.generatekeys()
        objects.append(obj)
    for i in range(16):
        parallelRun(objects,i)
        if i<15:
            shiftbits(objects,1)
            shiftBlocks(objects,1)
    res=[]
    for i in range(16):
        res.append(getblock(objects[i]))
    return res

def anim():
    for i in range (4):
        if prog==0:
            break
        print("...")
        sleep(1)
        





#shared set of 16 8byte keys
Key_list=["hello wo","abcd efg","bbb cccc","desalgoe","morningm","very bad","how ryou","key list","hello wo","abcd efg","bbb cccc","desalgoe","morningm","very bad","how ryou","key list"]


#reading plaintext from file
l=[]
ec=0
pt=[]
ps='        '



img="sample.jpg"            #image file input
pinput="photostring.txt"     #file to store the string representation of the image



with open(img,"rb") as imageFile:
    str1=base64.b64encode(imageFile.read())
with open(pinput,"w+") as f:
    f.write(str1)
with open(pinput) as f:
    while True:
        if ec!=16:
            c=f.read(8)
            if not c:
                break
            if len(c)!=8:
                for i in range(len(c),8):
                    c=c+' '
            l.append(c)
            ec=ec+1
        else:
            pt.append(l)
            l=[]
            ec=0
    if len(l)!=16 and len(l)!=0:
        for i in range(len(l),16):
            l.append(ps)
        pt.append(l)




#generate one time key index for the given plain text and this has to be sent to the decryptor 

b1=string_to_bit_array(Key_list[0])
b2=string_to_bit_array(pt[0][0])
ki=int(tostring(xor(b1,b2)),2)%8
print "\nOne Time Key:"
print ki

#based on the one time keyindex generated modify the key set of 16 8 bytes keys
gen_keys=genMainKeys(Key_list,ki)

print "Encrypting "+str(img)
thread=Thread(target=anim())
thread.start()


cipherText=""
ct=[]
for i in pt:
    cipher=encrypt(i,gen_keys)
    ct.append(cipher)
    cipherText=cipherText+tostring(cipher)

with open("output.txt","w+") as f:
    f.write(cipherText)
f.close()

prog=0
print "\nCiphertext is stored in output.txt file\n"
prog=1
print "\nDecrypting data from output.txt file\n"
thread=Thread(target=anim())
thread.start()


r=""
for i in ct:
    result=decrypt(i,gen_keys)
    r=r+tostring(result)

with open("decrypteddata.txt","w+") as f:
    f.write(r)
f.close()

prog=1
print "\nProcess completed"
print("--- %s seconds ---" % (time.time() - start_time))


imgdata = base64.b64decode(r)
filename = 'encoded.jpg'  
with open(filename, 'wb') as f:
    f.write(imgdata)

img=mpimg.imread('encoded.jpg')
imgplot = plt.imshow(img)
plt.show()

