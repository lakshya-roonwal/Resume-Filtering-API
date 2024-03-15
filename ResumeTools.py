import PyPDF2
from urllib.parse import urlparse


def extract_text_and_links(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        
        pdf_reader = PyPDF2.PdfReader(pdf_file)

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