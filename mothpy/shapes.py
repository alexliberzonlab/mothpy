import numpy as np
def circle(x, y, r=3):
    listx=[]
    listy=[]
    for i in range(int(y-r),int(y+r)):
        for j in range(int(x-r),int(x+r)):
            if np.sqrt(((i-y)**2)+((j-x)**2))<r :
                    listx.append(i)
                    listy.append(j)
    return (listx, listy)



def square(x, y, a=5): #generates a tuple of two lists that through pylab draw a square
            listx=[]
            listy=[]
            for i in range(int(x-a/2),int(x+a/2)):
                for j in range(int(y-a/2),int(y+a/2)):
                    listx.append(i)
                    listy.append(j)
            #print 'square summoned' 
            return (listx,listy)



#lists for drawing a large circle
cy =[235, 235, 235, 235, 235, 235, 235, 235, 235, 235, 235, 236, 236, 236, 236, 237, 237, 237, 237, 238, 238, 238, 238, 239, 239, 240, 240, 241, 241, 241, 241, 242, 242, 243, 243, 244, 244, 245, 245, 246, 246, 247, 247, 248, 248, 249, 249, 250, 250, 251, 251, 252, 252, 253, 253, 254, 254, 255, 255, 256, 256, 257, 257, 258, 258, 259, 259, 259, 259, 260, 260, 261, 261, 262, 262, 262, 262, 263, 263, 263, 263, 264, 264, 264, 264, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265]
cx = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 18, 19, 31, 32, 16, 17, 33, 34, 15, 16, 34, 35, 14, 36, 13, 37, 12, 13, 37, 38, 12, 38, 11, 39, 11, 39, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 11, 39, 11, 39, 12, 38, 12, 13, 37, 38, 13, 37, 14, 36, 15, 16, 34, 35, 16, 17, 33, 34, 18, 19, 31, 32, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
