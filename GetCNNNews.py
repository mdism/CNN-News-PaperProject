import inspect
import json
import re
import sys
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class GetNews:
    def __init__(self, url) -> None:
        self._baseURL = url
        self._topicID = None
        self._topicURL = None
        self._headlineID = None
        self._headlineURL =None
        self._newslist = []
    
    def newsDetails(self) -> object:
        return str(self._newsDetails)

    @property
    def baseURL(self):
        return self._baseURL

    @baseURL.setter
    def baseURL(self, url:str):
        self._baseURL = url
    
    @property
    def topicURL(self):
        return self._topicURL

    @topicURL.setter
    def topicURL(self, url:str):
        self._topicURL = url

    @property
    def topicID(self):
        return self._topicID

    @topicID.setter
    def topicID(self, ID:int):
        self._topicID = ID

    @property
    def headlineURL(self):
        return self._headlineURL

    @headlineURL.setter
    def headlineURL(self, url:str):
        self._headlineURL = url

    @property
    def headlineID(self):
        return self._headlineID

    @headlineID.setter
    def headlineID(self, ID:int):
        self._headlineID = ID

    def add_news(self, topic, link, description):
        news = News(topic= topic, link= link, description= description)
        return news

    @property
    def newslist(self):
        # return self._newslist
        for news in self._newslist:
            yield news.topic
    
    def getTopics(self):
        self.get_newsTopics()
        topics = []
        for news in self.newslist:
            topics.append(news)
        return topics

    def pop_headlinebyid(self,id):
        self._newslist.pop(id)
        newHeadlines = []
        for news in self.newslist:
            newHeadlines.append(news)
        return newHeadlines
    
    def getHeadlines(self):
        self.get_NewsHeadline_byTopicID()
        topics = []
        for news in self._newslist:
            topics.append(news.topic)
        return topics

    def get_DetailedNews(self):
        return self.get_newsDetailsByHeadlineID()
    
    def insertNews(self,  topic, link, description):
        news = self.add_news(topic, link, description)
        self._newslist.append(news)
    
    @newslist.deleter
    def newslist(self):
        del self._newslist

    def getWeb(self):
        try:
            if self._topicURL in (None, ''):
                return requests.get(self._baseURL)
            elif self._topicURL and self._headlineURL in (None, ''):
                return requests.get(self._topicURL)
            else:
                return requests.get(self._headlineURL)
            
        except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:".lower() + repr(errh)
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:".lower() + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:".lower() + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred".lower() + repr(err)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err_filename = inspect.getframeinfo(exc_traceback.tb_frame).filename
            err_module_name = inspect.getmodule(exc_traceback.tb_frame).__name__
            err_line_number = exc_traceback.tb_lineno
            err_message = str(e)
            errDetails = f"Error. At line No: : {err_line_number} - Error message: {err_message} inside module: {err_module_name} - in file: {err_filename}"
            print(errDetails.lower())
            result = {
                "error":errDetails.lower()
            }
            return json.dumps(result)

    def get_newsTopics(self):
        try:
            responce = self.getWeb()
            html_content = responce.content
            soup = BeautifulSoup(html_content, "html.parser")
            if soup.find_all('a', 'header__nav-item-link'):
                for tag in soup.find_all('a', 'header__nav-item-link')[:-2]:
                    topic = str(tag.get_text()).strip()
                    link = str(tag.get('href'))
                    self.insertNews(topic=topic, link=link, description='')
            else:
                return []
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err_filename = inspect.getframeinfo(exc_traceback.tb_frame).filename
            err_module_name = inspect.getmodule(exc_traceback.tb_frame).__name__
            err_line_number = exc_traceback.tb_lineno
            err_message = str(e)
            errDetails = f"Error. At line No: : {err_line_number} - Error message: {err_message} inside module: {err_module_name} - in file: {err_filename}"
            print(errDetails.lower())
            result = {
                "error":errDetails.lower()
            }
            return json.dumps(result)
    
    def get_NewsHeadline_byTopicID(self):
        try:
            selectedNews = self._newslist[self._topicID]
            self._topicURL = selectedNews.link
            responce = self.getWeb()
            html_content = responce.content
            # del self._newslist
            self._newslist.clear()
            # Parse the HTML
            soup_encoded = BeautifulSoup(html_content, "html.parser")
            soup = BeautifulSoup(str(soup_encoded).encode('utf-8').decode('unicode-escape'), 'html.parser')
            links = soup.find_all("a")
            if links:
                for link in links:
                    span = link.find("span", {"data-editable": "headline"})
                    if span != None:
                        data_link_type = link.get("data-link-type")
                        href = link.get("href")
                        headline = span.get_text() if span else ""
                        href = self._baseURL + href
                        self.insertNews(headline,href, '')
            else:
                return []

        except IndexError as erri:
            return "Index error:".lower() + repr(erri)
        except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:".lower() + repr(errh)
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:".lower() + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:".lower() + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred".lower() + repr(err)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err_filename = inspect.getframeinfo(exc_traceback.tb_frame).filename
            err_module_name = inspect.getmodule(exc_traceback.tb_frame).__name__
            err_line_number = exc_traceback.tb_lineno
            err_message = str(e)
            errDetails = f"Error. At line No: : {err_line_number} - Error message: {err_message} inside module: {err_module_name} - in file: {err_filename}"
            print(errDetails.lower())
            result = {
                "error":errDetails.lower()
            }
            return json.dumps(result)

    def get_newsDetailsByHeadlineID(self):
        try:
            selectedLink = self._newslist[self._headlineID]
            print(f"*********** Fetching News from: {selectedLink.link} *********** ")
            self._headlineURL = selectedLink.link
            responce = self.getWeb()
            html_content = responce.content
            soup = BeautifulSoup(html_content, "html.parser")
            header = soup.find('header')
            footer = soup.find('footer')
            relatedAlrticals = soup.find(class_="related-content related-content--article")
            for element in header.find_all():
                element.extract()
            for element in footer.find_all():
                element.extract()
            if relatedAlrticals not in (None, ''):
                for element in relatedAlrticals.find_all():
                    element.extract()
            
            newsHeadline = soup.find('h1').text.strip() if soup.find('h1').text.strip() else ""
            try:
                author_element = soup.find('div', class_='byline__names')
                author_name = author_element.text if author_element else ""
            except:
                author_name = ""
            
            try:
                timestamp_element = soup.find('div', class_='timestamp')
                timestamp_text = timestamp_element.get_text(strip=True)
            except:
                timestamp_text = ""
            
            try:
                location_element = soup.find('span', class_='source__location')
                location = location_element.text if location_element else ""
            except:
                location = None
            
            try:
                source__text = soup.find('span', class_='source__text').text if soup.find('span', class_='source__text') else ''
            except:
                source__text = None
            
            news_paragraphs = soup.find_all('p', class_='paragraph') if soup.find_all('p', class_='paragraph') else ""

            if source__text in (None, ''):
                source__text = ""
            
            if location in (None, ""):
                location = ""

            newsPrefix = location + f"({source__text})"
            data1 = []
            for count, paragraph in enumerate(news_paragraphs):
                if count == 0:
                    data = newsPrefix + "―" + paragraph.get_text(strip=True)
                    data1.append(data)
                else:
                    data = paragraph.get_text(strip=True)
                    data1.append(data)
            
            detail= NewsDetails(topic= selectedLink.topic, link=selectedLink.link, description="")
            detail.newsHeadline = newsHeadline.strip()
            detail.author_name = author_name.strip()
            detail.timestamp = timestamp_text.replace('\n', ": ").replace(','," ") if  timestamp_text.find('\n') > -1 else timestamp_text
            detail.location = location.strip()
            detail.source_text = source__text.strip()
            data2 = [f'<p>{item}</p>' for item in data1]
            detail.artical_body = " ".join(data2)
            data = {
                "status" : 'success',
                'details': str(detail)
            }
            return json.dumps(data)

        except IndexError as erri:
            return ["Index error:".lower() + repr(erri)]
        except requests.exceptions.HTTPError as errh:
            return ["An Http Error occurred:".lower() + repr(errh)]
        except requests.exceptions.ConnectionError as errc:
            return ["An error Connecting to the API occurred:".lower() + repr(errc)]
        except requests.exceptions.Timeout as errt:
            return ["A Timeout error occurred:".lower() + repr(errt)]
        except requests.exceptions.RequestException as err:
            return ["An Unknown error occurred".lower() + repr(err)]
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

class News:
    def __init__(self, topic, link, description=''):
        self._topic = topic
        self._link = link
        self._description = description

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, value):
        if value not in (None, ''):
            self._topic = value.strip()

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        if value not in (None, ''):
            self._link = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value not in (None, ''):
            self._description = value.strip()
    
    def __str__(self):
        data = {
            "link":self._link,
            "topic": self._topic,
            "description" : self._description}
        
        return json.dumps(data)

class NewsDetails:
    def __init__(self, topic: str, link:str, description='No description') -> None:
        news = News(topic=topic, link=link, description=description)
        self._news = news
        self._newsHeadline = None
        self._author_name = None
        self._timestamp = None
        self._location = None
        self._source_text = None
        self._artical_body = None

    @property
    def newsHeadline(self) -> str:
        return self._newsHeadline
    
    @newsHeadline.setter
    def newsHeadline(self, value: str) ->None:
        self._newsHeadline = value.strip()

    @property
    def author_name(self) -> str:
        return self._author_name
    
    @author_name.setter
    def author_name(self,value: str) -> None:
        self._author_name = value.strip()
    
    @property
    def timestamp(self) -> str:
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value)-> None:
        self._timestamp = value
    
    @property
    def location(self) -> str:
        return self._location
    
    @location.setter
    def location(self,value) -> None:     
        self._location = value.strip()
    
    @property
    def source_text(self) -> str:
        return self._source_text
    
    @source_text.setter
    def source_text(self, value) -> None:
        self._source_text = value.strip()
    
    @property
    def artical_body(self) -> str:
        return self._artical_body
    
    @artical_body.setter
    def artical_body(self, value) -> None:
        self._artical_body = value.strip()

    def __str__(self) -> str:
       details = {
       "news"  : str(self._news),
       "newsHeadline"  : self._newsHeadline,
       "author_name"  : self._author_name,
       "timestamp"  : self._timestamp,
       "location"  : self._location,
       "source_text"  : self._source_text,
       "artical_body"  : self._artical_body}
       return json.dumps(details)
