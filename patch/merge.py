from scipy import interpolate
import numpy as np
from graph import graph
import sys
from ximu import xgraph

class merger:
    def __init__(self, dataPath, imagePath, namePrefix):
        self.data_path = dataPath
        self.image_path = imagePath
        self.name_prefix = namePrefix

    def merge(self):
        g = graph( self.data_path, self.image_path, self.name_prefix)
        tx,ty = g.readTXYData()
        ex,ey = g.readEXYData()
        if len(ey)<2:
            ex = np.arange(0,tx[-1],0.04)
            ey = np.arange(0,tx[-1],0.04)
            n = -1
            for e in ey:
                n = n + 1
                ey[n] = 0
                
        x_new = np.arange(0,tx[-1],0.04)

        tf = interpolate.interp1d(tx,ty)
        ef = interpolate.interp1d(ex,ey)

        tf_new = tf(x_new)
        
        ex_new = np.arange(0,ex[-1],0.04)
        ef_new=ef(ex_new)

# bridge sensor port 3 data
        tx3,ty3 = g.readTXYData3()
        x3_new = np.arange(0,tx3[-1],0.04)

        tf3 = interpolate.interp1d(tx3,ty3)
        tf3_new = tf(x3_new)
                    
# merge xIMU data
        xgr = xgraph(self.data_path, self.image_path, self.name_prefix)
        xbt = []
        xbt = xgr.readXBatTherm()
        
        xrm = []
        xrm = xgr.readXRotationMatrix()
        
        xq = []
        xq = xgr.readXQuaternion()
        
        xea = []
        xea = xgr.readXEulerAngles()
        
        xim = []
        xim = xgr.readXInertialMag()
        
# prepare data
        xbt_X=[]
        xbt_Y1=[]
        xbt_Y2=[]
         
        xbt_X.append(0)
        xbt_Y1.append(xbt[0].b)
        xbt_Y2.append(xbt[0].th)
        
        for dx in xbt:
            xbt_X.append(dx.t)
            xbt_Y1.append(dx.b)
            xbt_Y2.append(dx.th)

        xim_X=[]
        xim_Y11=[]
        xim_Y12=[]
        xim_Y13=[]
        xim_Y21=[]
        xim_Y22=[]
        xim_Y23=[]
        xim_Y31=[]
        xim_Y32=[]
        xim_Y33=[]

        xim_X.append(0)
        xim_Y11.append(xim[0].gx)
        xim_Y12.append(xim[0].gy)
        xim_Y13.append(xim[0].gz)
        xim_Y21.append(xim[0].ax)
        xim_Y22.append(xim[0].ay)
        xim_Y23.append(xim[0].az)
        xim_Y31.append(xim[0].mx)
        xim_Y32.append(xim[0].my)
        xim_Y33.append(xim[0].mz)
       
        for xim_dx in xim:
            xim_X.append(xim_dx.t)
            xim_Y11.append(xim_dx.gx)
            xim_Y12.append(xim_dx.gy)
            xim_Y13.append(xim_dx.gz)
            xim_Y21.append(xim_dx.ax)
            xim_Y22.append(xim_dx.ay)
            xim_Y23.append(xim_dx.az)
            xim_Y31.append(xim_dx.mx)
            xim_Y32.append(xim_dx.my)
            xim_Y33.append(xim_dx.mz)

        xea_X=[]
        xea_Y1=[]
        xea_Y2=[]
        xea_Y3=[]
        xea_X.append(0)
        xea_Y1.append(xea[0].rpx)
        xea_Y2.append(xea[0].pty)
        xea_Y3.append(xea[0].ypz)
        
        for dx in xea:
            xea_X.append(dx.t)
            xea_Y1.append(dx.rpx)
            xea_Y2.append(dx.pty)
            xea_Y3.append(dx.ypz)
            
        xq_X=[]
        xq_Y1=[]
        xq_Y2=[]
        xq_Y3=[]
        xq_Y4=[]

        xq_X.append(0)
        xq_Y1.append(xq[0].e1)
        xq_Y2.append(xq[0].e2)
        xq_Y3.append(xq[0].e3)
        xq_Y4.append(xq[0].e4)
        
        for dx in xq:
            xq_X.append(dx.t)
            xq_Y1.append(dx.e1)
            xq_Y2.append(dx.e2)
            xq_Y3.append(dx.e3)
            xq_Y4.append(dx.e4)
            
        xrm_X=[]
        xrm_Y11=[]
        xrm_Y12=[]
        xrm_Y13=[]
        xrm_Y21=[]
        xrm_Y22=[]
        xrm_Y23=[]
        xrm_Y31=[]
        xrm_Y32=[]
        xrm_Y33=[]
        xrm_X.append(0)
        xrm_Y11.append(xrm[0].e11)
        xrm_Y12.append(xrm[0].e12)
        xrm_Y13.append(xrm[0].e13)
        xrm_Y21.append(xrm[0].e21)
        xrm_Y22.append(xrm[0].e22)
        xrm_Y23.append(xrm[0].e23)
        xrm_Y31.append(xrm[0].e31)
        xrm_Y32.append(xrm[0].e32)
        xrm_Y33.append(xrm[0].e33)        
        for dx in xrm:
            xrm_X.append(dx.t)
            xrm_Y11.append(dx.e11)
            xrm_Y12.append(dx.e12)
            xrm_Y13.append(dx.e13)
            xrm_Y21.append(dx.e21)
            xrm_Y22.append(dx.e22)
            xrm_Y23.append(dx.e23)
            xrm_Y31.append(dx.e31)
            xrm_Y32.append(dx.e32)
            xrm_Y33.append(dx.e33)
           
# end prepare

# interpolation
        xbt_X_new = np.arange(0,xbt_X[-1],0.04)
        f_xbt_Y1 = interpolate.interp1d(xbt_X, xbt_Y1)
        f_xbt_Y2 = interpolate.interp1d(xbt_X, xbt_Y2)
        f_xbt_Y1_new = f_xbt_Y1(xbt_X_new)
        f_xbt_Y2_new = f_xbt_Y2(xbt_X_new)
#---        
        xim_X_new = np.arange(0,xim_X[-1],0.04)
        f_xim_Y11 = interpolate.interp1d(xim_X, xim_Y11)
        f_xim_Y12 = interpolate.interp1d(xim_X, xim_Y12)
        f_xim_Y13 = interpolate.interp1d(xim_X, xim_Y13)        

        f_xim_Y21 = interpolate.interp1d(xim_X, xim_Y21)
        f_xim_Y22 = interpolate.interp1d(xim_X, xim_Y22)
        f_xim_Y23 = interpolate.interp1d(xim_X, xim_Y23)        

        f_xim_Y31 = interpolate.interp1d(xim_X, xim_Y31)
        f_xim_Y32 = interpolate.interp1d(xim_X, xim_Y32)
        f_xim_Y33 = interpolate.interp1d(xim_X, xim_Y33)        
        
        f_xim_Y11_new = f_xim_Y11(xim_X_new)
        f_xim_Y12_new = f_xim_Y12(xim_X_new)
        f_xim_Y13_new = f_xim_Y13(xim_X_new)

        f_xim_Y21_new = f_xim_Y21(xim_X_new)
        f_xim_Y22_new = f_xim_Y22(xim_X_new)
        f_xim_Y23_new = f_xim_Y23(xim_X_new)

        f_xim_Y31_new = f_xim_Y31(xim_X_new)
        f_xim_Y32_new = f_xim_Y32(xim_X_new)
        f_xim_Y33_new = f_xim_Y33(xim_X_new)
#---
        xea_X_new = np.arange(0,xea_X[-1],0.04)
        f_xea_Y1 = interpolate.interp1d(xea_X, xea_Y1)
        f_xea_Y2 = interpolate.interp1d(xea_X, xea_Y2)
        f_xea_Y3 = interpolate.interp1d(xea_X, xea_Y3)
                
        f_xea_Y1_new = f_xea_Y1(xea_X_new)
        f_xea_Y2_new = f_xea_Y2(xea_X_new)
        f_xea_Y3_new = f_xea_Y3(xea_X_new)
#---
        xq_X_new = np.arange(0,xq_X[-1],0.04)
        f_xq_Y1 = interpolate.interp1d(xq_X, xq_Y1)
        f_xq_Y2 = interpolate.interp1d(xq_X, xq_Y2)
        f_xq_Y3 = interpolate.interp1d(xq_X, xq_Y3)
        f_xq_Y4 = interpolate.interp1d(xq_X, xq_Y4)
        
        f_xq_Y1_new = f_xq_Y1(xq_X_new)
        f_xq_Y2_new = f_xq_Y2(xq_X_new)
        f_xq_Y3_new = f_xq_Y3(xq_X_new)
        f_xq_Y4_new = f_xq_Y4(xq_X_new)
#---
        
        xrm_X_new = np.arange(0,xrm_X[-1],0.04)
        f_xrm_Y11 = interpolate.interp1d(xrm_X, xrm_Y11)
        f_xrm_Y12 = interpolate.interp1d(xrm_X, xrm_Y12)
        f_xrm_Y13 = interpolate.interp1d(xrm_X, xrm_Y13)        

        f_xrm_Y21 = interpolate.interp1d(xrm_X, xrm_Y21)
        f_xrm_Y22 = interpolate.interp1d(xrm_X, xrm_Y22)
        f_xrm_Y23 = interpolate.interp1d(xrm_X, xrm_Y23)        

        f_xrm_Y31 = interpolate.interp1d(xrm_X, xrm_Y31)
        f_xrm_Y32 = interpolate.interp1d(xrm_X, xrm_Y32)
        f_xrm_Y33 = interpolate.interp1d(xrm_X, xrm_Y33)        
        
        f_xrm_Y11_new = f_xrm_Y11(xrm_X_new)
        f_xrm_Y12_new = f_xrm_Y12(xrm_X_new)
        f_xrm_Y13_new = f_xrm_Y13(xrm_X_new)

        f_xrm_Y21_new = f_xrm_Y21(xrm_X_new)
        f_xrm_Y22_new = f_xrm_Y22(xrm_X_new)
        f_xrm_Y23_new = f_xrm_Y23(xrm_X_new)

        f_xrm_Y31_new = f_xrm_Y31(xrm_X_new)
        f_xrm_Y32_new = f_xrm_Y32(xrm_X_new)
        f_xrm_Y33_new = f_xrm_Y33(xrm_X_new)        
# end interpolation
        
        mf = open(g.data_path+g.name_prefix+"_merged.txt",'w+')
        len_tf3 = len(tf3_new) 
        len_ef = len(ef_new)
        len_xbt = len(f_xbt_Y1_new)
        len_xim = len(f_xim_Y11_new)
        len_xea = len(f_xea_Y1_new)
        len_xq = len(f_xq_Y1_new)
        len_xrm =len(f_xrm_Y11_new)
        
        i = -1
        for i in xrange(len(tf_new)-1):
            
            _tf_new = tf_new[i]
            
            if i < len_tf3:
                _tf3_new = tf3_new[i]
            else:
                _tf3_new = tf3_new[-1]
                
            if i < len_xbt:
                _f_xbt_Y1_new = f_xbt_Y1_new[i]
                _f_xbt_Y2_new = f_xbt_Y2_new[i]
            else:
                _f_xbt_Y1_new = f_xbt_Y1_new[-1]
                _f_xbt_Y2_new = f_xbt_Y2_new[-1]
            
            if i < len_xim:
                _f_xim_Y11_new = f_xim_Y11_new[i]
                _f_xim_Y12_new = f_xim_Y12_new[i]
                _f_xim_Y13_new = f_xim_Y13_new[i]
                _f_xim_Y21_new = f_xim_Y21_new[i]
                _f_xim_Y22_new = f_xim_Y22_new[i]
                _f_xim_Y23_new = f_xim_Y23_new[i]
                _f_xim_Y31_new = f_xim_Y31_new[i]
                _f_xim_Y32_new = f_xim_Y32_new[i]
                _f_xim_Y33_new = f_xim_Y33_new[i]
            else:
                _f_xim_Y11_new = f_xim_Y11_new[-1]
                _f_xim_Y12_new = f_xim_Y12_new[-1]
                _f_xim_Y13_new = f_xim_Y13_new[-1]
                _f_xim_Y21_new = f_xim_Y21_new[-1]
                _f_xim_Y22_new = f_xim_Y22_new[-1]
                _f_xim_Y23_new = f_xim_Y23_new[-1]
                _f_xim_Y31_new = f_xim_Y31_new[-1]
                _f_xim_Y32_new = f_xim_Y32_new[-1]
                _f_xim_Y33_new = f_xim_Y33_new[-1]            
            
            if i < len_xea:
                _f_xea_Y1_new = f_xea_Y1_new[i]
                _f_xea_Y2_new = f_xea_Y2_new[i]
                _f_xea_Y3_new = f_xea_Y3_new[i]
            else:
                _f_xea_Y1_new = f_xea_Y1_new[-1]
                _f_xea_Y2_new = f_xea_Y2_new[-1]
                _f_xea_Y3_new = f_xea_Y3_new[-1]            
            
            if i < len_xq:
                _f_xq_Y1_new = f_xq_Y1_new[i]
                _f_xq_Y2_new = f_xq_Y2_new[i]
                _f_xq_Y3_new = f_xq_Y3_new[i]
                _f_xq_Y4_new = f_xq_Y4_new[i]
            else:
                _f_xq_Y1_new = f_xq_Y1_new[-1]
                _f_xq_Y2_new = f_xq_Y2_new[-1]
                _f_xq_Y3_new = f_xq_Y3_new[-1]
                _f_xq_Y4_new = f_xq_Y4_new[-1]
            
            if i < len_xrm:
                _f_xrm_Y11_new = f_xrm_Y11_new[i]
                _f_xrm_Y12_new = f_xrm_Y12_new[i]
                _f_xrm_Y13_new = f_xrm_Y13_new[i]
                _f_xrm_Y21_new = f_xrm_Y21_new[i]
                _f_xrm_Y22_new = f_xrm_Y22_new[i]
                _f_xrm_Y23_new = f_xrm_Y23_new[i]
                _f_xrm_Y31_new = f_xrm_Y31_new[i]
                _f_xrm_Y32_new = f_xrm_Y32_new[i]
                _f_xrm_Y33_new = f_xrm_Y33_new[i]
            else:
                _f_xrm_Y11_new = f_xrm_Y11_new[-1]
                _f_xrm_Y12_new = f_xrm_Y12_new[-1]
                _f_xrm_Y13_new = f_xrm_Y13_new[-1]
                _f_xrm_Y21_new = f_xrm_Y21_new[-1]
                _f_xrm_Y22_new = f_xrm_Y22_new[-1]
                _f_xrm_Y23_new = f_xrm_Y23_new[-1]
                _f_xrm_Y31_new = f_xrm_Y31_new[-1]
                _f_xrm_Y32_new = f_xrm_Y32_new[-1]
                _f_xrm_Y33_new = f_xrm_Y33_new[-1]
            
            if i < len_ef:
                _ef_new = ef_new[i]
            else:
                _ef_new = ef_new[-1]
 
            mf.write("%.2f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f\n"%(i*0.04, _tf_new, _tf3_new, _ef_new, _f_xbt_Y1_new, _f_xbt_Y2_new, _f_xim_Y11_new, _f_xim_Y12_new, _f_xim_Y13_new, _f_xim_Y21_new, _f_xim_Y22_new, _f_xim_Y23_new, _f_xim_Y31_new, _f_xim_Y32_new, _f_xim_Y33_new, _f_xea_Y1_new, _f_xea_Y2_new, _f_xea_Y3_new, _f_xq_Y1_new, _f_xq_Y2_new, _f_xq_Y3_new, _f_xq_Y4_new, _f_xrm_Y11_new, _f_xrm_Y12_new, _f_xrm_Y13_new, _f_xrm_Y21_new, _f_xrm_Y22_new, _f_xrm_Y23_new, _f_xrm_Y31_new, _f_xrm_Y32_new, _f_xrm_Y33_new))
            
        mf.close()    

#if len(sys.argv) != 3 :
#    print("usage: python merge.py [data_path] [name_prefix]")
#    exit(0)

#m = merger(sys.argv[1],'/media/Workspace/phidget/sensor/stylesheets/',sys.argv[2])
#m = merger(sys.argv[1],'/media/Workspace/phidget/sensor/stylesheets/',sys.argv[2])
#m.merge()
#exit(0)

