import os
import shutil

# count number of tiles
def images_counter(folder):
	directory = "temp_18/18/" + str(folder)
	global cnt
	for image in os.listdir(directory):
		cnt = cnt + 1
	return cnt

#move tiles to two folders: for training dataset and for processing dataset
def file_mover(folder, training_num):
	directory = "temp_18/18/" + str(folder)
	global count
	for image in os.listdir(directory):
		if count <= training_num:
			shutil.copy2(directory + '/'+ image, "tr_data/" + str(folder) + '_' + image)
			print "File", image, "copied to the 'tr_data' directory"
			count = count + 1
		else:
			shutil.copy2(directory + '/'+ image, "data/" + str(folder) + '_' + image)
			print "File", image, "copied to the 'data' directory"
			count = count + 1

# write the dataset file (http://tflearn.org/data_utils/#image-preloader)
def datafile():
	for image in os.listdir('tr_data'):
		dataset_file.write('tr_data/' + image + ' 0\n')
	for image in os.listdir('tr_data/1'):
		#copy back to the main tr_data folder
		shutil.copy2('tr_data/1/' + image, "tr_data/" + image)
		dataset_file.write('tr_data/' + image + ' 1\n')


cnt = 0
count = 0
dataset_file = open('my_dataset.txt', 'w')
os.makedirs('tr_data')
os.makedirs('data')

for folder in os.listdir("temp_18/18"):
	cnt =  images_counter(folder)

training_num = int(cnt / 3)
for folder in os.listdir("temp_18/18"):
	file_mover(folder, training_num)

#create a temp directory for placing there appropriate tiles
os.makedirs('tr_data/1')
print "Now you should move appropriate tiles to the folder '1' in 'tr_data' folder"

while True:
	q = raw_input('Are we ready to continue? (y/n)')
	if q == 'y':
		datafile()
		break
	else:
		continue

shutil.rmtree('tr_data/1') #remove the directory

print "\n\n==============DONE==============\ndataset.txt is created\ndata strored in one folder 'tr_data'"