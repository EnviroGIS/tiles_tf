import os
import shutil

# count number of tiles
def images_counter(dir_folder, folder):
	directory = dir_folder + str(folder)
	global cnt
	for image in os.listdir(directory):
		cnt = cnt + 1
	return cnt

#move tiles to two folders: for training dataset and for processing dataset
def file_mover(dir_folder, folder, training_num):
	directory = dir_folder + str(folder)
	global count
	for image in os.listdir(directory):
		if count <= training_num:
			shutil.copy2(directory + '/'+ image, "tr_data/" + str(folder) + '_' + image)
			print "File", image, "copied to the 'tr_data' directory"
			count = count + 1
		elif training_num < count <= (training_num * 2):
			shutil.copy2(directory + '/'+ image, "val_data/" + str(folder) + '_' + image)
			print "File", image, "copied to the 'val_data' directory"
			count = count + 1
		else:
			shutil.copy2(directory + '/'+ image, "data/" + str(folder) + '_' + image)
			print "File", image, "copied to the 'data' directory"
			count = count + 1

dir_folder = 'temp_19/19/' # folder for tiles created with QTiles
cnt = 0
count = 0

os.makedirs('tr_data') #folder for training data
os.makedirs('val_data') #folder for validation data
os.makedirs('data')

for folder in os.listdir(dir_folder):
	cnt =  images_counter(dir_folder, folder)

training_num = int(cnt / 3)
for folder in os.listdir(dir_folder):
	file_mover(dir_folder, folder, training_num)

#create a temp directory for placing there appropriate tiles
os.makedirs('tr_data/1')
os.makedirs('val_data/1')
print "Now you should move appropriate tiles to the folder '1' in 'val_data' & 'tr_data' folder\nRun the data_prep2.py after this"