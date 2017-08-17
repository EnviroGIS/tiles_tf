# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import scipy
import numpy as np
import os
import shutil

print ('Setting the network model options')
# Same network definition as before
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()
img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=25.)
img_aug.add_random_blur(sigma_max=3.)

network = input_data(shape=[None, 64, 64, 4],
                     data_preprocessing=img_prep,
                     data_augmentation=img_aug)
network = conv_2d(network, 64, 4, activation='relu')
network = max_pool_2d(network, 2)
network = conv_2d(network, 128, 4, activation='relu')
network = conv_2d(network, 128, 4, activation='relu')
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='relu')
network = dropout(network, 0.5)
network = fully_connected(network, 2, activation='softmax')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

print ('Loading the options. This may take a while...')

name = raw_input('Enter the model name: ')

model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='model/'+name+'/'+name+'.tfl.ckpt')
model.load('model/'+name+'/'+name+'.tfl')

print ('Model is loaded. Checking the data...')

os.makedirs('0')
os.makedirs('1')

for image in os.listdir('data'):
	# Load the image file
	img = scipy.ndimage.imread('data/'+image, mode="RGBA")

	# Scale it to 64x64
	img = scipy.misc.imresize(img, (64, 64), interp="bicubic").astype(np.float32, casting='unsafe')

	# Predict
	prediction = model.predict([img])
	# print (prediction)

	# Check the result.
	is_red = np.argmax(prediction[0]) == 1

	if is_red:
	    print(image, "There is a building!")
	    shutil.copy2('data/' + image, "1/" + image)
	else:
	    print(image, "There is not a building!")
	    shutil.copy2('data/' + image, "0/" + image)