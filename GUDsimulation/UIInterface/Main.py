"""
This code provide input of GUD algorithm to C# UI program.
Function:
    input: NDVI time seris array/txt file
    output: 1.Original NDVI time seris map
            2.mix NDVI time seris map
            3.Curve Fit NDVI time seris map
"""
import numpy as np

def read_txt(txt_path):
    array = np.arange(0,366,1)
    return array

def main(input, txt_flag = False):
    if txt_flag:
        arrays = read_txt(input)
    else:
        for index,val in enumerate(input):

    return('3')


def getLogisticLin(a,b,c,d,time = 366):
    time = np.arange(0,time,1)
    expValue = np.exp(a + b*time)
    timeseris = c/(1 + expValue) + d
    return(timeseris)