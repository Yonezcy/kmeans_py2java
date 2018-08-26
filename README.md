# Java_Call_Python

Java calls the KMeans algorithm which is implemented by Tensorflow in Python, and stores the result in Dataframe format in Spark.

In Python, using the tensorflow framework to implement the kmeans algorithm (part of the internship project), there are two ways to call python in Java. The first one is to use jython, the other is to call the command line, but since the project was originally based on the windows platform, Tensorflow under this platform only supports python3.5 now, and jython does not support Python external packages, so call the command line to achieve the call.

First, we have a nice Java Web system, which is connected with Spark. After passing the parameters to the python through the command line, the python gets the sys module and calls the prepared kmeans algorithm. The return values are printed out and retrieved through the output stream. Note that the arguments that java passes to python and python returns to java are all string type. The thing that you need to do is to parse the string by yourself.
