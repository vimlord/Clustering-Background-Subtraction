import numpy as np
import sys, time

from sklearn.cluster import DBSCAN


def neighbors(points, p, eps):
    # Find the set of neighbors
    return [j for j in range(len(points))
        if np.linalg.norm(p - points[j]) <= eps]


def fix_photo(frames, eps=4, minPts = 3):
    shape = (len(frames), len(frames[0]), len(frames[0][0]))
    image = []

    bar_width = 40
    bar_prog = 0
    start = time.time()
    
    sys.stdout.write("Running DBSCAN...\nProgress: 0/" + str(shape[1]) + " [" + (bar_width * " ") + "] ETA: N/A")
    sys.stdout.flush()

    for r in range(0, shape[1]):
        row = []
        
        for c in range(0, shape[2]):
            pixels = np.array([frame[r][c] for frame in frames])
            
            # Compute the means
            db = DBSCAN(eps=eps, min_samples=minPts).fit(pixels)
            
            # Grab label information.
            labels = db.labels_
            label_set = set(labels)
            label_count = {l : 0 for l in label_set}
            
            # Compute label frequency
            for l in labels:
                label_count[l] += 1
            
            # Choose a cluster.
            choice = None
            for l in label_set:
                if choice is None or label_count[choice] < label_count[l] and l != -1:
                    choice = l
            
            # Apply the pixel if it exists.
            if choice is None:
                row.append(np.mean(pixels, axis=0))
            else:
                row.append(np.mean(np.array([pixels[i] for i in range(len(labels)) if labels[i] == choice]), axis=0))
                   
        # Provide the image
        image.append(row)
        
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
        res = dbscan(np.random.uniform(128, 130, size=(80, 3)), 16, 4)
        print(len(res))


