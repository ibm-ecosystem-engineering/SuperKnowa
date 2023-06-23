
import re
import os

def extarct_all_files(corpus_file_folder,corpus_file_folder_output):
    os.chdir(corpus_file_folder)
    file_path_list =[]
    file_path_list_new =[]
    for file in os.listdir():
        print(file)
        # Check whether file is in text format or not
        file_path = f"{corpus_file_folder}/{file}"
        file_name = file
        file_name =file_name.replace(".md",".txt")
        new_file_path = f"{corpus_file_folder_output}/{file_name}"
        file_path_list.append(file_path)
        file_path_list_new.append(new_file_path)
    return file_path_list ,file_path_list_new


def pre_processingtext(text_data):
    replaced = re.sub("\{{.*?\}}", "", text_data)
    replaced = re.sub("\{: .*?\}", "", replaced)
    replaced = re.sub("\(.*?\)|\[.*?\] |\{.*?\}", "", replaced)
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
    return replaced

def read_text_file(file_path):
    with open(file_path, 'r', encoding='latin-1') as f:
        return f.read()

corpus_file_folder = "/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs/hardware-firewall-shared"
corpus_file_folder_output = "/Users/abhilashamangal/Documents/GitHub/ibm_cloud_docs_process/hardware-firewall-shared"
os.mkdir(corpus_file_folder_output)
file_path_list,file_path_list_new  = extarct_all_files(corpus_file_folder,corpus_file_folder_output)

def write_textfile(file,text):
    f = open(file, "w")
    f.write(text)
    f.close()

i=-1
for file in file_path_list:
    i=i+1
    print("proccessing doc file for open shift----",i, file)
    try:
        text_data = read_text_file(file)
        text_data = pre_processingtext(text_data)
        write_textfile(file_path_list_new[i],text_data)
    except:
         continue

   





