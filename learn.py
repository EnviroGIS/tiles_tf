# -*- coding: utf-8 -*-

"""
Based on the tflearn example located here:
https://github.com/tflearn/tflearn/blob/master/examples/images/convnet_cifar10.py
"""
from __future__ import division, print_function, absolute_import

# Import tflearn and some helpers
import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation

print ('TensorFlow imported')

#define metafiles
dataset_file = 'tr_dataset.txt'
validation_file = 'val_dataset.txt'

# Load the data set
from tflearn.data_utils import image_preloader
X, Y = image_preloader(dataset_file, image_shape=(64, 64),   mode='file', categorical_labels=True,   normalize=True)
X_test, Y_test = image_preloader(validation_file, image_shape=(64, 64),   mode='file', categorical_labels=True,   normalize=True)

# Shuffle the data
X, Y = shuffle(X, Y)

print ('Everything is imported. [X Y] shuffled (I have no idea why)\nPreparing the model...')

# Make sure the data is normalized
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()

# Create extra synthetic training data by flipping, rotating and blurring the
# images on our data set.
img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=25.)
img_aug.add_random_blur(sigma_max=3.)

# Define our network architecture:
print ('Defining network architecture')
# Input is a 64x64 image with 4 channels (RGBA)
network = input_data(shape=[None, 64, 64, 4],
                     data_preprocessing=img_prep,
                     data_augmentation=img_aug)

# Step 1: Convolution
network = conv_2d(network, 64, 4, activation='relu')
print ('Step 1. Convolution 1 Done')
# Step 2: Max pooling
network = max_pool_2d(network, 2)
print ('Step 2. Max Pooling is Done 1')
# Step 3: Convolution again
network = conv_2d(network, 128, 4, activation='relu')
print ('Step 3. Convolution 2 is Done')
# Step 4: Convolution yet again
network = conv_2d(network, 128, 4, activation='relu')
print ('Step 4. Convolution 3 is Done')
# Step 5: Max pooling again
network = max_pool_2d(network, 2)
print ('Step 5. Max Pooling 2 is Done')
# Step 6: Fully-connected 512 node neural network
network = fully_connected(network, 512, activation='relu')
print ('Fully-connected 512 node neural network is Done')
# Step 7: Dropout - throw away some data randomly during training to prevent over-fitting
network = dropout(network, 0.5)
print ('Dropout is Done')
# Step 8: Fully-connected neural network with two outputs (0=isn't a bird, 1=is a bird) to make the final prediction
network = fully_connected(network, 2, activation='softmax')
print ('Fully-connected neural network with two outputs is Done')

# Tell tflearn how we want to train the network
print ('\n\nNetwork architecture is set')
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

name = input('Enter the model name: ')
# Wrap the network in a model object
print ('Wrapping the network')
model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='model/'+name+'/'+name+'.tfl.ckpt')

# Train it! We'll do 100 training passes and monitor it as it goes.
print ('\n\nWe are ready to train the network')
model.fit(X, Y, n_epoch=50, shuffle=True, validation_set=(X_test, Y_test),
          show_metric=True, batch_size=30,
          snapshot_epoch=True,
          run_id=name)

os.makedirs('model/' + name)
# Save model when training is complete to a file
model.save('model/'+name+'/'+name+'.tfl')
print('Network trained and saved as '+name+'.tfl!')