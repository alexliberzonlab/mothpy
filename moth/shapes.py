import numpy as np
def circle(array, x, y, r=3, color = (1,0,0)):
    for i in range(int(y-r),int(y+r)):
        for j in range(int(x-r),int(x+r)):
            if np.sqrt((i-y)**2+((j-x)**2))<r :
                array[i][j] = color



def square(array,x, y, a=2, color = (0,1,0)):
           array[y-a:y+a,x-a:x+a] = color


