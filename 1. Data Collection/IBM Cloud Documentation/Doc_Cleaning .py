#!/usr/bin/env python
# coding: utf-8


import re
import os


def remove_copyrights(text):

    #Remove Copyrights
    start_marker = '---\n'
    end_marker = '\n---'
    start_index = text.find(start_marker)
    end_index = text.find(end_marker, start_index) + len(end_marker)
    new_text = text[:start_index] + text[end_index:]
    return(new_text)

def blank_lines(text):

    lines = text.split('\n')
    # Remove any line that follows a blank line
    new_lines = [lines[0]]  # Always keep the first line
    for i in range(1, len(lines)):
        if not lines[i].strip() and not lines[i-1].strip():
            # If the current line is blank and the previous line is blank, skip it
            continue
        new_lines.append(lines[i])

    # Join the modified lines back into a single string
    new_text = '\n'.join(new_lines)
    
    return new_text

def remove_table(text):
    # matches rows that start and end with | for table
    pattern1 = r'^\|.*\|$[\n\r]*' 
    # matches the line that starts with "The following table"
    pattern2 = r'^The following table.*$[\n\r]*' 
    # Remove the rows that match pattern1
    result = re.sub(pattern1, '', text, flags=re.MULTILINE)
    # Remove the line that matches pattern2
    result = re.sub(pattern2, '', result, flags=re.MULTILINE)

    return result

#    Define the regular expression pattern
def first_char(text):

    pattern3 = r'^([!@#$%^&*_+\-=;\'\\:"|<,./?>])(\s+)?'
    # Remove the special character from the beginning of each line
    result = re.sub(pattern3, '', text, flags=re.MULTILINE)
    
    return result


def remove_code(text):

    #Remove code
    pattern4 = r'```[\s\S]*?```'
    result = re.sub(pattern4, '', text)
    # Define the regular expression pattern
    pattern5 = r'^\s*Example(?:\s+\w+){0,4}\s*\n?'
    # Remove the lines from the text
    result = re.sub(pattern5, '', result, flags=re.MULTILINE)
    # Define the regular expression pattern
    pattern6 = r'\n\s*\w+(?:\s+\w+)?\s*\n'
    # Remove the lines from the text which have 1-2 words and black line befor and after
    result = re.sub(pattern6, '\n', result)
    # remove rows with just a period symbol
    result = re.sub(r'^\n*[.]+\n*$', '', result, flags=re.MULTILINE)

    return(result)


# specify the root directory of doc
root_dir = 'ibm_cloud_docs_process/'
# specify the clean directory output
clean_dir = 'Clean_ibm_cloud_docs_process/'

# walk through the directory tree and find all the text files in each subdirectory
for dir_path, sub_dirs, files in os.walk(root_dir):
    # create the corresponding subdirectories in the clean directory
    clean_sub_dir = os.path.join(clean_dir, os.path.relpath(dir_path, root_dir))
    os.makedirs(clean_sub_dir, exist_ok=True)
    
    # process each text file in the current subdirectory
    for file_name in files:
        if file_name.endswith('.txt'):
            # read the original text file
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r') as f:
                text = f.read()
                
            text = remove_copyrights(text)
            text = remove_table(text)
            text = first_char(text)
            text = remove_code(text)
            text = blank_lines(text)
            
            # check text size and write to file if it's more than 200 characters
            if len(text) > 200:
                clean_file_path = os.path.join(clean_sub_dir, file_name)
                with open(clean_file_path, 'w') as f:
                    f.write(text)
            else:
                print("Text is not large enough to be written to a file.")

