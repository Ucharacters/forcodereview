#реализация прокси-сервера
import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
from html_handling import generate_html_response #парсинг веб-страницы и манипуляции со строками
from http_get_function import simple_http_get #получение исходной веб-страницы


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """Функция-обработчик для всех запросов GET"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        name = 'World'

        query_components = parse_qs(urlparse(self.path).query)
        if 'favicon.ico' in query_components:
            return None
        
        if 'processor' in query_components:
            name = query_components["processor"][0]
        
        html = "<html><head></head><body>"+str(generate_html_response(simple_http_get(name)))+"</body></html>"
        self.wfile.write(bytes(html, "utf8"))
        return None
