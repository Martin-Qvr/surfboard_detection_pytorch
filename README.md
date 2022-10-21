## Surfboard and surfer's detection 

In this repo I perform object detection (of surfboards :)) with pre-trained networks using PyTorch. I had this idea watching the work of [my-sessions.com](https://www.my-sessions.com/) which performs face recognition on surf photos. This is "the first part" of the pipeline. 

## installation and run

To install the required package run ``` $ pip install -r requirements.txt ```.

To detect on your images run ``` $ python detect_image.py -i  {your_image_path} ```.

Arguments :
- ``` -i --image``` : path to the input image (required)
- ``` -m --model``` : model chose between (frcnn-resnet, frcnn-mobilenet, retinanet) respectively (slow, fast, balanced) 


## Inputs: 
![example_01.jpg : input image](https://github.com/[Martin-Qvr]/[surfboard_detection_pytorch]/blob/[main]/code/images/example_O1.jpg?raw=true)

## Outputs: 

![Output image](https://github.com/[Martin-Qvr]/[surfboard_detection_pytorch]/blob/[main]/code/output/example_O1_output.jpg?raw=true)


Source : 

I used [this repo](https://pyimagesearch.com/2021/08/02/pytorch-object-detection-with-pre-trained-networks/) as an inspiration to construct my own detector. 

