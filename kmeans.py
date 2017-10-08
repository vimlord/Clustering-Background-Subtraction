import numpy as np
import sys, time

from sklearn.cluster import KMeans


def fix_photo(frames, means=4):
    shape = (len(frames), len(frames[0]), len(frames[0][0]))
    image = []

    bar_width = 40
    bar_prog = 0
    start = time.time()
    
    sys.stdout.write("Running K-means...\nProgress: 0/" + str(shape[1]) + " [" + (bar_width * " ") + "] ETA: N/A")
    sys.stdout.flush()

    for r in range(shape[1]):
        row = []

        for c in range(shape[2]):
            # Get each of the pixels for pixel (r,c)
            pixels = np.array([frame[r][c] for frame in frames])
            
            # Compute the means.
            clusters = KMeans(n_clusters=means).fit(pixels)
            
            # Grab label information.
            labels = clusters.labels_
            label_set = set(labels)
            label_count = {l : 0 for l in label_set}
            
            # Compute label frequency
            for l in labels:
                label_count[l] += 1
            
            # Choose a cluster.
            choice = None
            for l in label_set:
                if choice is None or label_count[choice] < label_count[l]:
                    choice = l

            # Add the value
            row.append(clusters.cluster_centers_[l]) 
        
        # Bar progress
        bar_prog = int((bar_width * (r+1.)) / shape[1])
        
        # Time remaining
        t = time.time() - start
        t = (shape[1] * t / (r+1.0)) - t

        sys.stdout.write("\rProgress: " + str(r+1) + "/" + str(shape[1]) + " [" + ("#" * bar_prog) + (" " * (bar_width - bar_prog)) + "] ETA: ")
        sys.stdout.write(time.strftime("%H hr %M min", time.gmtime(t)))
        sys.stdout.flush()

    sys.stdout.write("\rProgress: " + str(shape[1]) + "/" + str(shape[1]) + " [" + ("#" * bar_prog) + (" " * (bar_width - bar_prog)) + "] Done! ")

    print(time.strftime("(Time: %H hr %M min)", time.gmtime(time.time() - start)))

    return image


if __name__ == '__main__':
    for _ in range(1024):
        res = k_means(2, np.random.uniform(0, 256, size=(80, 3)))
        print(len(res))


