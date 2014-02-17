# -*- coding: utf-8 -*-
"""
Un serveur qui suit le modèle MVC, avec un Controller et un Router.
"""

import re
import BaseHTTPServer
import os.path
from django.template import Template, Context
from django.template import loader
from django.conf import settings

app_path = os.path.abspath(os.path.dirname(__file__))
settings.configure(TEMPLATE_DIRS=(os.path.join(app_path, "templates"),))

TEMPLATE_DIRS = getattr(settings, "TEMPLATE_DIRS", None)
    
class Router():
    
    def __init__(self, server, controller):
        self.__routes = []
        self.__server = server
        self.__controller = controller
        
    def add_route(self, regexp, action):
        self.__routes.append({'regexp' : regexp, 'action' : action})
        
    def route(self, path):
        """
        Analyse path pour déterminer l'action à appeler.
        """
        
        for route in self.__routes:
            m = re.search(route['regexp'], path)
            if m: #path correspond à une route
                args = m.groupdict()
                getattr(self.__controller, route['action'])(args)
                return 
            
        self.__server.send_response(404)
        self.__server.end_headers()
        
class Controller():   
    
    def __init__(self, server):
        self.__server = server
        
    @property
    def server(self):
        return self.__server
    #Peut être qu'on se passer de ça, et juste accéder au serveur par self.server ?
    
    def send_headers(self):
        self.__server.send_response(200)  
        self.__server.send_header('Content-type', 'text/html')  
        self.__server.end_headers()
        
    #Quand on route une url, on peut avoir des arguments : par exemple,
    #si url = /topics/7, on veut pouvoir récupérer le 7. Le router appelle donc
    #systématiquement actions(args). Les actions qui n'ont pas besoin d'argument
    # prennent donc quand même args en argument (qui sera vide). 
    #Est-ce gênant/nécessaire ?
    def voir_topics(self, args): 
        self.send_headers()
        t = loader.get_template('voir_topics.html')
        self.__server.wfile.write(t.render(Context()))
              
class HabeasCorpusRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def __init__(self, request, client_adress, server):
            
        routes = [
                  {'regexp' : r'/topics', 'action' : 'voir_topics'}
                  ]
        
        self.__router = Router(self, Controller(self))
        for route in routes:
            self.__router.add_route(route['regexp'], route['action'])
            
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_adress, server) 
        
    def do_GET(self):  
        self.__router.route(self.path)  
                
if __name__ == '__main__':
    adress = ('', 9000)
    httpd = BaseHTTPServer.HTTPServer(adress, HabeasCorpusRequestHandler)
    httpd.serve_forever()