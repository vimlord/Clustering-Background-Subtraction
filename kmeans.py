import numpy as np
import sys

def k_means(k, points):
    """Performs the K-means clustering algorithm to a set of data points.
    k - The number of clusters to generate.
    points - The set of points to classify.
        precondition: All points have same dimensionality.
    return - A collection of points and their means.
    """

    min_bound = np.max(points, axis=0)
    max_bound = np.min(points, axis=0)
    
    """
    print()
    for p in points:
        print("point:", p)

    print("min_bound:", min_bound)
    print("max_bound:", max_bound)
    """
    
    bound = list(zip(
        min_bound,
        max_bound
    ))
    
    """
    upper_bound = np.array([max([v[i] for v in points]) for i in range(len(points[0]))])
    lower_bound = np.array([min([v[i] for v in points]) for i in range(len(points[0]))])
    """
    
    # Initial condition: randomized means to categorize.
    means = [
        np.array([
            np.random.uniform(bound[i][0], bound[i][1])
            for i in range(len(bound))
        ])
        for _ in range(k)
    ]

    # We will provide categorizations of the points in the return data.
    categories = None 

    iterations = 0
    complete = False

    while not complete:
        categories = [[] for _ in range(k)]

        for p in points:
            # We seek out the index of the nearest mean to the point.
            m, idx = min([(np.linalg.norm(p-m), idx) for (idx, m) in enumerate(means)])

            # Then, we categorize it under that mean.
            categories[idx].append(p)

        # Using these categories, we can generate a set of new means.
        new_means = [
                np.mean(np.array(category), axis=0) if len(category) > 0 
                else np.array([np.random.uniform(bs[0], bs[1]) for bs in bound])
                for category in categories
        ]
        
        complete = True

        for m, n in zip(means, new_means):
            if np.linalg.norm(m-n) != 0:
                # The means do not match, so the means have not yet converged.
                # Store the new means, then start a new cycle.
                means = new_means
                complete = False
                break

        iterations += 1

        # The upper bound is 2^(kd+1), where d is the dimensionality of the data
        if complete or iterations >= len(points)**(k*len(points[0])+1):
            break

    return list(zip(means, categories))


def fix_photo(frames, means=4):
    shape = (len(frames), len(frames[0]), len(frames[0][0]))
    image = []

    bar_width = 40
    bar_prog = 0
    
    sys.stdout.write("Running K-means\nProgress: 0/" + str(shape[1]) + " [" + (bar_width * " ") + "]")
    sys.stdout.flush()

    for r in range(shape[1]):
        row = []

        for c in range(shape[2]):
            # Get each of the pixels for pixel (r,c)
            pixels = np.array([frame[r][c] for frame in frames])

            # Compute the means of the photo
            res = k_means(means, pixels)
            
            # Find the mean with the largest number of hosted points
            m, cs = res[0]
            for i in range(1, len(res)):
                if len(cs) < len(res[i][1]):
                    m, cs = res[i]
            
            # Add the mean to the row
            row.append(m)
        
        # Provide the image
        image.append(row)

        bar_prog = int((bar_width * (r+1.)) / shape[1])
        sys.stdout.write("\rProgress: " + str(r+1) + "/" + str(shape[1]) + " [" + ("#" * bar_prog) + (" " * (bar_width - bar_prog)) + "]")
        sys.stdout.flush()

    print("\rProgress: " + str(shape[1]) + "/" + str(shape[1]) + " [" + ("#" * bar_prog) + (" " * (bar_width - bar_prog)) + "] 0 hr 0 min (Done!)")

    return image


if __name__ == '__main__':
    for _ in range(1024):
        res = k_means(2, np.random.uniform(0, 256, size=(80, 3)))
        print(len(res))


