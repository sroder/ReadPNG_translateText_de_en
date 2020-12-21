#!/usr/bin/env python
# coding: utf-8

# # READ a PNG file
# # Extract the german Text
# # Translate to english
# # Save as text file

# In[ ]:


import pytesseract
from PIL import Image
from googletrans import Translator
from google_trans_new import google_translator
import sys, os
from os import listdir
from os.path import isfile, join, isdir
from json.decoder import JSONDecodeError



# Load Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
#where are we
print(sys.path[0])

# select all jpg files from current folder


mypath = sys.path[0]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyjpgfiles = [f for f in onlyfiles if '.png' in f]
print(f'lList of jpg files : {onlyjpgfiles}')


def get_textfromjpg(list_of_files):
    extracted_dict = {}
    for file_name in list_of_files:
        text = pytesseract.image_to_string(Image.open(file_name))
        extracted_dict[file_name] = text.splitlines()
        
    return extracted_dict

extracted_text_all = get_textfromjpg(onlyjpgfiles)

#text1 =  extracted_text_all['PXL_20201205_160438315.jpg']
#print(text1)

# Translate Text

translator = google_translator()
def translate_please(file_dict):
    translated_files = {}
    for file_name in file_dict:
        translate_list = []
        file = file_dict[file_name]
        for line in file:
            try:
                english_text = translator.translate(line,lang_src='de', lang_tgt='en')
                translate_list.append(english_text)
            except JSONDecodeError:
                pass
        translate_en =  '\n'.join(translate_list)
        translated_files[file_name] = translate_en
    
    return translated_files

# Print english Translation

translated_files = translate_please(extracted_text_all)

#print(translated_files['PXL_20201205_160438315.jpg'])

#store translated files

def write_txtfiles(list_files, lang):
    for file in list_files:
        write_file = file[:-4] + '_' + lang + '.txt'
        with open(write_file,'w') as f:
            f.write(translated_files[file])
    pass 
     
if not isdir(join(mypath, 'de')):
    get_ipython().system('mkdir de ')
    directory = join(mypath, 'de')
    os.chdir(directory)
    write_txtfiles(translated_files,'de')
    os.chdir(mypath)
else:
    directory = join(mypath, 'de')
    os.chdir(directory)
    write_txtfiles(translated_files,'de')
    os.chdir(mypath)

if not isdir(join(mypath, 'en')):
    get_ipython().system('mkdir en')
    directory = join(mypath, 'en')
    os.chdir(directory)
    write_txtfiles(extracted_text_all,'en')
    os.chdir(mypath)
else:
    directory = join(mypath, 'en')
    os.chdir(directory)
    write_txtfiles(extracted_text_all,'en')
    os.chdir(mypath)


# 

# 
