import numpy as np
import matplotlib.pyplot as plt


def draw_paper_line(p_line, color='r', title='map', x_label='x label', y_label='y label', label='label'):

    p_line = np.array(p_line)
    p_size = np.size(p_line)
    plt.plot(range(p_size), p_line, 'o--' + color, label=label)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid()
    plt.show()

    return


def draw_paper_two_lines(p_lines, title='map', x_label='x label', y_label='y label', label1='label1',\
                         label2='label1'):

    p_size = np.size(p_lines[0, :])
    plt.plot(range(p_size), p_lines[0, :], 'o--b', label=label1)
    plt.plot(range(p_size), p_lines[1, :], 'o--r', label=label2)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid()
    plt.show()

    return


'''
line = [115.1,	116.4,	117.5,	118.5,	119.4]
line = np.array(line) - line[0]
draw_paper_line(line, color='r', title='∆GUD change with fa', x_label='fa', y_label='∆GUD', label='change line')
'''

line1 = [117.5,	118.1,	118.8,	119.5,	120.4]
line2 = [117.5,	116.9,	116.2,	115.6,	115.2]
lines = [line1, line2]
lines = np.array(lines)
lines[0, :] = lines[0, :] - lines[0, 0]
lines[1, :] = lines[1, :] - lines[1, 0]
draw_paper_two_lines(lines, title='∆GUD change with NDVI min', x_label='NDVI min change', y_label='∆GUD',\
                label1="change A's NDVI min", label2="change B's NDVI min")
