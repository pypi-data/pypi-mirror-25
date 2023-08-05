
Filework
========

This package can be found at https://github.com/aescwork/filework.

In the github repository there is sphinx-generated documentation: the main page is docs/index.html. Included in the documentation is a Usage
file (docs/usage.html) which provides a simple and hopefully helpful explanation about how the methods work and how to call them.



FileWork is a class for simplifying work with files.  

Most of the tedious code for working with a file is contained in the class, so the calling code doesn't need to bother with it.

A FileWork object can:

1. Create a file
2. Write to a File
3. Append content to a File
4. Read the entire contents of a File
5. Read a file one line at a time
6. Open or Close the Connection to a File
7. Delete a File

This module was originally created for the waxtablet application.  



After installation of this package is complete, trying to use the module might result in the following error: "ImportError: No module named filework"
or some other error message.

This probably indicates that the Python interpreter may not be able to locate the module.  In this case,
the following is recommended:

	On Linux:

		Locate where the package was installed.  In the terminal, navigate to the root directory and execute the following command:

												sudo find . -name filework.py


		This should give a path to the filework.py file.  
		Create a file called "local_python.sh" and put the following text in it:

								PYTHONPATH="/usr/local/lib/python*.*/dist-packages/filework/":"${PYTHONPATH}"
								export PYTHONPATH

		To make the module available to all users, place this file in /etc/profile.d.  Then place a line to execute this
		file somewhere in .bashrc or one of the other bash configuration files in the individual (non-root) user's terminal: 

										    . /etc/profile.d/local_python.sh

		This should cause the python interpreter to locate the filework.py file in the module.   


	On MS Windows:
		
		The following was tested on a machine running Windows 10. 
		
		(This assumes that Python is installed on the machine.)

		Locate where the package was installed.  On Windows 10, Look for the Python folder.  Its usually right under the C: drive. 
		The name of the folder probably has the version number in it as well, like "Python27".  Look for the filework folder: it should
		be in "Lib\" and then "site-packages\" folder.  

		Open up the System Properties Panel.  (You can find this by clicking on the "Settings" icon and entering "Environment Variables" in the 
		search bar.  When the panel comes up, Click the "Environment Variables" button.  Under "System variables", click "New" and type in the full path to
		the filework folder.

		Test this by opening the command line application and starting the Python interpreter (type the command "python" and press enter).
		Now try to import the module and instantiate a filework object.  Type the following:
	
		>>> import filework
		>>> sg = filework.SQLiteMgr()
		>>> sg.result

		If everything went well, 'None' should print out on the screen.  If there was an "ImportError" or any other error, try importing the
		module again and test as follows: 


		>>> import filework.filework as filework
		>>> sg = filework.FileWork()
		>>> sg.result
		


