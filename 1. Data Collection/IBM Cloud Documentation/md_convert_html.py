import re
import os
import markdown



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

def extarct_all_files(corpus_file_folder,corpus_file_folder_output):
    os.chdir(corpus_file_folder)
    file_path_list =[]
    file_path_list_new =[]
    for file in os.listdir():
        print(file)
        # Check whether file is in text format or not
        file_path = f"{corpus_file_folder}/{file}"
        file_name = file
        file_name =file_name.replace(".md",".html")
        new_file_path = f"{corpus_file_folder_output}/{file_name}"
        file_path_list.append(file_path)
        file_path_list_new.append(new_file_path)
    return file_path_list ,file_path_list_new

def get_all_files_folder(corpus_file_folder,corpus_file_folder_output,corpus_file_folder_output_clean):
    file_path_list =[]
    file_path_list_new =[]
    file_path_list_clean =[]
    url_list =[]
    for subdir, dirs, files in os.walk(corpus_file_folder):
        print("Sub dir ---",subdir)
        ## Create dir
        dir_name = subdir.replace(corpus_file_folder,"").strip()
        print("dir name",dir_name)
        print("dir name",len(dir_name))
        if len(dir_name) >0:
            corpus_file_folder_output1 = corpus_file_folder_output+"/"+dir_name
            os.mkdir(corpus_file_folder_output1)
            for file in files:
                file_name = file
                if ".md" in file_name:
                    url = "https://github.com/ibm-cloud-docs/"+file_name
                    file_name =file_name.replace(".md",".html")
                    file_clean = file_name.replace(".html",".txt")
                    file_clean = dir_name+"_"+file_clean
                    file_clean = file_clean.replace("/","")
                    print(file_clean)
                    file_path = os.path.join(subdir, file)
                    new_file_path = os.path.join(corpus_file_folder_output1, file_name)
                    new_file_path_clean = os.path.join(corpus_file_folder_output_clean, file_clean)

                    file_path_list.append(file_path)
                    file_path_list_new.append(new_file_path)
                    file_path_list_clean.append(new_file_path_clean)
                    url_list.append(url)
    return file_path_list ,file_path_list_new,file_path_list_clean,url_list
    
                

def pre_processingtext(text_data):
    replaced = re.sub("\{: .*?\}", "", text_data)
    #replaced = re.sub("\(.*?\)|\[.*?\] |\{.*?\}", "", replaced)
    replaced = re.sub("</?div[^>]*>", "", replaced)
    replaced = re.sub("</?p[^>]*>", "", replaced)
    replaced = re.sub("</?a[^>]*>", "", replaced)
    replaced = re.sub("</?h*[^>]*>", "", replaced)
    replaced = re.sub("</?em*[^>]*>", "", replaced)
    replaced = re.sub("</?img*[^>]*>", "", replaced)
    replaced = re.sub("&amp;", "", replaced)
    replaced = re.sub("</?href*>", "", replaced)
    replaced = replaced.replace("##","")
    replaced = replaced.replace("###","")
    replaced = replaced.replace("#","")
    replaced = replaced.replace("*","")
    replaced = replaced.replace("<strong>","")
    replaced = replaced.replace("</strong>","")
    replaced = replaced.replace("<ul>","")
    replaced = replaced.replace("</ul>","")
    replaced = replaced.replace("<li>","")
    replaced = replaced.replace("</li>","")
    replaced = replaced.replace("<ol>","")
    replaced = replaced.replace("</ol>","")

    
    return replaced

def extract_metadata(text):
    text_data = text.split("\n")
    print(len(text_data))
    text_hr = -1
    text_end = -1
    i =0;
    for line in text_data:
        if "<hr />" in line:
            if text_hr ==-1:
                text_hr =i
            else:
                text_end =i
                break
        i=i+1
    meta_data=""
    for line in text_data[text_hr:text_end+1]:
        meta_data = meta_data +"\n"+line
    return meta_data


def read_text_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        return f.read()

corpus_file_folder = "/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_v2/ibm-cloud-docs"
corpus_file_folder_output = "/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_process_metadata/"
corpus_file_folder_output_clean = "/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_process_metdata1/"
##os.mkdir(corpus_file_folder_output)
#file_path_list,file_path_list_new  = extarct_all_files(corpus_file_folder,corpus_file_folder_output)

file_path_list,file_path_list_new,file_path_list_clean,url_list  = get_all_files_folder(corpus_file_folder,corpus_file_folder_output,corpus_file_folder_output_clean)

def write_textfile(file,text):
    f = open(file, "w")
    f.write(text)
    f.close()

i=-1
print(len(file_path_list))
meta_data_list_text =[]
for file in file_path_list:
    i=i+1
    try:
        text = read_text_file(file)
        html = markdown.markdown(text)
        count_code = html.count("<code>")
        count_codeblock = html.count("{: codeblock}")
        print("Count code --",count_code)
        print("Count code --",count_codeblock )

        if count_codeblock < 1 or count_code <1:
            meta_data = extract_metadata(html)
            process_data = html.replace(meta_data,"")
            meta_data = pre_processingtext(meta_data)
            meta_data_list = meta_data.split("\n")
            for meta in meta_data_list:
                process_data = process_data.replace(meta,"")
            
            process_data = pre_processingtext(process_data)
            process_data=remove_table(process_data)
            process_data=remove_code(process_data)
            process_data=blank_lines(process_data)
            print("file clean name ---",file_path_list_clean[i])

            write_textfile(file_path_list_clean[i],process_data)
            meta_data = meta_data.replace("\n"," ");

            file_metadata="{\"file name\": \""+file_path_list_clean[i]+"\""",\"Url\": \""+url_list[i]+"\""", \"metadata""\": \""+meta_data+"\"}"
            meta_data_list_text.append(file_metadata)
        else:
            print("has more code block---")
        print("file name---",file_path_list_new[i])
        with open(file_path_list_new[i], 'w') as f:
            f.write(html)
    except Exception as e:
         print(e)
         continue
print(len(meta_data_list))
corpus_file = '/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_metadata3.txt'
file = open(corpus_file,'w')
for item in meta_data_list_text:
    file.write(item)
    file.write("\n")
file.close()

print("File created sucessfully")
   





