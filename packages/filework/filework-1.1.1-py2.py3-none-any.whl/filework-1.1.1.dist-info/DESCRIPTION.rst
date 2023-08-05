Filework
========

FileWork is a class for simplifying work with files.  Most of the tedious code for working with a file is contained in 
the class, so the calling code doesn't need to bother with it.

A FileWork object can:

1. Create a file
2. Write to a File
3. Append content to a File
4. Read the entire contents of a File
5. Read a file one line at a time
6. Open or Close the Connection to a File
7. Delete a File

There is sphinx-generated documentation: the main page is docs/html/index.html. Included in the documentation is a Usage
file (docs/html/usage.html) which provides a simple and hopefully helpful explanation about how the methods work and how
to call them.

This module was originally created for the waxtablet application.  

After installation of this package is complete, trying to use the module might result in the following error: "ImportError: No module named sqlitemgr"
or some other error message.

This probably indicates that the Python interpreter may not be able to locate the module.  In this case,
the following is recommended:

	On Linux:

		Locate where the package was installed.  In the terminal, navigate to the root directory and execute the following command:

												sudo find . -name sqlitemgr.py


		This should give a path to the sqlitemgr.py file.  
		Create a file called "local_python.sh" and put the following text in it:

								PYTHONPATH="/usr/local/lib/python*.*/dist-packages/sqlitemgr/":"${PYTHONPATH}"
								export PYTHONPATH

		To make the module available to all users, place this file in /etc/profile.d.  Then place a line to execute this
		file somewhere in .bashrc or one of the other bash configuration files in the individual (non-root) user's terminal: 

										    . /etc/profile.d/local_python.sh

		This should cause the python interpreter to locate the sqlitemgr.py file in the module.   





