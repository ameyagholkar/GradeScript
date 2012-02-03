Grader Script v1.0 [New version posted at https://github.com/ameyagholkar/GradeScript-v2.0]
.Made for Java and Moodle.
The Grader Script will process all the Java and related files in its directory and organize them into folders with respect to the file's UNITY ID if it is present. If not; the script will ignore that file.

It will compile and process the output of all Java files into seperate text files and place them in their respective folders. It then processes all the files in each UNITY folder and converts and concatenates each one of them into a Main Project PDF. Currently, only those files are converted which are listed in the 'legal_conversion_types' list.

Gradesheet is to be provided in pdf format before script can be executed. It is important that the file name of that PDF matches the one in the script. Gradesheet PDF can be kept with the script file in the same directory.

Test Folder is provided with the Script. This folder should contain all the test files that are required to be input re-directed to the project Java files.
The format of the test files should be: 
	<classname_of_the_file_to_be_tested>_<any_string>.<any_extension>
Currently, test files are not concatenated into the Main Project PDF.

There will be a few java files left in the Main Script folder. This means that these java files did NOT compile successfully. 

-----------------
Requirements:
-----------------
Python is required.
Installing enscript - use sudo apt-get install enscript / yum install enscript 
Installing ps2pdf - use sudo apt-get install ps2pdf / yum install ps2pdf
Installing pdftk - use sudo apt-get install pdftk / yum install pdftk


--------------------
Can be run by the following command : ./grade.py
