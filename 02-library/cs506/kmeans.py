from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    summation: list = [sum(x) for x in zip(*points)]
    return [colSum /len(points) for colSum in summation]


def update_centers(dataset, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    temp = defaultdict(list)
    centers = []
    for assignment, point in zip(assignments, dataset):
        temp[assignment].append(point)

    for i in temp.values():
        centers.append(point_avg(i))

    return centers

def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    if (hasattr(a[0], '__len__')):
        rows = len(a); cols = len(a[0])
        summation = 0

        for i in range(rows):
            vec = [a[i][j] - b[i][j] for j in range(cols)]

            s = sum(i**2 for i in vec)
            summation += s


    else:
        summation = sum([(a[i] - b[i])**2 for i in range(len(a))])

    return summation**(1/2)

def distance_squared(a, b):
    return distance(a, b)**2

def generate_k(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    points = [dataset[random.randint(0, len(dataset) - 1)] for i in range(0, k)]
    return points

def cost_function(clustering):
    total_cost = 0
    for data_set in clustering.keys():
        datas = clustering[data_set]
        centers = point_avg(datas)
        for indiv_data in datas:
            total_cost += distance(indiv_data, centers)
    return total_cost

def generate_k_pp(dataset, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    where points are picked with a probability proportional
    to their distance as per kmeans pp
    """
    random_centers: list = generate_k(dataset, k)
    random_assignments: list = assign_points(dataset, random_centers)

    distances: list = [distance(random_centers[random_assignments[i]], dataset[i]) for i in range(len(dataset))]
    
    # Generate indices for each distance then sort in ascending order of distance
    indices: list = [i for i in range(len(distances))]
    indices = [j for i, j in sorted(zip(distances, indices))]

    weighted_indices: list = []
    for i in range(len(indices)):
        n: int = int(distances[indices[i]])
        
        for j in range(n):
            weighted_indices.append(indices[i])

    N: int = len(weighted_indices) - 1

    pp_centers: list = []
    random_numbers: list = []
    choices: list = []
    for i in range(k):
        random_choice: int = random.randint(0, N)
        index = weighted_indices[random_choice]

        if random_choice in random_numbers or index in choices:
            while random_choice in choices or index in choices:
                random_choice = random.randint(0, N)
                index = weighted_indices[random_choice]

        random_numbers.append(random_choice)
        choices.append(index)
        pp_centers.append(dataset[index])
    
    return pp_centers


def _do_lloyds_algo(dataset, k_points):
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering


def k_means(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")
    
    k_points = generate_k(dataset, k)
    return _do_lloyds_algo(dataset, k_points)


def k_means_pp(dataset, k):
    if k not in range(1, len(dataset)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")

    k_points = generate_k_pp(dataset, k)
    return _do_lloyds_algo(dataset, k_points)

if __name__ =='__main__':
    from cs506 import read

    data = read.read_csv('D:/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/CS506-Fall2020/02-library/tests/test_files/dataset_1.csv')
    res = (k_means(data, 4))
    print(res[0])