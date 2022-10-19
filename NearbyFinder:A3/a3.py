'''
1) Sort the pointlist considering standard dictionary order : Call this x sorted list
2) Construct a segment tree with nodes containing subsets of the pointlist which lies in the corresponding
   interval of the segment tree node : Call the list in each of the node as y-sorted node list
PREPROCESSING ENDS : Total time: O(n*log(n))

QUERIES:
1) Binary search through the x-sorted list to get bounds on the point in terms of x (two binary searches : O(logn))
2) With the retrieved bounds, construct the bound interval from the nodes of the segment tree and binary search
   the y-sorted node list of each node to get the bound on points in y. Add all the points in the interval to final list
This gives the point in the square  
QUERIES END:
   TIME:
    Each of binary search in node of the tree takes O(logn) time and there will be at max log(n) nodes
    we will have to search (property of segment tree). so searching for the elements takes O(log(n)^2) time and appending
    m elements take O(m) time. Hence, total time is O( m + log(n)^2 )
    
'''

class TreeNode:
    # NODE CONTAINING : the interval bounds "_int"
    #                 : restaurants sorted in y co-ordinate "_data"
    #                 : LEft and right child : "_right , _left"
    __slots__ = ['_int','_data','_left','_right']

    def __init__(self,start,end):
        self._int = (start,end)
        self._data = None; self._left = None
        self._right = None

    def __str__(self):
        return f"( {self._int[0]} | {self._int[1]} )\nDATA : {str(self._data)}"

class SegmentTree:

    # SEGMENT TREE
    # _root : contains root of the tree
    # _size : number of nodes in the tree

    __slots__ = ['_root','_size']

    def __init__(self,data):
        self._root,nd = self.build(data,0,len(data)-1,TreeNode(0,len(data)-1))
        self._size = len(data)

    def __len__(self):
        return self._size

    def build(self,arr,left,right,node):
        # Building Segment Tree using Merge Sort algorithm
        # Time Complexity:
        #   recurrence relation : T(n) = 2T(n/2) + c1 + c2n
        #                       : taking n = 2^k
        #                       : T(n) = n + c1logn + c2*n*logn
        #                       O(n*logn)

        if left>right:
            return None, []
        elif left == right:
            data = [arr[left]]
            nd = TreeNode(left,right)
            nd._data = data
            return nd,data
        else:
            node._right, data1 = self.build(arr,((left+right)//2)+1,right,TreeNode(((left+right)//2)+1,right))
            node._left , data2 = self.build(arr,left,((left+right)//2),TreeNode(left,((left+right)//2)))
            data = self.merge(data1,data2)
            node._data = data
            return node, data
        
    def merge(self,L,R):
        # Helper function to merge sorted lists
        # O(len(L) + len(R))
        arr = []
        i = j = 0
        while i < len(L) and j < len(R):
                if L[i][1] <= R[j][1]:
                    arr.append(L[i])
                    i += 1
                else:
                    arr.append(R[j])
                    j += 1
        while i < len(L):
                arr.append(L[i])
                i += 1
    
        while j < len(R):
                arr.append(R[j])
                j += 1
        return arr

    def contained(self,interval,small):
        # To check if the smaller interval of the node is exactly contained in the x-search interval or not
        # O(1)
        if small[0]>=interval[0] and small[1] <= interval[1]: return 1 # Exactly contained
        elif small[0]>interval[1] or interval[0]>small[1]: return -1 # PArtial 
        else : return 2 #null
    
    def range_query(self,interval,node,points,q,d):
        # Performs Range Query in a given interval on the y-sorted data contained in the node
        # O(m + log(N)^2) as described in the algorithm in the start
        temp = self.contained(interval,node._int)
        if temp ==1 : # Eactly contained. Append all the correct points
            i1,i2 = getRange(q,d,node._data,-1,1),getRange(q,d,node._data,+1,1)           
            if i1 == i2 == None: return points
            for i in range(i1,i2+1):
                points.append(node._data[i])
            return points

        elif temp == 2: # Partially contained. Split the interval further
            points = self.range_query(interval,node._left,points,q,d); points = self.range_query(interval,node._right,points,q,d)
            return points
        else : # Null intersection
            return points 
        
class PointDatabase:

    __slots__ = ['_dataX','_dataTree']

    def __init__(self,pointlist):
        # Constructor to construct point database
        if not len(pointlist):
            self._dataTree = []
        else:
            pointlist.sort()
            self._dataX = pointlist.copy()
            self._dataTree = SegmentTree(pointlist)
    
    def searchNearby(self, q, d):
        # to handle queries
        if len(self._dataTree) == 0 or d==0:
            return []
        big = (getRange(q,d,self._dataX,-1,0),getRange(q,d,self._dataX,1,0))
        if big[0] == big[1] == None: return []
        return self._dataTree.range_query(big,self._dataTree._root,[],q,d)
    
def getRange(q,d,data,mid_pm,cord):
    # Helper function to implement binary search with parameters:
    # q,d : inputs to searchNearby
    # data : list on which the search is to be performed
    # cord : on which coords to perform the search
    # mid_pm : if +1 then search for upper bound, -1 then search for lower bound

    # O(logn) as it is basically a binary search
        i1 = None; start = 0; end = len(data) -1; mid = (start+end)//2
        if mid_pm == -1:
            if abs(data[0][cord] - q[cord])<=d: return 0
        else:
            if abs(data[end][cord] - q[cord])<=d: return end
        while( start <= end ):
                mid = (start+end)//2
                if abs(data[mid][cord] - q[cord])<=d:
                        if abs(data[mid+mid_pm][cord] - q[cord])>d : i1 = mid; break
                        else :
                            if mid_pm == - 1: end = mid-1
                            else:start = mid + 1
                else :
                    if data[mid][cord] > q[cord]:end = mid -1
                    else :start = mid +1
        return i1
