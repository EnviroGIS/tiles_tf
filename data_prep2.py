import os
import shutil


# write the dataset file (http://tflearn.org/data_utils/#image-preloader)
def datafile():
	for image in os.listdir('tr_data'):
		dataset_file.write('tr_data/' + image + ' 0\n')
	for image in os.listdir('tr_data/1'):
		#copy back to the main tr_data folder
		shutil.copy2('tr_data/1/' + image, "tr_data/" + image)
		dataset_file.write('tr_data/' + image + ' 1\n')
	for image in os.listdir('val_data'):
		validation_file.write('val_data/' + image + ' 0\n')
	for image in os.listdir('val_data/1'):
		#copy back to the main val_data folder
		shutil.copy2('val_data/1/' + image, "val_data/" + image)
		validation_file.write('val_data/' + image + ' 1\n')

dataset_file = open('my_dataset.txt', 'w')
validation_file = open('validation.txt', 'w')

datafile()

shutil.rmtree('tr_data/1') #remove the directory
shutil.rmtree('val_data/1')

print "\n\n==============DONE==============\ndataset.txt and validation.txt are created\ndata strored in folders 'tr_data' and 'val_data'"