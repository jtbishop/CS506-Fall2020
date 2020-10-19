def read_csv(csv_file_path):
    """
        Given a path to a csv file, return a matrix (list of lists)
        in row major.
    """
    arr: list = []

    with open(csv_file_path) as csv_file:
        for i in csv_file.readlines():
            arr.append(i.split())


    print(arr)



if __name__=='__main__':
    read_csv("C:/Users/bishj/OneDrive/College Notebook/Boston University/Fall Senior Year/CS 506/CS506-Fall2020/02-library/tests/test_files/dataset_1.csv")
