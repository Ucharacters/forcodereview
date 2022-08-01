import unittest
from http_get_function import simple_http_get #получение исходной веб-страницы
from proxy_server import MyHttpRequestHandler #реализация прокси-сервера
from html_handling import generate_html_response #парсинг веб-страницы и манипуляции со строками
from proxy_server_config import * #конфигурация прокси-сервера

request="https://raw.githubusercontent.com/Ucharacters/forcodereview/main/test_html_page.html"
source_page_reply=['\ufeff<!DOCTYPE', 'html>', '<html>', '<body>', 'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit,', 'sed', 'do', 'eiusmod', 'tempor.', '<a', 'href="http://mail.ru">', 'suspendisse', 'potenti', 'nullam', 'ac', 'tortor.</a></body>', '</html>']
expected_reply=['\ufeff<!DOCTYPE',
'html>',
'<html>',
'<body>',
'Lorem',
'ipsum',
'dolor',
'sit',
'amet,',
'consectetur',
'adipiscing',
'elit,',
'sed',
'do',
'eiusmod',
'<span>tempor™</span>.',
'<a',
'href="http://mail.ru">',
'suspendisse',
'potenti',
'<span>nullam™</span>',
'ac',
'<span>tortor™</span>.</a></body>',
'</html>']

print("Start...")
class TestMethods(unittest.TestCase):

    def test_can_get_web_page_from_internet(self):
        """Проверка возможности получения веб-страницы"""
        self.assertEqual(simple_http_get(request).split(),  source_page_reply)
        
    def test_proxy_is_running(self):
        """Проверка работы прокси-сервера"""
        self.assertTrue(len(simple_http_get(PROXY_CONFIG+request)))
        
    def test_html_utilities(self):
        """Проверка замены слов и возврата HTML"""
        self.maxDiff=None
        self.assertEqual(generate_html_response(simple_http_get(request)).split(),  expected_reply)


if __name__ == '__main__':
    unittest.main()
