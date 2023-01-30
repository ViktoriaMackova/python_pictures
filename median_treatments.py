# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 17:20:55 2023

@author: vikto
"""

import glob
import czifile
import numpy as np
import matplotlib.pyplot as plt
import skimage
from collections import defaultdict

folder = r'C:\Users\vikto\Documents\Python\spracovanie_obrazu\data'
all_dict = defaultdict(list)
filenames = glob.glob(folder + '/**/*.czi')


for filename in filenames:
    text = filename.split('_')
    treat = text[-4]
    all_dict[treat].append(filename)
    
    
def test(all_dict, channel=int, mask=int):
    mean_dict = defaultdict(list)
    treats = list(all_dict.keys())
    for key in all_dict:
        for el in all_dict[key]:
            temp = czifile.imread(el)
            mean = ready_mean(temp, channel, mask)
            mean_dict[key].append(mean)
    return dict(mean_dict)

def ready_mean(img, channel:int, mask:int):
    img = np.squeeze(img)
    chan = img[channel,:,:]
    mask = chan>mask
    med_im = skimage.filters.median(mask, footprint=np.ones((3,3)))
    med_list = chan[med_im]
    return np.mean(med_list, axis=0)

def show_im(img): # vstupi image s maskou
    plt.figure(figsize=(15,15))
    plt.imshow(img) # cmap='hot',green, blue?
    plt.show()
            

def plot(my_dict: dict, title: str) :
    labels, data = [*zip(*my_dict.items())] # 'transpose' items to parallel key, value lists
    plt.title(title)                
    plt.boxplot(data)
    plt.xticks(range(1, len(labels) + 1), labels)
    plt.savefig('{title}_graf.png'.format(title = title))
    plt.show()

testing = test(all_dict, 0, 550) 
plot(testing,'red')