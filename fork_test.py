import os 
def parentchild(cwrites): 
   r, w = os.pipe() 
   pid = os.fork() 
   if pid: 
      os.close(w) 
      r = os.fdopen(r) 
      print ("Parent is reading") 
      str = r.read() 
      print( "Parent reads =", str) 
   else: 
      os.close(r) 
      w = os.fdopen (w, 'w') 
      print ("Child is writing") 
      w.write(cwrites) 
      print("Child writes = ",cwrites) 
      w.close() 
# Driver code         
cwrites = "Python Program"
parentchild(cwrites) 
