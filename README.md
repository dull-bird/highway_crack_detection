# Highway Crack Detection

Code of my BEng thesis project in Zhejiang University (2017-2018): highway crack detection (高速公路裂纹检测).

[Thesis (中文)](https://github.com/dull-bird/highway_crack_detection/blob/master/%E6%AF%95%E8%AE%BE.pdf)

The algorithm is more about feature engineering. Due to the limitation of computing power, we don't use deep learning.

The detection algorithms are mainly divided into the following four steps:
1. Image segmentation, which is able to extract the part between white lines of a lane and divide the original image into sub-image sequences;
2. Illumination compensation, which is possible to model the illumination distribution in the sub-image and compensate for uneven illumination.
3. Crack extraction, which is able to extract suspected crack areas in the sub-image;
4. Crack identification, which is possible to identify the suspected crack area and determine whether it belongs to a crack, and then make a simple classification of crack types.

At present, the system can perform batch crack detection on the input images and export the detection results. The results of testing 1000 highway images show that the total false positive rate is 25% and the total missed detection rate is 4%, indicating that the detection system has certain practical value.

