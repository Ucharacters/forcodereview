#парсинг веб-страницы и манипуляции со строками
#from http_get_function import simple_http_get #получение исходной веб-страницы
from proxy_server_config import * #конфигурация прокси-сервера
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def word_tokenize(text):
    '''text word tokenizator'''  
    # delete punctuation
    punctuation = "."+","+"("+")" + '–'+'—'+'…'+'...'+'..'+"\n"
    for a_character in punctuation:
        text=text.replace(a_character,'')

    # word tokenization
    words =text.split(" ")
    # cleaning words
    words = [w.replace('\'','').replace('`','') for w in words]
    words = [w.replace('«','').replace('»','') for w in words]
    words = [w.replace('„','').replace('“','') for w in words]
    words = [w.replace('…','') for w in words]
    words = [w.replace('—','') for w in words]
    words = [w.replace('\ufeff','') for w in words]
    
    return words


def generate_html_response(the_source_web_page) -> str:
    """Эта функция готовит веб-страницу для передачи в прокси-сервер"""
    doc = BeautifulSoup(the_source_web_page,"html.parser")
    #редактируем все анкоры
    for tag in doc.find_all("a"):
        try:
            tag["href"]=tag["href"].replace(tag["href"],PROXY_CONFIG+tag["href"])
        except:
            pass
        
    def is_short_string(string):
        """Вспомогательная функция для поиска строк длиной 6 символов"""
        return len(string) == 6
    
    #создаём набор из уникальных слов 
    words_needed=set(word_tokenize(BeautifulSoup(str(doc.prettify()),"html.parser").get_text()))

    #ко всем словам длиной 6 символов добавляем SPECIAL_CHARACTER        
    for selected_word in filter(is_short_string, words_needed):
        if selected_word is not None and len(str(selected_word)) == 6:
            selected_word_with_tm_added = str(BeautifulSoup("<span>"+str(selected_word) +SPECIAL_CHARACTER+"</span>", "html.parser"))
            the_source_web_page = the_source_web_page.replace(selected_word,selected_word_with_tm_added)

    return str(the_source_web_page) 

