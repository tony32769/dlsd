import os

class Experiment_Helper_With_K_Fold_Validation:
	'''
		|Experiment location
		|---root_dir
			|---level_0_dir
				|---io_param_dir
				    |---tensorflow_dir
					|---targets.csv
				    |---predictions_test
				    |   |---model_1.csv
				    |   |---model_2.csv
				    |---predictions_train
				    |---predictions_validation

	'''
	def __init__(self):
		self.experiment_output_path = None
		self.root_path = None
		self.path_level_0 = None
		self.io_param_name = None
		self.path_io_param = None
		self.tensorflow_dir_path = None
		self.predictions_dir_path = None

	def set_experiment_output_path(self, path):
		self.experiment_output_path = path
		self.root_path = path

	def set_level_0_name(self, name):
		print(self.root_path)
		print(name)
		self.path_level_0 = os.path.join(self.root_path, name)

	def set_io_parameters_name(self, name):
		self.io_param_name = name

	def setup_directory(self):
		self.check_output_dirs_exist()
		self.create_io_param_dir()

	def check_output_dirs_exist(self):
		self.check_or_make_dir(self.experiment_output_path)
		self.check_or_make_dir(self.root_path)
		self.check_or_make_dir(self.path_level_0)

	def create_io_param_dir(self):
		self.path_io_param = os.path.join(self.path_level_0, self.io_param_name)
		self.check_or_make_dir(self.path_io_param)
		self.create_child_dirs()

	def create_child_dirs(self):
		self.tensorflow_dir_path = self.add_directory_to_io_param_dir("tensorflow")
		self.predictions_dir_path = self.add_directory_to_io_param_dir("predictions")
		self.predictions_train_dir_path = self.add_directory_to_io_param_dir("predictions_train")
		self.predictions_validation_dir_path = self.add_directory_to_io_param_dir("predictions_validation")

	def add_directory_to_io_param_dir(self, child_name):
		path = os.path.join(self.path_io_param,child_name)
		return self.check_or_make_dir(path)

	def check_or_make_dir(self, dir_name):
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		return dir_name

	def new_predictions_file_path_with_specifier(self, name):
		return os.path.join(self.predictions_dir_path,name+".csv")

	def new_tf_session_file_path_with_specifier(self, name):
		new_tf_session_path = os.path.join(self.tensorflow_dir_path,"tf_session_"+name)
		return new_tf_session_path

	def get_tensorflow_dir_path(self):
		return self.tensorflow_dir_path

	def get_target_file_path(self):
		return os.path.join(self.path_io_param,"target.csv")

	def get_train_target_file_path(self):
		return os.path.join(self.path_io_param,"target_train.csv")

	def get_validation_target_file_path(self):
		return os.path.join(self.path_io_param,"target_validation.csv")

	def make_new_model_prediction_file_path_with_model_name(self,model_name):
		filename = model_name+".csv"
		filepath = os.path.join(self.predictions_dir_path,filename)
		return filepath

	def make_new_model_train_prediction_file_path_with_model_name(self,model_name):
		filename = model_name+".csv"
		filepath = os.path.join(self.predictions_train_dir_path,filename)
		return filepath

	def make_new_model_validation_prediction_file_path_with_model_name(self,model_name):
		filename = model_name+".csv"
		filepath = os.path.join(self.predictions_validation_dir_path,filename)
		return filepath



