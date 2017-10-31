"""
This code provide input of GUD algorithm to C# UI program.
Function:
    input: NDVI time seris array/txt file
    output: 1.Original NDVI time seris map
            2.mix NDVI time seris map
            3.Curve Fit NDVI time seris map
"""
import numpy as np
import matplotlib.pyplot as plt
import timeseris
import logsticFit

def getFirstMaxValue(line):
    valTemp = -1000
    for i in range(len(line)):
        if(line[i] <= valTemp):
            return(i - 1)
        else: 
            valTemp = line[i]
    return(-1)


def GUDcaculate(timeSeris):
    shape = np.shape(timeSeris)
    minusShape = list(shape)
    minusShape[-1] = minusShape[-1] - 1
    derivative = np.zeros(minusShape)
    derivative = timeSeris[1:] - timeSeris[:-1]
    derivative = (1 / max(abs(derivative))) * derivative
    derivative2 = derivative[1:] - derivative[:-1]
    derivative2 = (1 / max(abs(derivative2))) * derivative2
    derivative3 = derivative2[1:] - derivative2[:-1]
    derivative3 = (1 / max(abs(derivative3))) * derivative3
    GUD = getFirstMaxValue(derivative3)
    
    return [GUD,derivative,derivative2,derivative3]
    

def __drawTwo(GUD,derivative,derivative2,derivative3,orin,STEP):# 画出不同的原始曲线
    '''
    画出第一幅显示图像，其内容有:
        1、原始的拟合后的混合时序变化图
        2、一阶倒数
        3、二阶倒数
        4、三阶倒数
        5、返青期直线
    '''
    plt.figure()
    plt.title('Two picture')
    plt.xlabel('Day of year')
    plt.ylabel('NDVI')
    plt.plot(range(len(derivative)),derivative,'--',label='frist D')
    plt.plot(range(len(derivative2)),derivative2,'--',label='second D')
    plt.plot(range(len(derivative3)),derivative3,'-',lw = 2,label='third D')
    plt.axvline(GUD,ls = '--',lw = 3)
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(range(len(orin)),orin,'r-',lw = 2,label='orin')
    
    ax1.legend()
    ax2.legend(loc ='upper left')
    #ax2.legend()
    plt.savefig("drawTwo.png")
    plt.show()

def __drawOne(mixline,totalLine,STEP):# 画出不同的原始曲线
    '''
    画出第一幅显示图像，其内容有:
        1、几条原始时序变化图
        2、求和后的时序变化图
        3、拟合后的时序变化图
    '''
    x = np.arange(0,STEP,1)
    lineNums = mixline.shape[0]
    plt.figure()
    for i in range(lineNums - 1):
        plt.plot(x,mixline[i],'--',label='line:' + str(i))
    
    plt.plot(x,mixline[-1],'r',lw = 4,label='mix line')
    plt.plot(x,totalLine,'g', lw = 2,label='fit line')
    plt.savefig("drawOne.png")
    plt.title('One picture')
    plt.xlabel('Day of year')
    plt.ylabel('NDVI')
    plt.legend(loc ='upper left')
    plt.show()
    
def __read_txt(txt_path,STEP):
    '''
    输入原始NDVI时序数据，获得混合曲线
    '''
    array = np.arange(0,STEP,1)
    print(txt_path);
    return array

def __allOrinTimeseris(input_value, STEP, fa = [0.3,0.3,0.4]):
    '''
    输入原始NDVI参数，获得混合曲线
    '''
    onelines = np.zeros([input_value.shape[0],STEP])
    for index, parameters in enumerate(input_value):
        onelines[index] = timeseris.get_initial_line(
            parameters[0], \
            parameters[1], \
            parameters[2], \
            parameters[3], \
            parameters[4], \
            parameters[5], 
            STEP)
    '''
    判断fa
    '''
    mixline = 0
    for index, val in enumerate(fa):
        mixline = mixline + val * onelines[index]
    mixline = np.row_stack((onelines,mixline))
    
    return mixline

def main(input_value, fa = [0.3,0.3,0.4], txt_flag = False):
    STEP = 3660
    if txt_flag:
        input_value = __read_txt(input_value,STEP)
    mixline = __allOrinTimeseris(input_value,STEP) #获取到了输入各种参数后的混合光谱\
    regress_line_up,regress_line_down,totalLine = \
        logsticFit.curve_fit(mixline[-1]) #获取到了拟合后的像素
    __drawOne(mixline,totalLine,STEP) #画出第一条显示的图像
    
    [GUD,derivative,derivative2,derivative3] = GUDcaculate(totalLine)
    __drawTwo(GUD,derivative,derivative2,derivative3,totalLine,STEP)
    
    #return '3'

if __name__ == "__main__" :
    #print(timeseris.initialAParameter)
    a = [[10,-0.007,0.7,0.1,-27,0.009],[9,-0.007,0.7,0.1,-27,0.009],[11,-0.007,0.7,0.1,-27,0.009]]
    a = np.array(a)
    main(a)
    #main()