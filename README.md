# Presentation Video
![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/c65bb0d0-56f9-44d2-b217-c3d02c708d36)**[2023 Synopsys ARC AIoT](https://contest.synopsys.com.tw/2023ARC?utm_source=synopsys.com&utm_mediu)**

# Abstract
## Motivation
Many traditional factories are still using analog guages. However, to replace the new machine with digital readers will be large costs, and record or moniter guage data by human inspectors is a waste of time.
## Our Proposal

- Digtize the analog guage without replacing it
- Use ARC EM9D real-time monitor analog guage
- Reduce labor costs and enhanced management automation

![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/baca9e00-d55d-4dfd-9562-a1bcac825076)


# Challenge
**1. Dataset Collection**

- Collect and annotate a sufficient number of data
- Different gauge styles and appearances
- Influence of lighting and noise

![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/59da26dd-8346-4d3a-906c-0972cd3c68af)


**2. Model Sellection**

* Extraction and recognition of numbers -> Large-scale detection and Classification model
* Angle prediction for gauge pointer -> Regression or Multi-class Classification

**3. Computation and Storage Limitations**

* Compress the model to deploy on the device
* Maintain the model performance with limited model size

**4. Traditional Computer Vision Methods Are Sensitive**

* Variations in lighting, background clutter, particular types of guages

**5. Exist Dataset Lacks Realism**

* Inaccurate background representation
* Without considering image distortion
# Innovation
## Analog Guage Image Data Generator
- Gauge Images and Videos: Pressure Gauge Dataset(Source: Kaggle)
- Backgroud Images: Places Dataset-engine_room(Source: MIT)

![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/2826b7d0-2321-48f5-abd9-80aa4edc9dc0)


## Data Augmentation
**- Random Enhancement**
* Saturation
* Brightness
* Contrast
* Sharpness

**- Random Noise**
* Gaussian Noise

**- Random Blur**
* Gaussian Blur

    ![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/3d38acb8-abcd-4f5d-b2d6-84e40922e469)


## Fisheye Transform
![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/6f199919-4a2f-4aeb-9506-ef7c343cf254)


## Fisheye Transform to AoSTM VGA Camera

![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/9c4408a1-802b-4d14-872a-e030ab7d893d)




## Analog Guage Calibration
![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/a8762e4d-08d4-4578-993f-9ee86dab6dfe)




## Knowledge Distillation
### Compress Model Through Knowledge Distillation
- Matching prediction probability between teacher and student model

![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/72dc7a5d-0e05-4492-82c8-d6a4a4b86ae0)


# Design and Reliability 
## System Architecture

![](https://hackmd.io/_uploads/BkaKGIftn.png)

## Analog Gauge Reader
* **MobileNet V2**

    ![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/28b6d6ca-a15c-46a3-b663-d2812ebdcc4c)


## Post-Training Quantization
![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/9e272037-6bd2-4d76-afbe-3d33b606655b)



# Hardware and Software setup
## Software version
    python=3.8.0
    tensorflow=2.5.0
## Hardware specification
    GPU: NVIDIA GeForce GTX 2080 Ti
## Create Enviroment
    conda create -n 2023ARC python=3.8

## Activate Enviroment
    conda activate 2023ARC

## Packages Installation
    conda install jupyter notebook
    pip install tensorflow-gpu==2.5.0
    conda install numpy==1.23.4
    conda install matplotlib
    conda install pandas
    conda install -c anaconda scikit-learn
    conda install -c conda-forge keras
    pip install opencv-python
    pip install tqdm

# User-Manual
Connect ARC EM9D AIoT DK with Wemos D1 R32

    UART0 RX header connect to GPIO16
    UART0 TX header connect to GPIO17
    GND to GND
# Demo Video
* Demo 1: https://www.youtube.com/watch?v=Uo0q9bvPye8
* Demo 2: https://www.youtube.com/watch?v=cPMuLgIlY1I
* Demo 3: https://www.youtube.com/watch?v=dGtSQWrOaJU
* Demo 4: https://www.youtube.com/watch?v=Z6F6YlwSd7A
* Demo 5: https://www.youtube.com/watch?v=5TH9fBItiWc


# Overall Summary
## Real-time Analog Gauge Reader
**1. Data Generator Generate**
* Automatically generates and labels images to create a training dataset
* Suitable for the real-world scenario

**2. Analog Gauge Calibration**
* Decide the number of categories
* Trade-offs between model size and accuracy

**3. Model Compression**
* Reduce the size of MobileNetV2
* Using int8 quantization to compress the model size

**4. UI for Recording and Displaying Analog Gauge**
![image](https://github.com/KW-Baker/2023_Synopsys_ARC_AIoT_OASIS_Titan/assets/96005167/b7672a5d-e60b-4b06-ac14-634021d6507e)

