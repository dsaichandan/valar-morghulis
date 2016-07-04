#Introduction
Game of Thrones is a title of well known TV show/books franchise, originally created by George R. R. Martin, in which there is enormouse number of deaths of characters, especially of the main characters.
Predicting character deaths in this famous franchise can be challenging, but also can lead to interesting results.
Steps that were required in order to accomplish death prediction of characters were:
1. Data gathering and filtering out needed attributes from different datasets into one that can be used in neural network
2. Normalizing and encoding attributes for better prediction results
3. Creation of neural network architecture and running of the train process
4. Prediction of death chance for characters that were not used during train period
Technologies that were used are *Keras neural network abstraction* and *PySide GUI* library.



#Data normalization and encoding
Datasets for given task consists of character attributes:
* Name
* Title
* Age
* Gender
* Culture
* Birth date
* House name
* Number of dead relations
* Is mother alive
* Is father alive
* Is heir alive
* Is spouse alive
* Is character noble
as input attributes and as output attribute is character alive or not.
Certain attributes must be encoded into numbers because data must have only numeric representation inside neural network and
since those values can vary from different ranges normalizing given data is a must.

#Create neural network architecture and run training
Adequate neural network model was required for the best accuracy.
After many tweaks model that gave the best results has the following features:
1. Dense layer with 100 nodes, uniform initialization and tanh activation function
2. Batch normalization layer with uniform beta initialization
3. Dense layer with 200 nodes, uniform initialization and tanh activation function
4. Dropout layer with 0.2 dropout and 
5. Dense output layer with softmax activation function
Reason for running one dropout layer is to prevent overfitting of the data.
Batch normalization layer led to better accuracy and faster performance that was not previously achieved.
Output parameter (character deathe prediction) was transformed into binary data, reason for it is that
softmax function works better with that shape of data.


#Predict death chance for characters 
Characters that were chosen for obtaining their death predictions were excluded from train samples,
because it was important not to adapt neural network with character attributes that were being predicted.

 
