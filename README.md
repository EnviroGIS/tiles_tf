# tiles_tf
TensorFlow neural network for processing Raster Tiles.

![](https://i2.wp.com/cdn-images-1.medium.com/max/600/1*wUZiI2Mg2cncuMWWXIiBgQ.png?zoom=1.5&w=697&ssl=1)

## CURRENTLY WORKS WITH 2 CATEGORIES

## Installation

1. Clone the [repository](https://github.com/EnviroGIS/tiles_tf.git)
2. Go to `tiles_tf\tf_env\Scripts>activate.bat` for activating Virtual Environment with all needed dependencies.

## Usage

1. [data_prep.py]() is the code for preparing data to be categorized by expert(s). Edit the code in line 30

> dir_folder = 'temp_19/19/' # folder for tiles created with QTiles

replacing by your tiles folder.
Use `python data_prep.py` for running the code.

2. There are 3 datasets created: `tr_data` for training data, `val_data` for validation data and `data` for testing the neural network (actually there is that sort of data that has to be processed). Now you have to cut categorized images from `tr_data` and `val_data` to the folder `1` inside. Run [data_prep2.py]() after this.

After running the code you will get the metafiles required in [TensorFlow Documentation](http://tflearn.org/data_utils/#image-preloader).

3. Run `python3 learn.py` for training the neural network. You will be asked for the name of your neural network. There are `50` iterations by default. It could be changed in code in line 91. It is recommended to have at least 3o iteractions. _has to be verified_. Change `batch_size` in line 91 to the number your images number could be divided (_recommended near 3% of the total number_). 

#### TAKES TIME TO PROCEED. You will see the accuracy of the neural network during the process. Once the neural network is ready you can use it with any similar dataset, so it is preferable to spend time and efforts to make the model as good, nice and shiny as it is possible.

4. Run `python3 check.py` for checking data from dataset stored in `data` folder to be categorized. Images would be copied to folders `0` and `1`.

### CONGRATULATIONS! You have just tested #TilesBasedNeuralNetwork.


# Things to do

1. Georeferencing data

2. Custom categories number

3. Read theory to make it more efficient.

4. Visualize the neural network

Some information to inspire:
* [CNN is FUN (in Russian)](https://algotravelling.com/ru/%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B5-%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%8D%D1%82%D0%BE-%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D0%BE-3/)
* [Some scientific stuff](https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLII-1-W1/653/2017/isprs-archives-XLII-1-W1-653-2017.pdf)
* [CityClass Project (in Russian)](https://medium.com/@romankuchukov/cityclass-project-37a9ebaa1df7)

# RESULTS

Idea: define tiles with artificial objects (buildings primarily).

Input: zoom 19, Bing Imagery, 1120 training images, 1120 validation images, `batch_size = 40`, `n_epoch = 30`.

Samples:
Trained category = 1
![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/train%3D1.png)

Trained category = 0
![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/train%3D0.png)

## After training and checking

Checked category = 1 (first 9 images. All the images categorized as 1 were categorized correctly (not the same with category 0. There are some tiles with buildings). General accuracy up to 93% (After 5 iteraction it was 87%))
![](https://github.com/EnviroGIS/tiles_tf/blob/master/img/check%3D1.png)

Model named `build_30` is already created. You could check it with your data.

