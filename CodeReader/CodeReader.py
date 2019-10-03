#
# Code Reader Assessment for Capital One
# 
# Author: Wei Zhou 
#
# Program to make comments about code merging into the build pipeline
# Program files are to be places into the "Checkin" folder
#
# This program will read the following file types: .java .js .py .c 
#   
# Reading Python(.py) file assumptions: 
# Triple quotes(''') are docstrings and not the same as multiline comment
# Lines with 2 or more consecutive comments are considered as a comment block

# OS module to interact with the operating system
import os

# Change the current working directory
os.chdir('Checkin')

# Run the following for each of the files in the directory
for f in os.listdir():

    file_name, file_ext = os.path.splitext(f)
    print(f)

    # Open and read each file
    with open(f, 'r') as rf:

        # Initialize the count variables
        line_count = 0
        comment_count = 0
        block_comment_count = 0
        total_block_count = 0 
        todo_count = 0
        block_comment_flag = False

        #For Java(.java), Javascript(.js) or C/C++(.c) file extension
        if (file_ext == '.js' or file_ext == '.java' or file_ext == '.c'):

            # Initialize block variable and comment symbol
            comment = "//"
            block_comment_start = "/*"
            block_comment_end = "*/"

            # Runs for every line in the file  
            for line in rf:

                # Increase line counter for reading a line
                line_count = line_count + 1 

                # Look for comment symbol in a line
                if (comment in line):
                
                     # Increase line counter for reading a comment if it's not a string
                    if (line[:line.find(comment)].count("\"") % 2 == 0):
                        comment_count = comment_count + 1 
                      
                        # Increase TODO counter for finding a TODO in a comment
                        if (line[line.find(comment)+2:].lstrip()[:5] == "TODO:"):
                            todo_count = todo_count + 1

                # Set a flag when block comment symbols found and keeps track of block count    
                if (block_comment_start in line):

                    # Reset flag if block comment ends on the same line
                    if (block_comment_end not in line):
                        block_comment_flag = True    
                    else: 
                        comment_count = comment_count + 1
                        block_comment_count = block_comment_count + 1
                    total_block_count = total_block_count + 1
                    
                # Treat code as comment when block comment flag is true    
                if (block_comment_flag):
                    comment_count = comment_count + 1
                    block_comment_count = block_comment_count + 1

                    # Reset block comment flag when the ending block symbols are detected
                    if (block_comment_end in line):
                        block_comment_flag = False

        # For Python(.py) extension
        if (file_ext == '.py'):
            
            # Initialize block variable and comment symbol
            block_count = 1
            comment = "#"

            # Runs for every line in the file
            for line in rf:

                # Increase line counter
                line_count = line_count + 1 
 
                # Look for comment symbol in a line
                if (comment in line):

                    # Increase comment count when the comment symbol is not part of a string
                    if (line[:line.find(comment)].count("'") % 2 == 0):
                  
                        if (line[:line.find(comment)].count("\"") % 2 == 0):
                            comment_count = comment_count + 1 
                        
                            # Increase consecutive comment count
                            if (block_comment_flag):
                                block_count = block_count + 1
                            block_comment_flag = True

                            # Look for TODOs in a comment
                            if (line[line.find(comment)+1:].lstrip()[:5] == "TODO:"):
                                todo_count = todo_count + 1
                        else:
                            # Reset consecutive comment count when comment symbol is used in string
                            block_comment_flag = False
                    else:
                        block_comment_flag = False
                    

                else :

                    # Reset consecutive comment count when comment symbol not found
                    block_comment_flag = False

                    # Add the number of lines in the last block to the total block line count
                    if (block_count > 1 ):
                        block_comment_count = block_comment_count + block_count
                        total_block_count = total_block_count + 1

                    #Reset block line count
                    block_count = 1
       


        #Print final results to the console for each file
        print("Total # lines: ", line_count)
        print("Total # of comment lines: ", comment_count)
        print("Total # of single line comments: ", comment_count-block_comment_count)
        print("Total # of comment lines within block comments: ", block_comment_count)
        print("Total # of block line comments: ", total_block_count)
        print("Total # of TODO's:", todo_count)