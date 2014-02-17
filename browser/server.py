# -*- coding: utf-8 -*-
"""
Un serveur qui suit le modèle MVC, avec un Controller et un Router.
"""

import re
import BaseHTTPServer
import os.path
import glob
import sys
from django.template import Context
from django.template import loader
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

browser_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(browser_dir)
data_dir = os.path.join(app_dir, 'data')

sys.path.append(os.path.join(browser_dir, 'entities'))

from document import Document
from topic import Topic

settings.configure(TEMPLATE_DIRS=(os.path.join(browser_dir, "templates"),))

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
        #le chemin vers la base de données
        self.__database_path = glob.glob(os.path.join(data_dir,'*.db'))[0]
        
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
        try:
            engine = create_engine('sqlite:///' + self.__database_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            topics = [topic.get_related_words() for topic in session.query(Topic)]
        except:
            raise IOError('Impossible de se connecter à la base de données')
        
        self.send_headers()
        template = loader.get_template('voir_topics.html')
        context = Context({'topics' : topics})
        self.__server.wfile.write(template.render(context))
              
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