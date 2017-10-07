import dbscan, kmeans
import os, sys, fnmatch
import numpy as np

import argparse

from PIL import Image

# Command line arguments
parser = argparse.ArgumentParser(
        description="Generates a picture by removing distractions from a video")

parser.add_argument('-a', '--algo',
        default='dbscan',
        dest='algo',
        help='nlustering algo to use',
        choices=['dbscan', 'kmeans'])

parser.add_argument('-c', '--clusters',
        default=4, dest='clusters',
        help='number of clusters to use if necessary')

parser.add_argument('-i', '--input',
        dest='input', 
        help='the video to use', 
        required=True)

parser.add_argument('-n', '--neighbors',
        default=4,
        dest='neighbors',
        help='number of neighbors to use if necessary')

parser.add_argument('-o', '--output',
        default=None,
        dest='output',
        help='the file to save the image to')

parser.add_argument('-r', '--radius',
        default=4,
        dest='radius',
        help='neighbor radius to check with if necessary')

# Parse arguments.
params = parser.parse_args()

workdir = './.frames_' + os.path.splitext(os.path.basename(params.input))[0]

if params.output is None:
    # Use input file as name for output file
    params.output = './' + os.path.splitext(os.path.basename(params.input))[0] + '.png'

#print('Preparing files in', workdir)
print('Preparing', params.input, 'for processing')

# Make a workspace
if not os.path.exists(workdir):
    # Generate a directory
    os.mkdir(workdir)

    # Generate the frames
    n = os.system("ffmpeg -i " + params.input + ' ' + workdir + '/frame%d.png > /dev/null 2>&1')

    if n != 0:
        # Error if frame extraction fails
        print(sys.argv[0] + ': could not properly extract frames')

        # Attempt to remove the directory
        os.rmdir(workdir)

        exit(1)

# Get the PNG files from the frames directory
frames = np.array([
    np.asarray(Image.open(os.path.join(workdir, f)))
    for f in os.listdir(workdir)
])


# Cleanup the directory
for f in os.listdir(workdir):
    os.remove(os.path.join(workdir, f))

# Remove the working directory
os.rmdir(workdir)

num_frames = frames.shape[0]
print("Extracted", num_frames, "frames from", frames.shape[2], "by", frames.shape[1], "video")

print('\nThe following settings will be used:')
print('algo:', params.algo)

res = None
if params.algo == 'dbscan':
    # Information about DBSCAN parameters.
    print('epsilon:', params.radius)
    print('min neighbors:', params.neighbors)
    print()

    # Perform the clustering
    res = dbscan.fix_photo(frames, eps=params.radius, minPts=params.neighbors)

elif params.algo == 'kmeans':
    # Information about K-means parameters
    print('clusters:', params.clusters)
    print()

    # Perform clustering
    res = kmeans.fix_photo(frames, means=params.clusters)

res = np.array(res).astype(np.uint8)
    
print('Saving file to', params.output)
Image.fromarray(res).save(params.output)

