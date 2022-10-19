class node:

    __slots__ = ['_time','_ind']
    #initialization
    def __init__(self,t,i):
        #INPUT : t : float : time of i and i+1 collison
        #        i : the index i 
        self._time = t
        self._ind = i


    #redfining less than operator
    def __lt__(self, other):
        # INPUT : other : object of class node
        # OUTPUT : float : lesser of self and other
        if self._time == other._time:
            return self._ind < other._ind
        return (self._time < other._time)

    #redifining greater than operator
    def __gt__(self, other):
        # INPUT : other : object of class node
        # OUTPUT : float : greater of self and node
        if self._time == other._time:
            return self._ind > other._ind
        return(self._time > other._time)
    
    def __str__(self):
        return '(' + str(self._time)+' ,'+str(self._ind)+')'

class heap:
    #Initialization of heap
    __slots__ = ['_data','_indices']
    def __init__(self,l=None):
        self._data = []
        self._indices = []
        if l is not None:
            self.build_heap(l)
    
    def __len__(self):
        return len(self._data)

    def build_heap(self,l):
        # O(n) heap building using keys from list l
        self._indices  = [-1]*len(l)
        self._data = l
        for i in range(len(l)-1,-1,-1):
            self._indices[i] = l[i]._ind
            self._heap_down(i)
              
    def _enqueue(self,ele,requeue = False):
        #enqueueing element e in O(log(n))
        # FOR THIS ASSIGNMENT; requeue is used: if requeue is True that means the i-collision was previously in the heap and we are adding it again
        self._data.append(ele)
        if requeue:
            self._indices[ele._ind] = len(self)-1
        self._heap_up(len(self)-1)

    def _heap_up(self,i):
        # O(log(n)) Heap up operation over the heap
        ind = self._get_parent(i)
        while self._data[i]<self._data[ind] and i>0:
            self._data[i],self._data[ind] = self._data[ind],self._data[i]
            self._indices[self._data[i]._ind], self._indices[self._data[ind]._ind] = self._indices[self._data[ind]._ind],self._indices[self._data[i]._ind]
            i  = ind
            ind = self._get_parent(i)
    
    def _extract_min(self):
        #Extracting min element using heap down in O(log(n))
        if len(self._data)==1:
            min =  self._data[0]
            self._data = []
            self._indices[min._ind] = -1
            return min
        min = self._dequeue()
        return min
    
    def _dequeue(self,i=-1):
        # To dequeue the i and i+1 collision if i!=-1. if i == -1, then to extract the minimum element
        # O(log(n))
        ind = self._indices[i] # index in the
        if i == -1: # to assist extract_min
            ind = 0
        data, val = self._data[ind],self._data[-1]
        self._indices[val._ind],self._indices[data._ind] = self._indices[data._ind],-1
        self._data[ind] = val; self._data.pop(); self._heap_down(ind)
        return data

    def _heap_down(self,i):
        # O(log(n))
        ind = self._get_min_child(i)
        if ind == -1:
            return
        while self._data[i]>self._data[ind] and ind != -1:
            self._data[i],self._data[ind] = self._data[ind],self._data[i]
            self._indices[self._data[i]._ind], self._indices[self._data[ind]._ind] = self._indices[self._data[ind]._ind],self._indices[self._data[i]._ind]
            i  = ind
            ind = self._get_min_child(i)
        return

    def _get_min_child(self,i):
        #returns minimum child of element at index i (if exists else 1)
        left = self._get_left_child(i)
        right = self._get_right_child(i)
        if left == right ==-1:
            return -1
        if left == -1:
            return right
        if right == -1:
            return left
        return left if self._data[left]<self._data[right] else right

    def _get_parent(self,i):
        #returns index of parent if exist (else -1)
        if len(self)==0:
            return -1
        return (i-1)//2

    def _get_left_child(self,i):
        #returns index of left child (if exists else -1)
        if 2*i+1>=len(self):
            return -1
        return (2*i+1)

    def _get_right_child(self,i):
        #returns index of right child (if exist else -1)
        if 2*i+2>=len(self):
            return -1
        return 2*i+2

    def __str__(self):
        return str([str(i) for i in self._data])

def get_col_vel(i,M,v):
    #returns velocities after collision of i and i+1 particle
    v1 = ((2*M[i+1]*v[i+1])/(M[i] + M[i+1])) + ((M[i]-M[i+1])/(M[i]+M[i+1]))*v[i]
    v2= ((2*M[i]*v[i])/(M[i] + M[i+1])) - ((M[i]-M[i+1])/(M[i]+M[i+1]))*v[i+1]
    return v1,v2

def listCollisions(M,x,v,m,T):
    n = len(M)
    state = [] #stores the ient state of collisions of particles (v1,v2,time of future collision, and co-ord)
    prev = [0]*(n) #time of past collisions of each particle

    for i in range(n-1): #storing initial time of collision of all adjacent particle pair to the state variable and the building heap from this list
        if v[i+1]>=v[i]: #if i+1 has a greater velocity then particles never collides
            state.append([float('inf'),i])
        else:
            state.append([abs((x[i+1]-x[i])/(v[i+1]-v[i])),i])
    
    hip = heap([node(i[0],i[1]) for i in state]) #heap of (t,i) of future collisions
    tick = 0; col = 0; cols = [] #tick : total time elapsed; col: total collision occured; cols[] : final list of collisions

    while tick<=T and col<m:

        top = hip._extract_min() #get the min element
        i = top._ind
        tick = top._time

        if tick>T: #time exceeded. break out of loop and print collisions list
            break      

        t_col = tick - prev[i] #time AFTER the last collision
        x[i]+=v[i]*t_col ;x[i+1] = x[i] #change in position due to collision
        v[i],v[i+1] = get_col_vel(i,M,v) #updating post-collision velocities of the i and i+1 particles
        prev[i] = prev[i+1] = tick #changing the time of last collision to current time for the i and i+1 particles

        cols.append((top._time,top._ind,x[i])) # appending the collision

        top._time = float('inf') # changing the time of next collision to inf as particles won't collide until velocities change
        hip._enqueue(top,True) #enqueueuing the updated i,i+1 collide to the heap
          
        if i!=0: #updating i-1 and i collision if i ! = 0

            left = hip._dequeue(i-1)
            time_to_col= 0 #time for collision between i-1 and i particle at their current init positions and velocities

            if v[i]>=v[i-1] :
                time_to_col = float('inf')
            else :
                time_to_col = abs((x[i] - (x[i-1]+v[i-1]*(tick-prev[i-1])))/(v[i]-v[i-1]))

            left._time = tick + time_to_col
            hip._enqueue(left,True)

        if i!=n-2: #updating i+1 and i+2 collision

            right = hip._dequeue(i+1)
            time_to_col = 0 #time for collision between i and i+1 particle at their current init positions and velocities

            if v[i+2]>=v[i+1]:
                time_to_col = float('inf')
            else:
                time_to_col = abs((x[i+1] - (x[i+2]+v[i+2]*(tick-prev[i+2])))/(v[i+1]-v[i+2]))

            right._time = tick+time_to_col
            hip._enqueue(right,True)

        col+=1
    
    return  cols