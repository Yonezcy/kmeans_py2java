# -- coding：utf-8 --
__author__ = '赵晨宇'

import tensorflow as tf
from numpy import *
from random import shuffle

def KMeanscluster(train, cluster_n, max_iter):
    '''K-Means Algorithm Use Tensorflow.

    Args:
    train:Training dataset of samples.
    cluster_n:Number of cluster centers.
    max_iter:Maximum number of iterations.

    Returns:
    cluster_centers:Eigenvalues of cluster centers.
    assignments:The category of each sample.
    '''

    #聚类中心数量应小于样本总数
    assert cluster_n < len(train)

    train_shuffle = list(range(len(train)))
    shuffle(train_shuffle)
    #特征数量
    dim = shape(train)[1]
    #最大迭代次数
    iteration = max_iter

    graph = tf.Graph()
    with graph.as_default():
        #聚类中心
        cluster_centers = [tf.Variable(train[train_shuffle[i]]) for i in range(cluster_n)]
        cluster_center_newvalue = tf.placeholder("float64", [dim])
        change1 = [tf.Variable(0) for i in range(cluster_n)]
        for i in range(cluster_n):
            change1[i] = tf.assign(cluster_centers[i], cluster_center_newvalue)

        #标志类别的变量
        assignments = [tf.Variable(0) for i in range(len(train))]
        assignment_newvalue = tf.placeholder("int32")
        change2 = [tf.Variable(0) for i in range(len(train))]
        for i in range(len(train)):
            change2[i] = tf.assign(assignments[i], assignment_newvalue)

        #属于同一类别的样本
        mean_input = tf.placeholder("float", [None, dim])
        #同类样本的新聚类中心
        mean_op = tf.reduce_mean(mean_input, 0)

        #计算两两样本间的距离
        v1 = tf.placeholder("float", [dim])
        v2 = tf.placeholder("float", [dim])
        distance = tf.sqrt(tf.reduce_sum(tf.pow(tf.subtract(v1, v2), 2)))

        #当前样本距离聚类中心的距离
        center_distance = tf.placeholder("float64", [cluster_n])
        #当前样本属于的类别
        cluster_assignment = tf.argmin(center_distance, 0)

        with tf.Session() as sess:
            init_op = tf.global_variables_initializer()
            sess.run(init_op)
            for iteration_number in range(iteration):

                for train_nn in range(len(train)):
                    #每个样本到聚类中心的距离
                    distances = [sess.run(distance, feed_dict={
                                v1:train[train_nn], v2:sess.run(cluster_new)})
                                 for cluster_new in cluster_centers]
                    #计算最小距离下标,即判断样本属于哪一类
                    assignment = sess.run(cluster_assignment, feed_dict={
                            center_distance:distances})
                    #更新所有样本的类别矩阵
                    sess.run(change2[train_nn], feed_dict={assignment_newvalue:assignment})

                cluster_centers1 = sess.run(cluster_centers)

                for cluster in range(cluster_n):
                    #第n类中心的样本集合
                    train_n = [train[i] for i in range(len(train))
                               if sess.run(assignments[i]) == cluster]
                    #新聚类中心的位置
                    location = sess.run(mean_op, feed_dict={
                                    mean_input: train_n})
                    #更新聚类中心
                    sess.run(change1[cluster], feed_dict={cluster_center_newvalue:location})

                #前一代个体和后一代相同时停止迭代
                if (array(cluster_centers1) == array(sess.run(cluster_centers))).all(): break;

            cluster_centers = sess.run(cluster_centers)
            assignments = sess.run(assignments)
    return cluster_centers, assignments
