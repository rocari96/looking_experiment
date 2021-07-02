# Looking or not human performance experiment.

## Getting started

To be able to run the code, you first need to open a terminal window and navigate to a directory where you want to clone this repository.

Then clone the repository:

```
git clone https://github.com/rocari96/looking_experiment.git
```


Navigate to the **looking_experiment** folder: 

```
cd looking_experiment
```

Create a virtual environment using:

```
python3 -m venv looking_env
```

Then activate the environment:

```
source looking_env/bin/activate
```

Note: To deactivate the environment, use:

```
deactivate
```

Install the librairies using:

```
pip install -r requirements.txt
```

## Chosing a dataset

We run this experiment on multiple datasets, please select one dataset that is **uncomplete** and please write your firstname on the corresponding row of the following spreadsheet. https://docs.google.com/spreadsheets/d/1QUayKcOI0bqS5Dc5P2gvrjBFxdZIqXJ4GrpVB_vPbHo/edit?usp=sharing

You can use the **link** column to download the zip file that contains the dataset you will label.
Then unzip it in the **looking_experiment** folder.

The datasets are either images (full body, head or eye crops), keypoints (full body, body or head) or a combination of image and keypoints.


## Run the program

To run the program, use
```
python main.py
```

In the User-Interface:

Go to File -> Open, then choose the dataset's folder you extracted.
It will show the first instance that you have to label.


## Task

You need to guess if the person is looking or not at our camera from the image you see on screen.
There are three possible labels:
- **looking**: the person is looking at us.
- **not looking**: the person is not looking at us.
- **don't know**: it is impossible to say from what we see.

There are shortcuts you can use to label the images quicker:
- **i**: labels the image as **looking** and goes to next image.
- **o**: labels the image as **not looking** and goes to next image.
- **p**: labels the image as **don't know** and goes to next image.

You can also navigate between the images.
- **a**: goes to previous image.
- **d**: goes to next image.

You have to label all the images at once for the result to be saved. 
When you are done with the task, a message will pop on the screen telling you that all images have been labelled.
It will save the output with your annotations.
You can then quit the program.

To double check that all images have been labeled, please run:
```
python check_completed dataset_name.py
```


## Output

Once all the images have been labeled, a json file will be saved in the **labels** folder in the format **dataset_name.json**.
Please copy and paste this json file to the [following location](https://drive.google.com/drive/folders/1GjnfDoC3mYXpVfzL2n9vZySOnSJvXoiQ?usp=sharing) and change the status of the dataset in the [spreadsheet](https://docs.google.com/spreadsheets/d/1QUayKcOI0bqS5Dc5P2gvrjBFxdZIqXJ4GrpVB_vPbHo/edit?usp=sharing) to **completed**.


Thank you for your help. 
If you have any question, you can send them to romain.caristan@epfl.ch

