# Example:
#g = graph('/media/Workspace/phidget/sensor/data/','/media/Workspace/phidget/sensor/stylesheets/','q10')
#g.saveTData()
#

from pylab import *

class TData:
    def __init__(self,t,v):
        self.t = t
        self.v = v
          
class EData:
    def __init__(self,t,dv,dt,v):
        self.t = t      #time
        self.dv = dv    #delta value (position)
        self.dt = dt    #delta t
        self.v = v      #value (position)
        
class graph:
    def __init__(self, dataPath, imagePath, namePrefix):
        self.data_path = dataPath
        self.image_path = imagePath
        self.name_prefix = namePrefix
    
    def readTData(self):
        f = open(self.data_path + self.name_prefix + '_data.txt','r')
        lines = f.readlines()
        data = []
        start_time = -1.0
        for line in lines:
            d = line.split(";")
            if start_time == -1.0:
                start_time = float(d[2])
            data.append(TData(float(d[2])-start_time,float(d[3])))
        f.close()
        return data    

    def readTXYData(self):
        f = open(self.data_path + self.name_prefix + '_data.txt','r')
        lines = f.readlines()
        x = []
        y = []
        start_time = -1.0
        for line in lines:
            d = line.split(";")
            if start_time == -1.0:
                start_time = float(d[2])
            x.append(float(d[2])-start_time)
            y.append(float(d[3]))
        f.close()
        return x,y

    def readTXYData3(self):
        f = open(self.data_path + self.name_prefix + '_3_data.txt','r')
        lines = f.readlines()
        x = []
        y = []
        start_time = -1.0
        for line in lines:
            d = line.split(";")
            if start_time == -1.0:
                start_time = float(d[2])
            x.append(float(d[2])-start_time)
            y.append(float(d[3]))
        f.close()
        return x,y
                        
    def plotTData(self):
        d = self.readTData()
        X=[]
        Y=[]
        for dx in d:
            X.append(dx.t)
            Y.append(dx.v)
        plot (X, Y, color='blue', alpha=1.00)
        show()
        clf()
        
    def saveTData(self):
        d = self.readTData()
        X=[]
        Y=[]
        for dx in d:
            X.append(dx.t)
            Y.append(dx.v)
        plot (X, Y, color='blue', alpha=1.00)
        savefig(self.image_path + self.name_prefix + '_data.png')
        clf()
        
    def readEData(self):
        f = open(self.data_path + self.name_prefix + '_encoder_data.txt','r')
        lines = f.readlines()
        data = []
        start_time = -1.0
        for line in lines:
            d = line.split(";")
            if start_time == -1.0:
                start_time = float(d[2])
            data.append(EData(float(d[2])-start_time,float(d[3]),float(d[4]),float(d[5])))
        f.close()
        return data
        
    def readEXYData(self):
        f = open(self.data_path + self.name_prefix + '_encoder_data.txt','r')
        lines = f.readlines()
        x = []
        y = []
        start_time = -1.0
        for line in lines:
            d = line.split(";")
            if start_time == -1.0:
                start_time = float(d[2])
            x.append(float(d[2])-start_time)
            y.append(float(d[5]))
        f.close()
        return x,y
        
        
    def plotEData(self,isPrintValue):
        d = self.readEData()
        X=[]
        if isPrintValue:
            Y=[]
        else:
            DY=[]
        for dx in d:
            X.append(dx.t)
            if isPrintValue:
                Y.append(dx.v)
            else:
                DY.append(dx.dv)

        if isPrintValue:
            plot (X, Y, color='blue', alpha=1.00)
        else:
            plot (X, DY, color='green', alpha=1.00)
        show() 
        clf()
        
    def saveEValueData(self):
        d = self.readEData()
        X=[]
        Y=[]
        
        for dx in d:
            X.append(dx.t)
            Y.append(dx.v)

        plot (X, Y, color='blue', alpha=1.00)
            
        savefig(self.image_path + self.name_prefix + '_value_encoder_data.png')
        clf()
        
    def saveEDeltaData(self):
        d = self.readEData()
        X=[]
        DY=[]
        
        for dx in d:
            X.append(dx.t)
            DY.append(dx.dv)

        plot (X, DY, color='green', alpha=1.00)
            
        savefig(self.image_path + self.name_prefix + '_delta_encoder_data.png')
        clf()
          
    def saveEData(self,isPrintValue):
        if isPrintValue:
            self.saveEValueData()
        else:
            self.saveEDeltaData()

    def saveAllData(self):
	self.saveEValueData()
	self.saveEDeltaData()
	self.saveTData()