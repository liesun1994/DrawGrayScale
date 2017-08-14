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
    def __init__(self, ch, en, align, imgpath):
        self.ch=ch
        self.en=en 
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

    def parse_data(self):
        ch_obj = open(self.ch)
        en_obj = open(self.en)
        align_obj = open(self.align)
        ch_txt = ch_obj.readlines()
        en_txt = en_obj.readlines()
        align_txt = align_obj.readlines()
        ch_splited = self.split_src_trg_data(ch_txt)
        en_splited = self.split_src_trg_data(en_txt)
        align_splited = self.split_align_data(align_txt)
        align_obj.close()
        en_obj.close()
        ch_obj.close()

        # judge data 
        step = 0
        for align_now in align_splited:
            if len(en_splited[0]) != len(align_now):
                logger.error('align line'+ step + ' wrong.')

        if len(ch_splited[0]) != len(align_splited) :
            logger.error('chinese data wrong.')
        elif len(en_splited[0]) != len(align_splited[0]):
            logger.error('english data wrong.')
        if len(ch_splited) > 1: 
            logger.error('chinese data multi_lines.')
        elif len(en_splited) > 1:
            logger.error('english data multi_lines.')
        
        return ch_splited[0], en_splited[0], align_splited
         
    def draw(self):
        # added for chinese symbols 
        ch_parsed, en_parsed, align_parsed = self.parse_data()
        # plt.rcParams['font.sans-serif']=['simhei']
		# clear figure 
        plt.clf()
        f = plt.figure()
        ax = f.add_subplot(1, 1, 1)
        activation_map = np.asarray(align_parsed)
        # add image
        i = ax.imshow(activation_map, interpolation='nearest', cmap='gray', aspect='equal')
        ax.set_yticks(range(len(ch_parsed)))
        ch_parsed_new =[]
        for ch in ch_parsed:
            ch = unicode(ch, "utf-8")
            ch_parsed_new.append(ch)
        ax.set_yticklabels(ch_parsed_new, fontsize=14, fontproperties=myfont)
        ax.set_xticks(range(len(en_parsed)))
        ax.set_xticklabels(en_parsed, rotation=90, fontsize=14, fontproperties=myfont)
        # set x&y axis props
        for tick in ax.yaxis.get_major_ticks():
            tick.label1On = True
            tick.tick1On=False
            tick.tick2On=False
        for tick in ax.xaxis.get_major_ticks():
            tick.tick2On = False 
            tick.tick1On = False
            tick.label1On = False 
            tick.label2On = True
        
        ax.grid(False)
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
    draw_obj = DrawGrayScale(ch=args.ch, en=args.en, align=args.align, imgpath=args.imgpath)
    draw_obj.draw()
