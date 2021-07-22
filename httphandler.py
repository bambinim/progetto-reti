import http.server
from pathlib import Path
import os
import json


class HttpHandler(http.server.SimpleHTTPRequestHandler):

    BASE_DIR = Path(os.path.dirname(__file__))

    def __set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def __load_services(self) -> dict or None:
        if os.path.exists(self.BASE_DIR / 'services.json'):
            with open(self.BASE_DIR / 'services.json', 'r', encoding='utf-8') as fstream:
                return json.load(fstream)
        return None

    def do_GET(self) -> None:
        if self.path == '/':
            self.__index()
        elif self.path == '/file.pdf':
            self.__file_pdf()
        else:
            service_found = False
            for i in self.__load_services():
                if i['path'] == self.path:
                    service_found = True
                    self.__service(i)
            if not service_found:
                self.send_error(404, 'Page not found')

    def __index(self):
        self.__set_response()
        with open(self.BASE_DIR / 'public' / 'index.html') as fstream:
            page = fstream.read()
        data = ''
        for i in self.__load_services():
            data = data + '<tr>' \
                          '<td>{0}</td>' \
                          '<td><a href="{1}" class="btn btn-outline-primary">' \
                          '<i class="fas fa-link" aria-hidden="true"></i></a></td>' \
                          '</tr>'.format(i['name'], i['path'])
        page = page.replace('{% content %}', data)
        self.wfile.write(page.encode('utf-8'))

    def __service(self, service: dict):
        self.__set_response()
        with open(self.BASE_DIR / 'public' / 'service.html', 'r') as fstream:
            page = fstream.read()
        data = '<h1>{0}</h1><p>{1}</p>'.format(service['name'], service['description'])
        page = page.replace('{% content %}', data)
        self.wfile.write(page.encode('utf-8'))

    def __file_pdf(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/pdf')
        self.send_header('Content-Disposition', 'attachment;filename="file.pdf"')
        self.send_header('Content-Description', 'File Transfer')
        self.send_header('Pragma', 'public')
        self.end_headers()
        with open(self.BASE_DIR / 'public' / 'file.pdf', 'rb') as fstream:
            self.wfile.write(fstream.read())
