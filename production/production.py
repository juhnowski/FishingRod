import sys

class Data:
    def __init(self)__:
        self.isNull = true

    def set(self, t, v):
        self.t = t
        self.v = v
        
class Writer:
    def close(self):
        log("Closing...")

        if self.fd:
            self.fd.close()
            
        if self.fed:
            self.fed.close()
        
        try:
            if self.fad:
                self.fad.close()
        except:
            log("Error when store production file:" + self.baseName + "_all_data.txt")
            
        try:
            self.fal.close()
        except:
            print("Error to close log file: " + self.baseName + "_all_log.txt")
            
        exit(0)
        
    def ok(self):
        log("******************************")
        log("*             OK             *")
        log("******************************")   
        close()
                
    def error(self):
        log("******************************")
        log("*           ERROR            *")
        log("******************************")   
        close()
    
    def log(self,msg):
        if self.fal is None:
            print("datetime.datetime.utcnow().ctime():    " + msg)
        else:
            self.fal.write(msg+"\n")

    def __init__(self, name):
        print "Start data production"
        self.baseName = data[1]

        try:        
            self.fal = open(self.baseName + "_all_log.txt",'w+',0)
        except:
            print("Can not open log file:" + self.baseName + "_all_log.txt")
            close()
            
        try:
            self.fd = open(self.baseName + "_data.txt")
        except:
            log("Can not open log file:" + self.baseName + "_data.txt",'r')
            close()
                        
        try:
            self.fed = open(self.baseName + "_encoder_data.txt",'r')
        except:
            log("Can not open log file:" + self.baseName + "_encoder_data.txt")
            close()
            
        try:
            self.fad = open(self.baseName + "_all_data.txt",'w+',0)
        except:
            log("Can not open log file:" + self.baseName + "_all_data.txt")
            close() 
            
        self.ct = 0     # current time
        self.dct = 0.04 # delta time for 25 fps               
            
    def calculate(self, pd, nd, t):
    if nd:
        return pd.v + (t-pd.t)*(nd.v - pd.v)/(nd.t - pd.t)
    else:
        return pd.v
        
    pd = Data()
    nd = Data()
            
    def write(self):
                    



             

    

for line in f_data:
    if pd:
        
    else:
        pline = line.split(";")
        ct = 0
        pd.t = ct
        pd.v = pline[3]
        st =  pline[2]  # start time
        

pd = None
nd = None
class Data:
    pass
    


def interpol(self,pd,nd):
            
    return


def write(self,data):
    


f_data_line = f_data.readlines()
f_encoder_line = f_encoder.readlines()

data_fields = f_data_line.split(";")
data_time = float(fields_data[2])
data_value = float(fields_data[3])

start_time = data_time


while (f_data_line):
    data_fields = f_data_line.split(";")
    data_time = float(fields_data[2])
    data_value = float(fields_data[3])

    if (cur_time):
       cur_time += 0.04
    else:
        cur_time = data_time
        
    if cur_time > data_time:
    
    elif cur_time == data_time:
        value = data_value
    else:
        prev_data_time = data_time
        prev_data_value = data_value
    
    
f_data.close()
f_encoder.close()
f.close()

def readData(f,t):
    line = f.readlines()
    field = line.split(";")
    data = float(field[2]), float(field[3])
    interval = data, readData(f,t)


if len(sys.argv) != 1:
   print "Usage: production.py base files name."
            exit(0)
else:            
    writer = Writer(sys.argv[1])
    writer.write()
