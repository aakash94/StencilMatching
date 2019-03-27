# StencilMatching
match/classify images based on shared static components. 

## Background :
For this scheme it is assumed that all images that are from the same class, have some components that change across various instances of the class a.k.a dynamic components, and some that do not change a.k.a static components. 
Components can be defined by pixels and their specific location. 

(Note : This scheme is not intended for cases where images from the same class have no static component.
Eg: Images of dogs. We cannot expect certain pixels to appear at certain fixed places in the dog images.


## Scheme :
We define a stencil for a set of images. A stencil is a normal image with added alpha channel to express transparency.  
All the pixels (for a given location) that are constant across all the images in a set are put on the stencil. The stencil remains transparent at all the places that do not share same pixels for a given location. 
Thus we get an image (stencil) which has all the components that will stay the same across all the images of the same class.
Now for a new given image if the stencil when overlaid  on it does not produce any visible difference, we may conclude that the new image is from the class that the stencil is from. 
Note : All Stencil and images are of the same height and width.

## Application :
For applications, stencils may be created manually, or in an incremental manner where we modify the existing stencil (maybe copy of the first image to start with, but with 4 channels) in order to accommodate the newer images.
In theory a significantly large image set could eventually remove almost all of the dynamic components from a stencil.
It is also a good idea to create stencils out of similar set of images. In theory a stencil created out of an image and its negative would result in an empty stencil. 

## Optimizations : 
There are several optimizations that can improve the performance of this scheme.
#### Removing Color Information :
The key idea is create stencils out of black and white images. This makes the stencils color agnostic. Which may improve computational performance in some cases and make the scheme more robust. However, it comes with the added cost of preprocessing the input image. (Converting into black and white)
Note: Different ways of obtaining a black and white image only increase the reusability of a stencil. Thus leading to better generalization in some sense.
#### Faster Processing : 
On larger images it may be possible to get some performance improvement by simply copying the non transparent memory values from the stencils and overwriting the memory of a copy image. Then the data stored the memory of the overwritten copied image and the  original image can be compared to draw conclusions

