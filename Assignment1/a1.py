'''
COL106 Semester 1 2022-23
Assignment 1
@Author : Vaibhav Seth
Entry Number: 2021MT10236
'''
class Stack:
    #defining a stack using Linked List
    __slots__=['_head','_size']
    class _Node:
        __slots__ = ['_value','_next']
        def __init__(self,value,next):
            self._value = value
            self._next = next       
    def __init__(self):
        self._head = None
        self._size = 0 
    def __len__(self):
        return self._size    
    def push(self,e):
        self._head = self._Node(e,self._head)
        self._size+=1
    def pop(self):
        if self._size == 0:
            raise ValueError('STACK EMPTY')
        val = self._head._value
        self._head = self._head._next
        self._size-=1
        return val
    def top(self):
        return self._head._value

#main function that calculates the final distance
def findPositionandDistance(P):
    #INPUT: P : String: Given path
    #OUTPUT: List: Co-ordinates and total path length
    stk = Stack()
    return calc_moves(stk,P)

# Function to calculate the fligh_path
# calculating the flight_path by summing the moves inside a pair of brackets and pushing it to a Stack, multiplying it with the specified factor which is also pushed to the stack, and adding it to the final_path
def calc_moves(stk,P):
    # INPUT : stk <class 'Stack'> : Stack to store the open brackets, and the number preceding the respective bracket
    #        P <class 'str'> : The flight program
    #
    # OUTPUT: path <class 'list'> : The final path taken by the drone
    moves = {'+X':([1,0,0,1]),'-X':([-1,0,0,1]),'+Y':([0,1,0,1]),'-Y':([0,-1,0,1]),'+Z':([0,0,1,1]),'-Z':([0,0,-1,1])} # list to store the basic moves
    num = '' #stores the number before a bracket
    path = [0,0,0,0] #initializing the path variable
    i = 0 #loop variable
    while i<len(P): # LOOP INVARIANT: i<length of the program
        if P[i].isnumeric(): num+=P[i]; i+=1 #extracting the number before an open bracket
        else:
            if P[i] == ')': #if bracket closed, pop and all the elements after the nearest integer value and multiply the sum with the nearest integer
                while type(stk.top()) is list:
                    ele = stk.pop()
                    for k in range(4):
                        path[k] = path[k]+ele[k]
                a = int(stk.pop())
                for k in range(4):
                     path[k] = path[k]*a
                i+=1
            elif P[i] == '(': # if open bracket, push the number corresponding to the bracket to the stack, and the total path taken before the bracket to the stack and
                              # set path to [0,0,0,0]
                if path==[0,0,0,0]:
                    stk.push(num);num=''
                else:
                    stk.push(path);stk.push(num);num=''
                path = [0,0,0,0]
                i+=1
            else:
                # No brackets, just a normal move operation. So add that to the path
                move = moves[P[i]+P[i+1]];i+=2
                for k in range(4):
                    path[k]+=move[k]            

    while(not len(stk)==0): #to clear up the remaining eleemnts in the stack after the last bracket is closed
            ele = stk.pop()
            for k in range(4):
                path[k] = path[k]+ele[k]
    return(path)
    # Time Complexity : O(n)
    # The while loop runs from 0 to n and each index is referenced only once. Between the loop there are some O(1) functions but they add up to take a constant time
    # hence overall it's O(n)
