# Video Clustering

This application allows a user to remove moving objects from an "image".
Given a video taken by a still camera, the program will generate an image
with infrequent elements removed from the image. For instance, given a
clip of a man running through the field, it will ideally remove the man
from the field.

## About

The program performs its operation by searching for the most common pixel
value for a given pixel across all frames. This is done using K-means
clustering in the given implementation, although other clustering algorithms
would also work in its place. The operation is applied across each pixel
in order to generate an output image.

## Dependencies

The program utilizes a shell script that splits a given clip into frames.
This operation requires that ```ffmpeg``` be installed. Using a package
manager, this can be done with one of these methods:

```
# Apt-Get
sudo apt-get install ffmpeg

# Homebrew
brew install ffmpeg

# Pacman
sudo pacman -S ffmpeg
```

The program also relies on the use of ```python```, which can be similarly
installed. Finally, the program requires Numpy, which is used in the
computation of the clusters. This can be done using pip like so:

```
pip install numpy
```

## Usage
To run the program, simply run

```sh filter.sh <src> <dst (default='./output.png')>```

