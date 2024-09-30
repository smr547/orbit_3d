import os 
import time

def parentchild(cwrites): 
   r, w = os.pipe() 
   pid = os.fork() 
   if pid < 0:
       print("fork() failed ", pid)
       os.exit()

   if pid: 
      os.close(w) 
      r = os.fdopen(r, "r") 
      print ("Parent is reading") 
      while True:
          s = r.readline() 
          print( "Parent reads =", s) 
   else: 
      os.close(r) 
      w = os.fdopen (w, 'w') 
      print ("Child is writing") 
      while True:
          w.write(cwrites) 
          w.flush()
          print("Child writes = ",cwrites) 
          time.sleep(0.01)
      w.close() 
# Driver code         
cwrites = "Python Program\n"
parentchild(cwrites) 
