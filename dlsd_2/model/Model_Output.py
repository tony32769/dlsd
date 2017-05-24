import logging
from dlsd_2.dataset.Dataset import *

from dlsd_2.calc import error

class Model_Output:

	def __init__(self):
		self.prediction_dataset_object = Dataset()
		self.target_dataset_object = Dataset()

	def set_prediction_dataset_object_with_numpy_array(self,numpy_array):
		self.prediction_dataset_object.set_numpy_array(numpy_array)

	def set_target_dataset_object(self,dataset_object):
		self.target_dataset_object = dataset_object

	def write_target_and_predictions_to_file(self, output_file_path):
		pass # TODO

	def calc_mae(self):
		my_error = error.mae(self.prediction_dataset_object.df, self.target_dataset_object.df)
		return my_error

	def calc_mape(self):
		return error.mape(self.prediction_dataset_object.df, self.target_dataset_object.df)

	def write_target_and_predictions_to_file(self, file_path):
		logging.info("Writing target and predictions to %s"%file_path)
		array = np.concatenate((self.target_dataset_object.df.values,self.prediction_dataset_object.df.values),axis=1)
		new_df = pd.DataFrame(array)
		new_df.index = self.target_dataset_object.df.index.values
		names_target = ["target_%d"%x for x in self.target_dataset_object.df.columns.values]
		names_predict = ["predict_%d"%x for x in self.prediction_dataset_object.df.columns.values]
		new_df.columns = names_target + names_predict
		new_df.to_csv(file_path)
	