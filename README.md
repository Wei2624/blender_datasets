# Dataset Generator in Blender

In this repo, I post the source code for generating 3D simulation data using Blender. Several factors are randomized for the generation such as position, texture, dimension, orientation and lights. It can generate 10,000 samples in an hour. 

## How To Run

`generator.py` is the funciton to generate the data samples. To run it, you should have Blender open and run from there. 

## Preliminary Scene Setup

You should have a camera, five planes and three lights in the scene before you run the generator script.  

## Folders

`/cfgs` folder contains all the config parameters that are used in the generation process. You should read 'test_config.py' to get a sense of what might be changed. 

`\lib` folder contains the functions necessary to run the generator. 

## Note

`sample_generator.py` and `sample_generator_draft.py` are deprecated. 


I am still cleaning the code. 
