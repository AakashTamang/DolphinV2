import os
import re
import docx2txt
import fitz
from pytesseract import image_to_string
from subprocess import Popen, PIPE
from PIL import Image

def clean_text(text, dolower):
    '''
    Accepts the plain text and makes
    use of regex for cleaning the noise
    :param: text :type:str
    :return:cleaned text :type str
    '''
    if dolower == True:
        text = text.lower()
    # text = re.sub(
    #     r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', '', text)
    # text = re.sub('\W',' ',text)
    # text = re.sub('\s+',' ',text)
    text = re.sub(' +',' ',text)
    text = re.sub('\n+','\n',text)
    text = re.sub('\t+','\t',text)
    text = [i.strip() for i in text.splitlines()]
    text = '\n'.join(text)
    text = re.sub('\n+','\n',text)
    text = text.encode('ascii', errors='ignore').decode("utf-8")
    return text



def doc_to_text(filepath, dolower):
    '''
    Takes the doc file from the
    file path param and returns
    the cleaned the text from the
    file.
    :param filepath: path/directory of the doc file in the system
    :return: Returns the cleaned text from the file
    '''
    text = ""
    cmd = ['antiword', filepath]
    p = Popen(cmd, stdout=PIPE)
    stdout, stderr = p.communicate()
    text += stdout.decode('utf-8', 'ignore')
    text = clean_text(text,dolower)
    return text


def prepare_text_from_string(text,dolower):
    '''
    takes string of text and then
    cleans the noise
    :param: text      :type str
    :return: cleaned_text :type str
    '''
    cleaned_text = clean_text(text,dolower)
    return cleaned_text


def pdf_to_text(file_path, dolower):
    '''
    Takes filepath and extracts
    the plain text from pdf for
    training the word to vec model
    :param file_path :type str
    :return:text   :type str
    '''
    doc = fitz.open(file_path)
    number_of_pages = doc.pageCount
    text = ''
    for i in range(0, number_of_pages):
        page = doc.loadPage(i)
        pagetext = page.getText("text")
        text += pagetext
    text = clean_text(text, dolower)
    return text


def docx_to_text(file_path, dolower):
    '''
    Takes docx files and
    extracts plain text
    from the docx files
    :param file_path :type str
    :return:text     :type str
    '''
    text = ""
    text += docx2txt.process(file_path)
    text = clean_text(text,dolower)
    return text


def img_to_text(filepath, dolower):
    '''
    Takes the image file
    from the file path param and returns
    the cleaned the text from the  image file.
    :param filepath: path/directory of the image file in the system
    :return: Returns the cleaned text from the image file
    '''
    text = image_to_string(Image.open(filepath))
    text = clean_text(text,dolower)
    return text


def txt_to_text(file_path, dolower):
    '''
    Extracts plain text from txt files
    :param file_path :type str
    :return:text     :type str
    '''
    text = ""
    with open(file_path, mode='r', encoding='unicode_escape', errors='strict', buffering=1) as file:
        data = file.read()
    text += data
    text = clean_text(text, dolower)
    return text


def prepare_text(file, dolower):
    '''
    Takes the resume or any other doc;
    checks the extension of doc and then
    uses suitable methods to extract and
    clean the text
    :param: file :type str
    :return: cleaned tokenized sentences :type list
    '''
    image_extensions = ['.jpeg', '.png', '.jpg', '.psd', '.ai']
    reader_choice = {'.pdf': pdf_to_text,
                     '.docx': docx_to_text,
                     '.doc': doc_to_text,
                     '.txt': txt_to_text,
                     '.img': image_to_string}

    _, ext = os.path.splitext(file)
    if ext.lower() in image_extensions:
        ext = '.img'
    file_content = reader_choice[ext](file, dolower=dolower)

    return file_content
