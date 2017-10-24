# -*- coding: utf-8 -*-
from Class_XLSManager import XLSManager as xlsm
from Class_SRFRead import SRFRead as sr
from Class_VIComputer import VIComputer as vic
import scipy.interpolate as itp
import matplotlib.pyplot as plt
import numpy as np

root = "C:\\Users\\Administrator\\Desktop\\SOIL SPECTRUM\\soilSpectralWet\\"
fileName = "wetSoilSpectral.xls"
srInstance = sr('landsat8All.txt')
spectralWavelength = np.arange(0.42,2.401,0.01)
soilSpectrals =  xlsm.getXLSValue(root,fileName)
#print(soilSpectrals)
srfResults = []
for i in range(len(soilSpectrals)):
    spectral = soilSpectrals[i,:]
    result,name = vic.spectralRespond_comp(srInstance,spectralWavelength,spectral)
    srfResults.append(result)


piValues = []
viValues = []
giValues = [] 
for i in range(10):
    srf9 = srfResults[i*9 : 9 + i*9]
    srf9 = np.array(srf9)
    piValue = vic.NDPI_comp(srf9[:,2],srf9[:,3],srf9[:,4],arf = 0.73)
    viValue = vic.NDVI_comp(srf9[:,2],srf9[:,3])
    giValue = vic.NDGI_comp(srf9[:,1],srf9[:,2],srf9[:,3],arf = 0.58)
    piValues.append(np.var(piValue))
    viValues.append(np.var(viValue))
    giValues.append(np.var(giValue))
print('NDPI')
print(piValues)
print('NDGI')
print(giValues)
print('NDVI')
print(viValues)

print('NDPI')
print(np.mean(piValues))
print('NDGI')
print(np.mean(giValues))
print('NDVI')
print(np.mean(viValues))


plt.figure(figsize=(10,7))
plt.bar(range(3), [np.mean(piValues),np.mean(giValues),np.mean(viValues)],color='k')
plt.xticks(range(3),['NDPI','NDGI','NDVI'],rotation=45)
plt.grid()
plt.xlabel('VI')
plt.ylabel('Var')
plt.title('All(10) Mean Var Histogram')
plt.show()

'''
#组图绘画

i = 7

plt.figure(figsize=(18,14))
ax1 = plt.subplot(321)
ax2 = plt.subplot(322)
ax3 = plt.subplot(312)
ax4 = plt.subplot(313)

srf9 = srfResults[i*9 : 9 + i*9]
#print(srf9)
srf9 = np.array(srf9)
piValue = vic.NDPI_comp(srf9[:,2],srf9[:,3],srf9[:,4],arf = 0.73)
viValue = vic.NDVI_comp(srf9[:,2],srf9[:,3])
giValue = vic.NDGI_comp(srf9[:,1],srf9[:,2],srf9[:,3],arf = 0.58)

#print(str(srf9[:,2]) +' ..|||.. '+  str(srf9[:,3]))
#print(viValue)

plt.sca(ax1)
plt.plot(range(9),piValue,'r',label = 'NDPI')
plt.plot(range(9),viValue,'g',label = 'NDVI')
plt.plot(range(9),giValue,'b',label = 'NDGI')
plt.grid()
plt.xlabel('Moisture Rank')
plt.ylabel('VI Value')
plt.title('VI Change With Moisture')
plt.legend()

plt.sca(ax2)
plt.bar(range(3), [np.var(piValue),np.var(giValue),np.var(viValue)],color='k')
plt.xticks(range(3),['NDPI','NDGI','NDVI'],rotation=45)
plt.grid()
plt.xlabel('VI')
plt.ylabel('Var')
plt.title('Var Histogram')

plt.sca(ax3)
for j in range(9):
    loc = i * 9 + j
    plt.plot(spectralWavelength,soilSpectrals[loc],label = 'wet' + str(j))
plt.xlabel('Wavelength')
plt.ylabel('Reflection')
plt.title('Soil spectral')
plt.legend()
plt.grid()

plt.sca(ax4)
for j in range(9):
    plt.plot(range(5),srf9[j],'o--',label = 'wet' + str(j))
plt.xticks(range(5),['Blue','Grenn','Red','NIR','SWIR'],rotation=45)
plt.xlabel('Wave')
plt.ylabel('SRF')
plt.title('Soil SRF')
plt.legend()
plt.grid()


plt.sca(ax3)
srfFunc = srInstance.getSRF()
srfFuncWaveLength = srInstance.getWavelength()
print(srfFuncWaveLength)
colorList = ['b','g','r','r','r']
for m in range(5):
    plt.plot(srfFuncWaveLength,srfFunc[:,m])

plt.show()
'''
    