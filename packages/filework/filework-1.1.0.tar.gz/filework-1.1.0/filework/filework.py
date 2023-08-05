"""

..	currentmodule:: filework
	:platform: Linux, Unix, Windows
	:synopsis: A simple wrapper class for easy reading (iterating) from, writing, and appending to files.

.. moduleauthor:: aescwork aescwork@protonmail.com


"""

import os

class FileWork(object):
	"""
		
	"""
	def __init__(self, file_path=None):
	
		"""
		Args:
			file_path: The name and optionally the path to the file.
		"""

		self.result = "None"
		self.status = ""
		self.fd = None
		self._file_path = file_path		# This member is private because this class uses a property to get and set it.
		self.action = ""
		self.new_path = False
		self.iter_start = 0

	def __del__(self):
		"""
		Make sure to close any open file descriptor when object is deleted.
		"""
		self.close_file()


	@property
	def file_path(self):
		"""
		Get the file path.
		"""
		return self._file_path


	@file_path.setter
	def file_path(self, val):
		"""
		This method is for assigning a value to self._file_path.  The self._file_path attribute can be accessed directly
		but the @property is used to call setter method.

		When a new value is assigned to _file_path, close_file() is called on the fd (the file descriptor) if a file was
		actually assigned to it.  Next, new_path is is set to True, meaning that the object is working with a new file.
		This will make sure that the methods which do the actual work with the files open the new file properly -- either to
		'a' (append), 'w' (write) or 'r' (read) the file.  

		Args:
			val (str):	the path to the file for the object.
		"""
		
		
		try:
			self._file_path = val
			self.close_file()
			self.new_path = True
			self._set_result_and_status("OK", "set new file_path")
		except Exception as e:
			self._set_result_and_status("FAIL", "In FileWork, file_path setter: ", str(e))
		

	def close_file(self):
		"""
		Close the file if there is a file descriptor.  This method is called automatically by @file_path.setter 
		if the value of self._file_path is changed.
		"""
		if self.fd:
			self.fd.close()
			self.is_file_open = False
			self.fd = None


	def delete_file(self, path=None):
		"""
		Delete the file whose path is assigned to the _file_path member.

		Args:
				none

		Returns:
				none
		"""
		
		if path:
			p = path
		else:
			p = self._file_path
			self.close_file()
		try:
			os.remove(p)
			self._set_result_and_status("OK", "") 
		except Exception as e:
			self._set_result_and_status("FAIL", "In FileWork, delete_file: " + str(e)) 


	def write_to_file(self, content, close=True):
		"""
		This method will write all of 'content' to the file.  The file is opened with the "w" mode: therefore if the file does not exist
		it will attempt to create it.  If the file exists already anything in the file will be deleted.  If content is None and the file does
		not exist, the only action will be that the file is created.
		
		Calls self._to_file to do the actual work.

		Args:
			content (str), (list), (NoneType):	
											The matter to be written to the file or a value of None which will only result in the file being
											created if it does not exist.
			close (bool):					
											Close the file after the function's code is finished.  
		
		"""

		self._to_file("w", "write_to_file", content)
		if close:
			self.close_file()


	def append_to_file(self, content, close=False):
		"""
		Append to a file. 

		Calls self._to_file to do the actual work.

		Args:
				content (str), (list):
										the matter to append to the file.
				close (bool):				
										Close the file when the method is finished executing.  (The default is False assuming that one may wish
										to call this method repeatedly.)
		"""
		
		self._to_file("a", "append_to_file", content)
		if close:
			self.close_file()



	def iterate_through_file(self, move):
		"""
		Read a file by iterating or stepping through it one line at a time.  This method essentially does the same thing as calling
		next(filework_object.fd) but outputs helpful messages (see Returns below) and handles exceptions for the calling code.

		Args:
		
			move (str):		what action to take with this method call: values are "n" for go to the next line, or "s" to stop iterating
							through the file, close the file descriptor, etc.

		Returns:
					(str) The current line of the file which has just been read, "EOF" which means the end of the file has been reached,
							or "ERR" which means something else went wrong..
							
		"""
	
		if self.new_path or self.action != "r":
			self._set_action("r")
			

		contents = "ERR"

		if self.is_file_open:
			if move == "n":
				try:
					self.fd.seek(self.iter_start)		# use self.fd.seek(self.start_iter) - starts location of fd at zero
					contents = self.fd.readline()		# call readline(), assign to be returned
					self.iter_start = self.fd.tell()	# use f.tell() to get the current position of self.fd, assign this to self.start_iter
					if len(contents) == 0:				# readline() returns an empty string at the end of the file
						contents = "EOF"
						self.close_file()
						self.iter_start = 0
						self._set_result_and_status("OK", "")
				except Exception as e:
					self.close_file()
					self.iter_start = 0
					self._set_result_and_status("FAIL", "In FileWork, iterate_through_file(): " + str(e))

			elif move == "s":
				self._set_result_and_status("OK", "")
				self.close_file()
				
			
		return contents


	def read_from_file(self):
		"""
		Read and return the entire contents of the file of this object.  

		Args:
				none

		Returns:
					(string) The entire contents of a file, or "ERR" if there was a problem.
							
		"""


		if self.new_path or self.action != "r":
			self._set_action("r")

		content = "ERR"
		
		if self.is_file_open:
			try:
				content = self.fd.read()
				self._set_result_and_status("OK", "")
			except Exception as e:
				content = "ERR"
				self._set_result_and_status("FAIL", "In FileWork, read_from_file(): ", str(e))


		return content


	def _set_action(self, new_action):

		self.new_path = False
		
		path = self.file_path
	
		self.action = new_action
		self.file_path = path

		return self._file_open()



	def _file_open(self):
		"""
		Private method for the object to open the file in the correct way for the operation to be performed.
		"""
		self.is_file_open = True
		try:			
			self.fd = open(self.file_path, self.action)
			self._set_result_and_status("OK", "")
		except Exception as e:
			self._set_result_and_status("FAIL", "in FileWork _file_open: " + str(e))
			self.is_file_open = False
				

	def _to_file(self, action, f_name, content):

		"""
		Private method for either writing or appending content to a file.

		Args:
				action (str):	"w", "a", "r" (The mode in which the file is to be opened).
				f_name (str):	The name of the "public facing" function which calls this method (for the message in teh status member).
				content (str), (list) (NoneType):	the matter to append to the file.
		"""

		if self.new_path or self.action != action:
			self._set_action(action) 

		if type(content) is list:
			content = "".join(content)

		if content and self.is_file_open:
			try:
				self.fd.write(content)
				self._set_result_and_status("OK", "")
			except Exception as e:
				msg = "In Filework " + f_name + "(): " + str(e)
				self._set_result_and_status("FAIL", msg)


	def _set_result_and_status(self, result, status):
		"""
		Set self.result and self.status here to help DRY out the code in the above methods.
		
		Args:
			result (string):	the result of the operation performed by the calling method.
			status (string):	the status (description) of the outcome of the operation performed by the calling method.
		"""
		self.result = result
		self.status = status

