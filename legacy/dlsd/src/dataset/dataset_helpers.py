import numpy as np
from dlsd import debugInfo

'''
    dataset_helpers

    TensorFlow requires that data be fed into placeholders during a session.run() call
    This is done using feed dictionaries, a dictionary mapping from a numpy array to 
    a tf.Placeholder 

    This module has classes to wrap data in a way that easily allows for the filling of 
    a feed dict.

    Also contains function to split data into a training/test set 

    Alex Hartenstein 14/10/2016

'''


def splitDataToTrainAndTest(data_df,train_frac):
    '''
        @   param data_df       Pandas dataframe object of all data, each row is data point
        @   param train_frac    Float determining how much reserved for training
        
        @   return  train,test  Two pandas dataframes                 
    '''
    debugInfo(__name__,"Splitting data to train and test fraction %.2f"%(train_frac))
    train = data_df.sample(frac=train_frac,random_state=1)
    test = data_df.loc[~data_df.index.isin(train.index)]
    return train,test

def normalizeData(data_df):
    max_value = np.nanmax(data_df.values)
    debugInfo(__name__,"Max value in maxMinNormalization is %.2f"%max_value)
    return ((data_df/max_value)*.99999999) + 0.00000001, max_value

def denormalizeData(data_df,max_value):
    #return ((data_df - 0.00000001)/.99999999)*max_value
    return ((data_df)/.99999999)*max_value


class FullDataSet:
    '''
        Wrapper for a training and test dataset
        Contains two 'DataSet' objects, one for training test respectively
        Dataset objects then each contain input/output data
    '''
    def __init__(self, trainInput, trainOutput, testInput=None, testOutput=None):
        # create contained dataset objects
        self.test = DataSet()
        self.train = DataSet()
        
        if testInput is not None:
            if len(trainInput.shape)==1:
                trainInput = trainInput.reshape(-1,1)
                testInput = testInput.reshape(-1,1)
            if len(trainOutput.shape)==1:
                trainOutput = trainOutput.reshape(-1,1)
                testOutput = testOutput.reshape(-1,1)
            
            # do assertions to ensure that data is reasonable
            assert(trainInput.shape[0]==trainOutput.shape[0]),"Number of data points (rows) for train input/output do not match!"
            assert(testInput.shape[0]==testOutput.shape[0]),"Number of data points (rows) for test input/output do not match!"
            assert(testInput.shape[1]==trainInput.shape[1]),"Number of input values (columns) for test/train input do not match!"
            assert(testOutput.shape[1]==trainOutput.shape[1]),"Number of input values (columns) for test/train output do not match!"
            self.test.inputData = testInput
            self.test.outputData = testOutput
        
        self.train.inputData = trainInput
        self.train.outputData = trainOutput
        
        self.max_value = 0

    def getNumberInputs(self):
        return self.train.inputData.shape[1]
    def getNumberOutputs(self):
        return self.train.outputData.shape[1]
    def getNumberTrainingPoints(self):
        return self.train.inputData.shape[0]
    def getNumberTestPoints(self):
        return self.test.inputData.shape[0]
    def toString(self):
        debugInfo(__name__,"FullDataSet Object : [ Train : input (%d, %d)  output (%d, %d) ]\t [ Test : input (%d, %d)  output (%d, %d) ]"%(
            self.train.inputData.shape[0],
            self.train.inputData.shape[1],
            self.train.outputData.shape[0],
            self.train.outputData.shape[1],
            self.test.inputData.shape[0],
            self.test.inputData.shape[1],
            self.test.outputData.shape[0],
            self.test.outputData.shape[1]))


class DataSet:
    '''
        Wrapper for a single input/output numpy array of values
        Call 'next_batch' to get a batch of values
    '''
    def __init__(self):
        self.inputData = []
        self.outputData = []
        self.rowNames = []
        
    def next_batch(self,batch_size):
        indices = np.random.choice(self.inputData.shape[0],batch_size,replace=False)
        b_in = self.inputData[indices]
        b_out = self.outputData[indices]

        return b_in,b_out

    def num_examples(self):
        return self.inputData.shape[0]
    
    def fill_feed_dict(self,input_pl, output_pl, batch_size):
        '''
        Args : 
            data_set :      a FullDataSet object from dataset_helpers 
                                    containing two DataSet objects (for next_batch method)
            input_pl :      tensorflow Placeholder for input data
            output_pl :     tensorflow Placeholder for correct data
            batch_size :    int value determining how many rows of dataset to feed into dictionary
        Return :
            feed_dict      dict with placeholder:numpy array for giving to session.run() method
        '''
        inputData,correctOutputData = self.next_batch(batch_size)
        feed_dict = {
            input_pl : inputData,
            output_pl : correctOutputData,
        }
        return feed_dict
