import os
import json
import sys


def __main__():
	if len(sys.argv) < 1:
		print("Usage: check_completed.py dataset_name")
	else:
		dataset_name = sys.argv[1]
		with open('labels/'+dataset_name+'.json', 'r') as f:
			labels = json.load(f)

		labeled_files = len(labels)

		images = os.listdir(dataset_name)
		images = len([im for im in images if '.json' in im])

		if images == labeled_files:
			print("Thank you! All the images have been labeled.")
		else:
			print("Some images have not been labeled. Please label all the images.")

if __main__:
	__main__()
