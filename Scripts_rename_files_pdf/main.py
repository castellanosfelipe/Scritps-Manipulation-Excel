import fitz
import os
import re
import shutil
import time
import math

# ==============================================================================
# =========================== functions ========================================
# ==============================================================================

# list files in directory
def list_files_recursively(path_directory):
    list_files = []
    for dirpath, dirnames, filenames in os.walk(path_directory):
        for filename in filenames:
            list_files.append(os.path.join(dirpath, filename))
    print(f"number of files in {path_directory} :", len(list_files))
    return list_files

# get the text of a PDF file
def get_pdf_text_first_page(pdf_path):
    pdf = fitz.open(pdf_path)
    page = pdf.load_page(0)
    text = page.get_text()
    pdf.close()
    return text

# get 1/4 of text of a PDF file
def get_pdf_text_first_page_1_4(text_first_page):
    return text_first_page[0:int(len(text_first_page)/4)]

# has matching pattern the PDF file
def has_matching_pattern(text, regular_expression):
    pattern_found = re.search(regular_expression, text)
    return bool(pattern_found)

def get_name_resolution_file(text, pattern):
    for line in text.split('\n'):
        if re.search(pattern, line):
            return line.strip()

def get_name_resolution_file_ocurrence(text, pattern, occurrence=0):
    count = 0
    for line in text.split('\n'):
        if re.search(pattern, line):
            count += 1
            if count == occurrence:
                return line.strip()
    return None

def contains_special_characters(text):
    # Regular expression to match special characters
    special_chars_pattern = re.compile(r'[<>:"/\\|?*]')
    
    # Check if the text contains any special characters
    if special_chars_pattern.search(text):
        return True
    else:
        return False

def rename_original_files(path_folder_original, path_directory_rename_files, file_name_mapping):
    list_files_original = list_files_recursively(path_folder_original)
    for file_i in list_files_original:
        if file_i in file_name_mapping:
            name_of_path = file_i.split(path_folder_original)[-1]
            sub_path  = name_of_path.split(os.path.basename(file_i))[0]
            path = path_directory_rename_files + sub_path
            original_file_name = os.path.splitext(os.path.basename(file_i))[0]
            rename_file_name = os.path.splitext(os.path.basename(file_name_mapping[file_i]))[0]
            final_name_processed = os.path.join(path, rename_file_name + "__" + original_file_name + ".pdf")
            os.makedirs(os.path.dirname(final_name_processed), exist_ok=True)
            shutil.copy2(file_i, final_name_processed)

# ==============================================================================
# =========================== variables ========================================
# ==============================================================================

REGULAR_EXPRESION = r'[Rr][Ee][Ss][Oo][Ll][Uu][Cc][Ii][ÓóA-zÀ-ú]+'

# ==============================================================================
# ======================== main functions ======================================
# ==============================================================================

def process_folder(path_folder_original, path_folder_processed, occurrence=1, batch_size=50):

    print(80 * "*")
    print("PROCESS FOLDER INIT")
    print(80 * "*" + "\n")

    print("path_folder_original: ",   path_folder_original)
    print("path_folder_processed: ", path_folder_processed + "\n")
    list_files_process = list_files_recursively(path_folder_original)

    time_init = time.time()

    init_index = 0
    end_index  = init_index + batch_size
    end_index  = min(end_index, len(list_files_process))

    num_batch = math.ceil(len(list_files_process) / batch_size)
    batch_iter = 0
    total_files_rename = 0
    total_files_fail   = 0

    file_name_mapping = {}

    while batch_iter < num_batch:

        list_files_process_batch = list_files_process[init_index:end_index]
        print()
        print(80 * "*")
        print("BATCH ITER: ", batch_iter)
        print("BATCH SIZE: ", len(list_files_process_batch))
        print(80 * "*" + "\n")

        num_files_renames  = 0
        num_files_fail     = 0

        for index_file_i, file_i in enumerate(list_files_process_batch):

            name_of_path = file_i.split(path_folder_original)[-1]

            first_page_text_file_i     = get_pdf_text_first_page(file_i)
            first_page_1_4_text_file_i = get_pdf_text_first_page_1_4(first_page_text_file_i)
            exist_matching_pattern_    = has_matching_pattern(first_page_1_4_text_file_i, REGULAR_EXPRESION)
            resolution_name            = get_name_resolution_file_ocurrence(first_page_1_4_text_file_i, REGULAR_EXPRESION, occurrence)
            if (exist_matching_pattern_):
                special_characters     = contains_special_characters(resolution_name)
            else:
                special_characters = False

            if exist_matching_pattern_ and not special_characters and resolution_name != None: # if exist matching pattern

                original_file_name = os.path.splitext(os.path.basename(file_i))[0]

                resolution_name = resolution_name.replace(" ", "_")
                resolution_name = resolution_name[0].upper() + resolution_name[1:].lower()
                name_file = resolution_name + ".pdf"
                sub_path  = name_of_path.split(os.path.basename(file_i))[0]

                path = path_folder_processed + sub_path
                final_name_processed = os.path.join(path, name_file)

                if (os.path.isfile(final_name_processed)):
                    consecutive_fails = 1
                    name_file = resolution_name + "_" + str(consecutive_fails) + ".pdf"
                    final_name_processed = os.path.join(path, name_file)
                    while (os.path.isfile(final_name_processed)):
                        consecutive_fails += 1
                        name_file = resolution_name + "_" + str(consecutive_fails) + ".pdf"
                        final_name_processed = os.path.join(path, name_file)
                    name_file =  resolution_name + "_" + str(consecutive_fails) + ".pdf"
                    path_file_repeted = os.path.join(path, name_file)
                    os.makedirs(os.path.dirname(path_file_repeted), exist_ok=True)
                    shutil.copy2(file_i, path_file_repeted)
                    file_name_mapping[file_i] = path_file_repeted
                else:
                    os.makedirs(os.path.dirname(final_name_processed), exist_ok=True)
                    shutil.copy2(file_i,final_name_processed)
                    file_name_mapping[file_i] = final_name_processed
                num_files_renames += 1
            else: # if not exist matching pattern

                original_file_name = os.path.splitext(os.path.basename(file_i))[0]
                name_file = "_undefined_" + original_file_name + ".pdf"

                sub_path  = name_of_path.split(os.path.basename(file_i))[0]
                path = path_folder_processed + sub_path
                final_name_processed = os.path.join(path, name_file)

                if (os.path.isfile(final_name_processed)):
                    consecutive_fails = 1
                    name_file = "_undefined_" + original_file_name + "_" + str(consecutive_fails) + ".pdf"
                    final_name_processed = os.path.join(path, name_file)
                    while (os.path.isfile(final_name_processed)):
                        consecutive_fails += 1
                        name_file = "_undefined_" + original_file_name + "_" + str(consecutive_fails) + ".pdf"
                        final_name_processed = os.path.join(path, name_file)
                    name_file = "_undefined_" + original_file_name + "_" + str(consecutive_fails) + ".pdf"
                    path_file_repeted = os.path.join(path, name_file)
                    os.makedirs(os.path.dirname(path_file_repeted), exist_ok=True)
                    shutil.copy2(file_i, path_file_repeted)
                    file_name_mapping[file_i] = path_file_repeted
                else:
                    os.makedirs(os.path.dirname(final_name_processed), exist_ok=True)
                    shutil.copy2(file_i, final_name_processed)
                    file_name_mapping[file_i] = final_name_processed
                num_files_fail += 1

        print("number of files renamed: ", num_files_renames)
        print("number of files fail: ",       num_files_fail)
        print(80*"-")
        print("total_files_rename: ", total_files_rename)
        print("total_files_fail: ",     total_files_fail)

        total_files_rename += num_files_renames
        total_files_fail   += num_files_fail
        batch_iter += 1
        init_index = end_index
        end_index  = min(init_index + batch_size, len(list_files_process))
    print("total_files_rename: ", total_files_rename)
    print("total_files_fail: ",     total_files_fail)
    time_final = time.time()
    print("time_running: ", time_final - time_init)
    return file_name_mapping

name_original_folder_ocr = "original_ocr_documents_246_prueba"
path_original_folder_ocr = os.path.join(os.getcwd(), name_original_folder_ocr)

name_processed_folder_ocr = "processed_documents_ocr_246_prueba"
path_processed_folder_ocr = os.path.join(os.getcwd(), name_processed_folder_ocr)

name_original_files_ocr = "renamed_original_documents_ocr_246_prueba"
path_original_files_ocr = os.path.join(os.getcwd(), name_original_files_ocr)

original_folder_files = "original_documents_ocr"
path_original_folder_files = os.path.join(os.getcwd(), original_folder_files)

file_name_mapping = process_folder(path_original_folder_ocr, path_processed_folder_ocr, 0, 500)
print("file_name_mapping: ", file_name_mapping)
rename_original_files(path_original_folder_files, path_original_files_ocr, file_name_mapping)

time.sleep(100000)
