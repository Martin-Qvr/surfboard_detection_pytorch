# import the necessary packages
from torchvision.models import detection
import os
import numpy as np
import argparse
import pickle
import torch
import cv2




# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path to the input image")
ap.add_argument("-m", "--model", type=str, default="frcnn-mobilenet",
	choices=["frcnn-resnet", "frcnn-mobilenet", "retinanet"],
	help="name of the object detection model")
ap.add_argument("-l", "--labels", type=str, default="coco_classes.pickle",
	help="path to file containing list of categories in COCO dataset")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# set the device we will be using to run the model, I only have CPU so we'll be patient. 

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# assign the list of categories in the COCO dataset and then generate a
# set of bounding box colors for each class

with open('coco_classes.txt', 'r') as f:
    CLASSES = [line.strip() for line in f]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# initialize a dictionary containing model name and its corresponding 
# torchvision function call
MODELS = {
	"frcnn-resnet": detection.fasterrcnn_resnet50_fpn,
	"frcnn-mobilenet": detection.fasterrcnn_mobilenet_v3_large_320_fpn,
	"retinanet": detection.retinanet_resnet50_fpn
}
# load the model and set it to evaluation mode
model = MODELS[args["model"]](pretrained=True, progress=True,
	num_classes=len(CLASSES), pretrained_backbone=True).to(DEVICE)
model.eval()

# load the image from disk
image = cv2.imread(args["image"])
orig = image.copy()
# convert the image from BGR to RGB channel ordering and change the
# image from channels last to channels first ordering
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = image.transpose((2, 0, 1))
# add the batch dimension, scale the raw pixel intensities to the
# range [0, 1], and convert the image to a floating point tensor
image = np.expand_dims(image, axis=0)
image = image / 255.0
image = torch.FloatTensor(image)
# send the input to the device and pass the it through the network to
# get the detections and predictions
image = image.to(DEVICE)
detections = model(image)[0]

# loop over the detections
for i in range(0, len(detections["boxes"])):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections["scores"][i]
	# filter out weak detections by ensuring the confidence is
	# greater than the minimum confidence
	if confidence > args["confidence"]:
		# extract the index of the class label from the detections,
		# then compute the (x, y)-coordinates of the bounding box
		# for the object
		idx = int(detections["labels"][i]) - 1 ## Need to put the -1 because the text is indexed from 1 onwards
		box = detections["boxes"][i].detach().cpu().numpy()
		(startX, startY, endX, endY) = box.astype("int")
		# display the prediction to our terminal
		label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
		print("[INFO] {}".format(label))
		# draw the bounding box and label on the image
		cv2.rectangle(orig, (startX, startY), (endX, endY),
			COLORS[idx], 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(orig, label, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
# show the output image
cv2.imwrite(f'./output/{args["image"].split("/")[1][:-4]}_output.jpg', orig) 
