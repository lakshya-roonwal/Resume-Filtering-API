import PyPDF2
from urllib.parse import urlparse
import os
import shutil

def extract_text_and_links(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        for page_number in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_number)
            text = page.extractText()

            links = []
            if '/Annots' in page:
                annots = page['/Annots']
                for annot in annots:
                    obj = annot.getObject()
                    if '/A' in obj:
                        link = obj['/A'].getObject()
                        if '/URI' in link:
                            links.append(link['/URI'])

            # print(f"Page {page_number + 1} Text: {text}")
            # print(f"Page {page_number + 1} Links: {links}")
            return links

def is_project_link(url):
    ignored_domains = {
    'linkedin.com',
    'facebook.com',
    'instagram.com',
    'twitter.com',
    'blogspot.com',
    'medium.com',
    'wordpress.com',
    'github.com',  
    'leetcode.com',
    'hackerrank.com',
    'codepen.io',
    'jsfiddle.net',
    'dev.to'
    }
    parsed_url = urlparse(url)
    
    # Check if the domain is not in the ignored_domains set
    if parsed_url.netloc not in ignored_domains:
        # You can add more conditions based on your specific use case
        return True

    return False

def does_resume_have_live_links(path):

    pdfLinks=extract_text_and_links(path)

    is_live_link_arr=[]
    for link in pdfLinks:
        is_live_link_arr.append(is_project_link(link))
    if any(is_live_link_arr):
        return True
    else:
        return False

def move_files_with_live_links(file_paths, filtered_folder):
    for file_path in file_paths:
        if does_resume_have_live_links(file_path):
            file_name = os.path.basename(file_path)
            destination = os.path.join(filtered_folder, file_name)
            shutil.move(file_path, destination)
            print(f"Moved '{file_name}' to '{filtered_folder}'.")

# Getting all the file paths 
def get_file_paths(folder_path):
    file_paths = []
    for root, directories, files in os.walk(folder_path):
        for file_name in files:
            file_paths.append(os.path.join(root, file_name))
    return file_paths

folder_path = 'all'
file_paths = get_file_paths(folder_path)

# Create a folder to store filtered files
filtered_folder = './filtered'
if not os.path.exists(filtered_folder):
    os.makedirs(filtered_folder)

# Move files with live links to the filtered folder
move_files_with_live_links(file_paths, filtered_folder)