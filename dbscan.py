import numpy as np
import sys, time


def neighbors(points, p, eps):
    # Find the set of neighbors
    return [j for j in range(len(points))
        if np.linalg.norm(p - points[j]) <= eps]


def dbscan(points, eps, minPts):
    """Performs the DBSCAN clustering algorithm on a set of points.
    """
    C = 0
    
    # Mark points as unlabeled.
    labels = [None for p in points]

    Nss = [None for p in points]

    for i in range(len(points)):

        # If a point has already been classified, don't classify it.
        if labels[i] != None:
            continue

        p = points[i]

        # Find the set of neighbors
        if Nss[i] is None:
            Nss[i] = neighbors(points, p, eps)
        Ns = Nss[i]

        if len(Ns) < minPts:
            # There are insufficient points to make a cluster.
            # So, mark it as noise in case a cluster is found later.
            continue

        # Create the cluster
        S = Ns
        #labels[i] = C

        inS = [x in S for x in range(len(points))]

        j = 0
        while j < len(S):
            s = S[j]
            q = points[s]

            if labels[s] != None:
                # The point is not noise, so ignore it.
                j += 1
                continue

            labels[s] = C

            if Nss[s] == None:
                Nss[s] = neighbors(points, points[s], eps)

            if len(Nss[s]) >= minPts:
                # Add all of the layers.
                S = S + [x for x in Nss[s] if x not in S]
            
            j += 1

        
        # Indicate that another cluster was found.
        C += 1

    # Find the representative data of the cluster.
    categories = [[] for _ in range(C)]

    # Grab the categories
    for i in range(len(points)):
        # Add the point
        if labels[i] != None:
            categories[labels[i]].append(points[i])

    # Grab the means and actual categories

    means = [(c, np.mean(np.array(c), axis=0))
            for c in categories if len(c) > 0]
    
    return means


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
            # Get each of the pixels for pixel (r,c)
            pixels = np.array([frame[r][c] for frame in frames])

            # Compute the means of the photo
            res = dbscan(pixels, eps, minPts)
            
            if len(res) > 0:
                data = [len(cs) for p, cs in res]

                # Find the mean with the largest number of hosted points
                p = res[data.index(max(data))][1]
                
                # Add the mean to the row
                row.append(p)
            else:
                row.append(np.mean(pixels, axis=0))
        
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


