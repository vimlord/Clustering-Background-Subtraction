from kmeans import *
import sys

from PIL import Image

if len(sys.argv) < 4:
    print('Proper use: python video_cluster/main.py <frames> <input> <output>')

num_frames = int(sys.argv[1])

frames = np.array([
    np.asarray(Image.open(sys.argv[2] + "/frame" + str(i) + ".png"))
    for i in range(1, num_frames+1)
])

print("Extracted frames for", frames.shape[2], "by", frames.shape[1], "video")

Image.fromarray(np.array(fix_photo(frames)).astype(np.uint8)).save(sys.argv[3])

