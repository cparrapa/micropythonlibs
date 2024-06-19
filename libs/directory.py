try: 
   import os 
except ImportError: 
   import uos as o 
 
class Directory: 
    directory = '/' 
 
    def __init__(self): 
        print('') 
 
    def listdir(self, directory): 
        if self.directory == '/': 
            return sorted([self.directory + f for f in os.listdir(self.directory)]) 
        else: 
            return sorted([self.directory + '/' + f for f in os.listdir(self.directory)]) 
 
    def ListOttoFiles(self): 
        print('&') 
        for f in self.listdir(self.directory): 
            size = os.stat(f)[6] 
            print(f) 
        print('%') 