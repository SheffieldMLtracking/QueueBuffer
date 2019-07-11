import queue
import threading

class QueueBuffer():
    def __init__(self,size=10):
        """Create a queue buffer. One adds items by calling the put(item) method.
        One can wait for new items to be added by using the blocking pop() method
        which returns the index and the item that have been added. One can read
        items that have been added previously using the read(index) method.
        
        The constructor takes one optional argument, size, which means older items
        are deleted."""
        
        self.inbound = queue.Queue() #an internal queue to manage the class properly in a thread safe manner.
        self.index = 0 #index of next item to be added.
        self.buffer = [] #the buffer we will store things in.
        self.size = size #the maximum size of the buffer
        self.newitem = threading.Event() #a blocking event to control the pop method
        t = threading.Thread(target=self.worker) #the worker that will run when items are added.
        t.start() #start the worker
        self.newitemindex = 0 #index of items to pop
        
    def worker(self):
        """
        Helper function, internally blocks until an item is added to the internal
        queue, this is then added into our buffer, and various indices are sorted.
        """
        while True:
            item = self.inbound.get()
            self.buffer.append(item)
            self.index += 1 #index of next item for buffer
            if len(self.buffer)>self.size:
                del self.buffer[0]
            self.newitem.set()
            
    def put(self,item):
        """
        Add an item to the queue. 
        """
        self.inbound.put(item)
        
              
    def read(self,getindex):
        """Read item at index getindex. Returns the item. Fails if item no longer exists."""
        if getindex<0:
            print("Indicies are non-negative")
            return None
        try:
            bufinx = len(self.buffer)+(getindex - self.index)
            if bufinx<0:
                print("This item has been deleted, try increasing the queue size")
                return None
            return self.buffer[bufinx]
        except IndexError:
            print("This item doesn't exist yet")
            return None
        
    def pop(self):
        """Blocks until a new item is added. Returns the index and the item.
        !Item remains in the QueueBuffer, so 'pop' is slightly misleading.
        
        It will return (index,None) if the item has already been lost from the buffer."""
        self.newitem.wait()
        if self.newitemindex+1==self.index: self.newitem.clear()
        index = self.newitemindex
        item = self.read(index)
        self.newitemindex += 1
                
        return index, item      
    
