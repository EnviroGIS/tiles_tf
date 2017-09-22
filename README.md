# tiles_tf
TensorFlow neural network for processing Raster Tiles.

![](https://i2.wp.com/cdn-images-1.medium.com/max/600/1*wUZiI2Mg2cncuMWWXIiBgQ.png?zoom=1.5&w=697&ssl=1)

## CURRENTLY WORKS WITH 2 CATEGORIES

## Installation

1. Clone the [repository](https://github.com/EnviroGIS/tiles_tf.git)
2. Go to `tiles_tf\tf_env\Scripts>activate.bat` for activating Virtual Environment with all needed dependencies.

## Usage

1. QGIS. The [code](https://github.com/EnviroGIS/tiles_tf/tree/master/qgis_scripts/raster_clipper.py) provided proposes you to create a vector grid any size you like. You may also use you own vector layer. This code HAS TO BE EXTREMELY UPGRADED. After creating the grid (or upload your own vector layer) you have to categorize vectors giving objects appropriate attributes. Then, the raster will be clipped with this vector. 

2. There are 3 datasets created: `tr` for training data, `val` for validation data and `raw` for testing the neural network (actually there is that sort of data that has to be processed).

There are also metafiles created (required in [TensorFlow Documentation](http://tflearn.org/data_utils/#image-preloader)).

3. Run `python3 learn.py` for training the neural network. You will be asked for the name of your neural network. There are `50` iterations by default. It could be changed in code in line 93. It is recommended to have at least 3o iteractions. _Has to be verified_. Change `batch_size` in line 91 to the number your images number could be divided (_recommended near 3% of the total number_). 

#### TAKES TIME TO PROCEED. You will see the accuracy of the neural network during the process. Once the neural network is ready you can use it with any similar dataset, so it is preferable to spend time and efforts to make the model as good, nice and shiny as it is possible.

4. Run `python3 check.py` for checking data from dataset stored in `tiles\raw` folder to be categorized. Images would be copied to folders `0` and `1` and appropriate metafile is created.

5. The metafile created could be joined with the grid layer created using the key field.

![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/vector.png)

# Things to do

1. Custom categories number

2. Read theory to make it more efficient.

3. Visualize the neural network

Some information to inspire:
* [CNN is FUN (in Russian)](https://algotravelling.com/ru/%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B5-%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%8D%D1%82%D0%BE-%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D0%BE-3/)
* [Some scientific stuff](https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLII-1-W1/653/2017/isprs-archives-XLII-1-W1-653-2017.pdf)
* [CityClass Project (in Russian)](https://medium.com/@romankuchukov/cityclass-project-37a9ebaa1df7)
* [Buildings in Nigeria](http://gbdxstories.digitalglobe.com/building-detection/) with [github page](https://github.com/PlatformStories/train-cnn-classifier)
* [Collecting Urban Data](http://pulse.media.mit.edu/) and [results](http://streetscore.media.mit.edu/citymap.html?city=NYC)

# RESULTS

Idea: define tiles with artificial objects (buildings primarily).

Input: cellsize - 100m, Bing Imagery, 710 training images, 362 validation images, `batch_size = 30`, `n_epoch = 50`.

Samples:
Trained category = 1
![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/tr_1.png)

Trained category = 0
![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/tr_0.png)

## After training and checking

Checked category = 1 (All the images categorized as 1 were categorized correctly (not the same with category 0. There are some tiles with buildings). General accuracy up to 95% (After 5 iteraction it was 85%))
![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/ch_1.png)
