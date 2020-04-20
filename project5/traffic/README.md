# ai50 - project5 - Traffic
tl;dr I was able to train a model with an accuracy rate of **99.15%** using a convolutional neural network, built with tensorflow, using maxpooling and a single hidden layer.

Here is a summary of my work:

## Background
For this project, I read a number of articles and papers.

While this tutortial required a great deal of further reading, it was a solid starting point.
https://www.tensorflow.org/tutorials/images/classification

In addition, I thought this paper was a concise, informative overview of how one stellar team approached a similar problem.
http://yann.lecun.com/exdb/publis/pdf/sermanet-ijcnn-11.pdf
- This was a great introduction to a professional approach to image classification, specific to road signs. I learned a lot, which I'll mention.

I found this notebook, which provided some terrific insight into how another team approached a similar problem. I worked through it and learned a lot.
https://github.com/kenshiro-o/CarND-Traffic-Sign-Classifier-Project/blob/master/Traffic_Sign_Classifier.ipynb

Along the way, I returned to this question a lot: what is the best learning rate? What I gathered from this article: https://machinelearningmastery.com/learning-rate-for-deep-learning-neural-networks/ is that this single parameter is crucial - it might even be the most important! So I played around a lot. And did some further reading: https://medium.com/octavian-ai/which-optimizer-and-learning-rate-should-i-use-for-deep-learning-5acb418f9b2

It's also worth mentioning that I read a few different articles on this problem in particular (road sign classification, using this specific dataset). I think that this review was within the bounds of the project, given that as students we should learn as much as possible about alternative approaches. These overiews included:

https://github.com/mohamedameen93/German-Traffic-Sign-Classification-Using-TensorFlow

And this repo (even though pre-trained models were used, it was informative):

https://github.com/mohamedameen93/German-Traffic-Sign-Classification-Using-TensorFlow

## Introduction
I started as many probably have - by failing miserably. My first tests had an accuracy of 0, which was discouraging. But after reading a great deal (above), I found that my accuracy, precison, recall, and MSE went up significantly. I finally reached a max of 99.14% accuracy.

Here is a brief overview:

## Approach
Based on the above reading, coupled with some initial attempts at solving the problem, I formulated a nuber of questions related to these topics:

- Activation Function
According to the various readings, I learned that relu is optimal for an image classification problem of this nature. This is what was used by LeCun and others for road sign classification. Furthermore, I tried others and didn't get results that were close to the ones I got here.

- Filters/Kernels
This was a difficult question to answer. For the most part, I answered it with trial and error. Based on my reading - both of the lecture and the articles cited above - it seemed best to start with 2d convolutional layers that were followed by maxpooling to sample the output and feed them into the next layer. I tried 10-12 couples of layers in this way, but found that it was optimal to use three.

As for the number of units, I found the LeCun paper to be very informative, as was this article: https://towardsdatascience.com/recognizing-traffic-signs-with-over-98-accuracy-using-deep-learning-86737aedc2ab. After 70-80 tests, I found that beginning with a number of units that matched one dimension of the images and then doubling that number of units each layer was successful.

For the hidden layer, I found that having a multiple of the output number was optimal. For example, having 120 instead of 129 was less performant. And having 80 got a worse accuracy rate. In fact, I tried 20-30 different unit numbers and ended up with the current settings.

- Greyscale Images
While the LeCun paper did show promise that using greyscale images might be optimal (or perhaps simply disregarding color information) I thought it was best to continue accounting for color information, given that the project specs do not account for such a distinction. As such, as if in a real-world scenario, I didn't want to diminish my model's ability to be used within a larger system. I think this is worth further exploration.

- Flattening
Based on my reading and on my tests, it's important to flatten the output of the conv layers to ensure that the input to the hidden layer and ultimately the output layer are consistent.

- Dropout
I learned a great deal about dropout through this assignment (especially how brilliant the concept is). In order to dimish overfitting of the models, it's important to do dropout. But my initial approach was flawed. I tried 10%, 5%, 1% (in that order). Unfortunately, I made the mistake of thinking that the improved results of diminishing the dropout meant that dropout was a bad idea. This was in part related to articles like this: https://www.kdnuggets.com/2018/09/dropout-convolutional-networks.html. But then I went to office hours and had a great conversation. I was challenged to test increasing dropout. And it worked! I tried 30%, 40%, and ultimately ended up dropping out 50% of the hidden layer. I didn't get good results from dropping out on the conv layers.

- Learning Rate
As I mentioned in the introduction, it seems like this is a crucial parameter. As such, I spent a great deal of time optimizing for this. I started with 0.001 (standard tf settings). But I found that making it bigger decreased accuracy and reducing this number increased accuracy, some of the time. Ultimately, I landed on 0.0001, which gave me the best results (0.0005, 0.00001, 0.0003, 0.0002, were not optimal).

- Epochs
Another difficult parameter. I tried 20-30 different settings, including 10, 12, 16, 18, 20, 50, 99, 100 (and others). I found that the tensorboard logs were most useful for finding the best. And honestly, for a newcomer to this conversation, this was one of the most perplexing parameters to test. I found that the results for each epoch changed based on the overall number of epochs (e.g. epoch 9/12 was very different than epoch 9/100). As such, I followed the advice of this article: https://machinelearningmastery.com/reproducible-results-neural-networks-keras/. That helped. But still I found that 16 was consistently optimal (given that 99 epochs was overkill and was prone to overfitting).

- Compile
For the compiling step, it's important to specify that from_logits=True. According to the tf documentation, this ensures that the results are more numerically stable. And for the loss function, the best is for this type of problem is CategoricalCrossentropy. I learned this from the tf image classification intro and from the LeCun paper. I wasn't able to use SparseCategoricalCrossentropy, given the dimension of the output (this was vexing, given that many articles, including a tutorial from tensorflow on image classification used this loss function).