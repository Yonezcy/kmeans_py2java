' test module for connect java and python'
__author__ = 'zcy'

import sys
import numpy as np
import KMeans

if __name__ == '__main__':
    strs = sys.argv[1]
    strs = strs.replace('[', '').replace(']', '').split(',')
    for i in range(len(strs)):
        strs[i] = float(strs[i])

    cluster_n = int(sys.argv[2])
    row = int(sys.argv[3])
    # 经过reshape变换得到的都是array
    train_data = np.reshape(strs, (row, -1))
    train_data = np.array(train_data)
    cluster_centers, assignments = KMeans.KMeanscluster(train_data, cluster_n)

    # 将cluster_centers化为list形式，保留一位小数
    for i in range(np.shape(cluster_centers)[0]):
        cluster_centers[i] = list(cluster_centers[i])
        for j in range(np.shape(cluster_centers)[1]):
            cluster_centers[i][j] = "%.1f" % cluster_centers[i][j]
            cluster_centers[i][j] = float(cluster_centers[i][j])

    # 将train_data化为list形式，为每个样本拼接上聚类结果
    train_data = list(train_data)
    for i in range(np.shape(train_data)[0]):
        train_data[i] = list(train_data[i])
        train_data[i].append(assignments[i])
    # 将train_data保留1位小数
    for i in range(np.shape(train_data)[0]):
        # 聚类结果不用取小数
        for j in range(np.shape(train_data)[1]-1):
            train_data[i][j] = "%.1f" % train_data[i][j]
            train_data[i][j] = float(train_data[i][j])

    print(cluster_centers)
    print(assignments)
    print(train_data)