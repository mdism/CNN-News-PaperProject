
import os
import re
import sys
import json
import inspect
from fpdf import FPDF
from dotenv import load_dotenv
from tabulate import tabulate
from GetCNNNews import GetNews
import time

def main():
    load_dotenv()
    url = os.getenv('cnnURL')
    print(f'*********** Welcome to "News On PDF" *********** '.title() )
    print(f"*********** Get your news paper copy from CNN: {url} *********** " )
    news = GetNews(url= url)
    topics = news.getTopics()
    header = ["SrNo", 'News Menu']
    selectedtopicId = Get_selectedFromList(topics,header)
    print(f'*********** Fetching Headline on "{topics[selectedtopicId]}" ***********')
    news.topicID = selectedtopicId
    HeadlinesList = news.getHeadlines()
    header = ["SrNo", 'News Headlines']
    news.headlineID = Get_selectedFromList(HeadlinesList,header)
    print(f'*********** Fetching News "{HeadlinesList[news.headlineID]}" ***********')
    retryCount = 3
    result = news.get_DetailedNews()
    result_obj = json.loads(result)
    while retryCount > 0:
        retryCount -= 1
        if re.search('error',result_obj['status'], re.IGNORECASE):
            print(' *+*+*+*+*+*+*+*+*+*+*+* "Error" While fetching this News Details, please try another news. *+*+*+*+*+*+*+*+*+*+*+* ' )
            HeadlinesList = news.pop_headlinebyid(news.headlineID)
            header = ["Sr. No", 'News Headlines']
            news.headlineID = Get_selectedFromList(HeadlinesList,header)
            print(f'*********** Fetching News on "{HeadlinesList[news.headlineID]}" *********** ')
            result = news.get_DetailedNews()
        else:
            break

    result = createPDF(result=result)
    
    if re.search('error', result, re.IGNORECASE):
        result = json.loads(result)
        raise Exception(f" *+*+*+*+*+*+*+*+*+*+*+* Error While Creating PDF. Please start the prcess again. Error details: {result['details']} *+*+*+*+*+*+*+*+*+*+*+* ")
    else:
        result = json.loads(result)
        print(f"*********** Process completed : {str(result['details']).title()} ********** " )
    
def Get_selectedFromList(topics, header):
    table_data = [(i+1, value) for i, value in enumerate(topics)] 
    print(tabulate(table_data,headers=header,tablefmt="grid"))
    print("*********** Enter Sr. No of corresponding menu item, to tel me what you’ve selected. *********** ")
    if len(topics):
        while True:
            try:
                type = int(input('Select News by entering its number: ').strip())
                if type <= 0:
                    sys.exit('**** Program Close ****')
                elif (type - 1) > len(topics):
                    raise ValueError
                else:
                    return type-1
            except ValueError:
                print(' *+*+*+*+*+* Invalid input. please select from the list above. To Exit `Enter "zero(0)" or :any Nagative" Number .'.title() + "*+*+*+*+*+* ")
                time.sleep(5)
                continue
            except TypeError:
                raise TypeError
    else:
        print("No topics to show.".title())

class PDF(FPDF):
    def __init__(self, header_text: str, title_text: str,orientation='portrait', format='A4'):
        super().__init__(orientation= orientation,format=format)
        self.headerText = header_text
        self.title_text = title_text
        self.is_first_page = True        
        
    def header(self):
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 9)
        self.cell(0, 10, f"{self.headerText}",f"{self.headerText}", align="L")
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="R")
    
def createPDF(result):
    try:
        load_dotenv()
        outputfile = os.getenv('OutputFilename')
        if outputfile is None:
            outputfile = "NewsPaper.pdf"

        result_obj = json.loads(result)
        result_obj = json.loads(result_obj['details'])
        news_obj = json.loads(result_obj['news'])
        # topic = news_obj['topic']
        link = news_obj['link']
        headerText = f"news source: {link}"
        headline = result_obj['newsHeadline']
        Authername = result_obj['author_name']
        timestamp = result_obj['timestamp']
        articalBody = result_obj['artical_body']

        # PDF create code starts from here
        orientation = 'portrait'
        format = 'A4'
        pdf = PDF(orientation=orientation,format=format, header_text= headerText, title_text= headline)
        pdf.add_font(fname='DejaVuSansCondensed.ttf')
        pdf.set_font("DejaVuSansCondensed",size=12)
        pdf.add_page(orientation=orientation, format=format)
        pdf.write_html(f"<h3 style: color:'green'>{headline}</h3><br></br>")
        pdf.write_html(f"Auther: {Authername}<br></br>{timestamp}<br></br>")
        pdf.write_html(articalBody)
        pdf.output(outputfile)
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        details = "Your news paper created Successfully at: " + ROOT_DIR + f"/{outputfile}"
        result = {
            "status" : 'success',
            "details":details.lower()
        }
        return json.dumps(result)       
        
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_filename = inspect.getframeinfo(exc_traceback.tb_frame).filename
        err_module_name = inspect.getmodule(exc_traceback.tb_frame).__name__
        err_line_number = exc_traceback.tb_lineno
        err_message = str(e)
        errDetails = f"error. At line No: : {err_line_number} - Error message: {err_message} inside module: {err_module_name} - in file: {err_filename}"
        print(errDetails.lower())
        result = {
            "status" : 'error',
            "details":errDetails.lower()
        }
        return json.dumps(result)        

if __name__ == '__main__':
    main()
