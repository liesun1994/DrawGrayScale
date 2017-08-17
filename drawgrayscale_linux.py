# -*- coding: utf-8 -*-
import numpy as np
import argparse
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from matplotlib.font_manager import *

myfont = FontProperties(fname='/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf')

logger = logging.getLogger(__name__)

class DrawGrayScale(object):
    def __init__(self, x, y, align, imgpath):
        self.x=x
        self.y=y
        self.align=align
        self.imgpath=imgpath

    def split_align_data(self,data):
        splited_data=[]
        for now_data in data: 
            splited_now_data = now_data.strip().split(' ')
            splited_now = []
            for n_data in splited_now_data:
                splited_now.append(float(n_data))
            splited_data.append(splited_now)
        return splited_data

    def split_src_trg_data(self,data):
        splited_data=[]
        for now_data in data: 
            splited_now_data = now_data.strip().split(' ')
            splited_data.append(splited_now_data)
        return splited_data

    def autofill_data(self, data, number):
        for t in range(number):
            data.append('<s>')
        return data

    def parse_data(self):
        x_obj = open(self.x)
        y_obj = open(self.y)
        align_obj = open(self.align)
        x_txt = x_obj.readlines()
        y_txt = y_obj.readlines()
        align_txt = align_obj.readlines()
        x_splited = self.split_src_trg_data(x_txt)
        y_splited = self.split_src_trg_data(y_txt)
        align_splited = self.split_align_data(align_txt)
        align_obj.close()
        x_obj.close()
        y_obj.close()
        # judge data
        if len(x_splited) > 1:
            logger.error('x data multi_lines.')
        elif len(y_splited) > 1:
            logger.error('y data multi_lines.')

        x_size = len(x_splited[0])
        y_size = len(y_splited[0])
        align_x_size = len(align_splited[0])
        align_y_size = len(align_splited)
        minus_x = align_x_size - x_size
        minus_y = align_y_size - y_size
        auto_x = self.autofill_data(x_splited[0], minus_x)
        auto_y = self.autofill_data(y_splited[0], minus_y)

        return auto_x, auto_y, align_splited
         
    def draw(self):
        # added for chinese symbols 
        x_parsed, y_parsed, align_parsed = self.parse_data()
        # plt.rcParams['font.sans-serif']=['simhei']
		# clear figure 
        plt.clf()
        f = plt.figure()
        ax = f.add_subplot(1, 1, 1)
        activation_map = np.asarray(align_parsed)
        # add image
        ax.imshow(activation_map, interpolation='nearest', cmap='gray', aspect='equal')

        ax.set_xticks(range(len(x_parsed)))
        x_parsed_new = []
        for x in x_parsed:
            x = unicode(x, "utf-8")
            x_parsed_new.append(x)
        ax.set_xticklabels(x_parsed_new, rotation=90, fontproperties=myfont)
        ax.set_xlabel("input sequence")

        ax.set_yticks(range(len(y_parsed)))
        y_parsed_new = []
        for y in y_parsed:
            y = unicode(y, "utf-8")
            y_parsed_new.append(y)
        ax.set_yticklabels(y_parsed_new, fontproperties=myfont)
        ax.set_ylabel("output sequence")
        # set x&y axis props
        for tick in ax.yaxis.get_major_ticks():
            tick.label1On = True
            tick.tick1On=False
            tick.tick2On=False
        for tick in ax.xaxis.get_major_ticks():
            tick.tick2On = False 
            tick.tick1On = False
            tick.label1On = True
            tick.label2On = False

        ax.grid(False)
        f.tight_layout()
        f.savefig(self.imgpath+'.pdf', bbox_inches='tight')
        # print('Successfully draw a picture.') # python 3.* 
        print 'Successfully draw a picture.'
        #f.show()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ch', type=str)
    parser.add_argument('en', type=str)
    parser.add_argument('align', type=str)
    parser.add_argument('imgpath', type=str)
    args = parser.parse_args()
    draw_obj = DrawGrayScale(x=args.ch, y=args.en, align=args.align, imgpath=args.imgpath)
    draw_obj.draw()
