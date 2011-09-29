#!/usr/bin/python
import os
print "##########################################################################################################"
print "#				Grader Script v1.0							 #"
print "#				Author: Ameya Gholkar							 #"
print "#This script will process the Java files which are in its current directory and generate a folder	 #"
print "# structure based on the Unity IDs. Files should be of the form	<unityid>_<exercise>__<program-name>.java#"
print "#This file format is automatically provided by NCSU moodle assignment download.				 #"
print "#    													 #"
print "#Script also generates a complied PDF file with the source code and its output for analysis		 #"
print "#			Requires enscript, ps2pdf and pdftk						 #"
print "#													 #"
print "#													 #"
print "##########################################################################################################"
legal_file_types = ['java']
legal_conversion_types = ['java', 'txt', 'ps']			
ordering = {'java': '0', 'compile': '1', 'output': '2'};
#Add the Exercise Name that you are grading. ****** No underscores allowed here. ******
exerciseName = "Exercise-15"
#Gradesheet filename - needs to be modified if the name is different other than what is mentioned. ****** No underscores allowed here. ******				
gradesheet = ''			
#Declare path = "" if there no grade-sheet is needed. Make sure you comment the path which is declared here.	
path_of_gradesheet = '' #os.getcwd() + "/" + gradesheet	
#Mostly should be the same. If there is another Test folder that you are bringing in; make sure you replace the folder name here.
#****** No underscores allowed here. ******
testfolder_name = 'Test'
path_to_test_folder = os.getcwd() + "/" + testfolder_name
# Do not Change
# ---------------------------------- #
home_path = os.getcwd()
print home_path
root = exerciseName + "/"
# ---------------------------------- #
# Add the names of files that have staff test files. Please add the exact Name. Spelling mistakes might make the script crash or Stop.
# ***** Important ***** TO be kept [''](empty) if there are no staff tests.
files_to_be_staff_tested = []
# Add the names of files that have input test files in Test Folder. Please add the exact Name. Spelling mistakes might make the script crash or Stop.
# ***** Important ***** TO be kept [''](empty) if there are no input tests.
files_to_be_input_tested = ['TriangleType.java']

# ***** Script Funtionality Begins - Do not Change ***** 
# Converts to ps.
def convert2ps(root_path, file_name):
	if file_name.find("java") != -1:
		prefix = ordering['java']
	elif file_name.find("compile") != -1:
		prefix = ordering['compile']
	elif file_name.find("output") != -1:
		prefix = ordering['output']
	else:
		prefix = '9'
	print root_path + " " + file_name
	os.system("enscript --header="+file_name+" "+root_path+"/"+file_name+" -o "+root_path+"/"+prefix+"_"+file_name.split(".")[0]+".ps")
	os.system("rm "+root_path+"/"+file_name)
	return prefix+"_"+file_name.split(".")[0]+".ps"

# Converts ps to pdf
def convert2pdf(root_path, file_name):
        os.system("ps2pdf "+root_path+"/"+file_name+" "+root_path+"/"+file_name.split(".")[0]+".pdf")
        return

## This method builds the folder strucutre and process the valid Java files. It also takes into consideration any Test files that might have to be input redirected to
## the corresponding program. Remember that all test files should be according to a specified format and in the Test folder.
def process_files( infile, file_type ):
        unityid = infile.split('_')
        if len(unityid) > 1:
                unityId = unityid[0]
        else:
                unityId = ""
        programName = infile.split('__');
        if len(programName) > 1:
                #print "ProgramName: "+programName[1]
                fileName = programName[1]
        else:
                fileName = programName[0]
        
        className = fileName.split('.')[0]

        if unityId != "":
                root_of_file = root + unityId+"/"
                if not os.path.exists(root + unityId):
                        os.system("mkdir " + root + unityId)
		if file_type == 'java':
                        path_to_compile_output = root_of_file + unityId + "_" + className + "_compile.txt"
                	path_to_output = root_of_file + unityId + "_" + className + "_output.txt"
			path_to_test_output = root_of_file + unityId + "_"
			path_to_compile_test_output = root_of_file + unityId + "_"
			path_to_java_file = root_of_file + fileName
			tests_listing = os.listdir(path_to_test_folder)
			##Following Block executes the required system commands##
                	os.system("cp " + infile + " " + fileName)
                	os.system("mv " + infile + " " + path_to_java_file)
			print "------------------------------------------------\n Compiling Java File \n------------------------------------------------"
                	os.system("javac " + fileName + " 2> " + path_to_compile_output)
			if os.stat(path_to_compile_output).st_size == 0:
				os.system("echo 'No compile Errors' > " + path_to_compile_output)
				# Check to see if there are any Test files listed; if yes: process them IF they are valid, if no: continue standard execution. 
		        	if fileName in files_to_be_input_tested:
					print "------------------------------------------------\n Tests Found - Executing Tests \n------------------------------------------------"
					for testFile in tests_listing:
						if testFile.find(className) != -1:
							os.system("java " + className + " < " + path_to_test_folder+"/"+testFile + " > " + root_of_file + testFile.split('.')[0]+"_"+unityId + "_" + className + "_output.txt")
						else:
							print "------------------------------------------------\n Test : " + testFile + " not for for the classname : "+className+"\n------------------------------------------------"
							#os.system("java " + className + " > " + path_to_output)		
				else: 
					print "------------------------------------------------\n No Tests Found - Standard Execution Selected \n------------------------------------------------"
					os.system("java " + className + " > " + path_to_output)
				# Execute the Staff Test Cases
				listing = os.listdir(home_path)
				if fileName in files_to_be_staff_tested:
					for testfile in listing:
						if testfile.find(className + "Test") != -1:
							print "Found testfile : " + testfile
							if testfile.find(".class") != -1:
								os.system("rm " + testfile.split(".")[0] + ".class")
								print "@@ Removing CLASS file : " + testfile + "@@"
							else:					
								os.system("javac "+ testfile +" 2> "+ path_to_compile_test_output)
								if os.stat(path_to_compile_test_output).st_size == 0:
									 	os.system("echo 'No compile Errors. ' > "+ path_to_compile_test_output+testfile.split('.')[0]+"_compile.txt")
										os.system("java "+testfile.split(".")[0]+" > "+path_to_test_output+testfile.split('.')[0]+"_output.txt" )
								else:
										os.system("echo 'Compile Errors Found. No Output. ' > " + path_to_test_output)
				#Removing the stale files. 	
				os.system("rm " + fileName)
		        	os.system("rm " + className + ".class")
			else:
				os.system("echo ' Compile Errors Found. No Output. ' > " + path_to_output)
				os.system("cp " + fileName + " " + infile)
				os.system("rm " + fileName)
		else:
			os.system("mv " + infile + " " + root_of_file + fileName)
                print "------------------------------------------------\n Finished processing a "+file_type+" file for "+unityId+" \n------------------------------------------------"
        else:	
		if infile != gradesheet:
                	print "------------------------------------------------\n No unity Id found. - "+infile+" \n------------------------------------------------ "
	return
## Main method. Upon call; it calls the process files method and handles any illegal file types.
def main(listing):
	for infile in listing:
		file_type_list = infile.split('.')
		print "Processing "+file_type_list[0]
		if len(file_type_list) > 1:
			file_type = file_type_list[1]
			if file_type in legal_file_types:
				process_files(infile,file_type)
			else:
				print "Illegal file type : "+file_type
				unityid_list = infile.split("_")
				if len(unityid_list) > 1:
					 if not os.path.exists(root + unityid_list[0]):
                                		os.system("mkdir " + root + unityid_list[0])
					 os.system("mv " + infile + " " + root + unityid_list[0]+"/"+ infile)
		else:
			unityid_list = infile.split("_")
			if len(unityid_list) > 1:
				 if not os.path.exists(root + unityid_list[0]):
                        		os.system("mkdir " + root + unityid_list[0])
				 os.system("mv " + infile + " " + root + unityid_list[0]+"/"+ infile)
			else:
				print "Directory found. Skipped."
	return

## Second Main method. Processes all the directories made by the 'main' method. Converts the files into ps and then to pdf. 
## Also builds the Main feedback PDF file.
def main_dir_processing(listing):
	for infile in listing:
		file_type_list = infile.split('.')
		print "Processing "+file_type_list[0]
		if len(file_type_list) > 1:
			print "File Found - "+infile+". Skipped."
		else:
			print "-----------------------------------------------------------------------------------------------------------"
			print "Directory found - "+file_type_list[0]
			if file_type_list[0] != testfolder_name:
				os.chdir(home_path + "/" + file_type_list[0])
				#After this point, all items found should be necessarily files.
				dir_file_list = os.listdir(os.getcwd())
				for infile in dir_file_list:
					if len(infile.split('.')) > 1:
						if infile.split('.')[1] in legal_conversion_types: #and infile.find(".pdf") == -1:
							convert2ps(os.getcwd(),infile)
					else:	#File found is without a type. Default Action - Convert it
						convert2ps(os.getcwd(),infile)
				dir_file_list = os.listdir(os.getcwd())
				dir_file_list.sort()
				for infile in dir_file_list:
				        if len(infile.split('.')) > 1:
						if infile.split('.')[1] in legal_conversion_types: #and infile.find(".pdf") == -1:
							convert2pdf(os.getcwd(),infile)
							os.system("rm "+infile)
				dir_file_list = os.listdir(os.getcwd())
				dir_file_list.sort()
				finalpdf_name = file_type_list[0]+"_"+exerciseName+".pdf "
				pdf_list = ""
				for infile in dir_file_list:
					if infile.find(".pdf") != -1:
				        	pdf_list = pdf_list + infile + " "
				finalpdf_path = "pdftk "+path_of_gradesheet+" "+pdf_list + "cat output " + finalpdf_name
				print finalpdf_path
				os.system(finalpdf_path) 
				os.system("rm " + pdf_list)
				os.chdir(home_path)
			print "-----------------------------------------------------------------------------------------------------------"
	return
if os.path.exists(home_path + "/" + exerciseName):
	os.system("rm -r " + exerciseName)
#Create Folder of the Exercise Name 
os.mkdir(exerciseName) 					
listing = os.listdir(home_path)
main(listing)
print "-------------------------------------------------------- Finished building Folder structure -------------------------------------------------------- "
home_path = home_path + "/" +  root 
listing = os.listdir(home_path)
main_dir_processing(listing)
print "--------------------------------------------------------------  Finished Process ------------------------------------------------------------------- "

