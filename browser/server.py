# -*- coding: utf-8 -*-
"""
Un serveur qui suit le modèle MVC, avec un Controller et un Router.
"""

import re
import BaseHTTPServer
import os.path
import glob
import sys
import json
from django.template import Context
from django.template import loader
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import extract
from sqlalchemy.sql import func

browser_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(browser_dir, 'entities'))

from document import Document, DocumentTopic
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
        self.__database_path = glob.glob('*.db')[0]
        
    @property
    def server(self):
        return self.__server
    #Peut être qu'on se passer de ça, et juste accéder au serveur par self.server ?
    
    def send_headers(self):
        self.__server.send_response(200)  
        self.__server.send_header('Content-type', 'text/html;charset=UTF-8')  
        self.__server.end_headers()
        
    #Quand on route une url, on peut avoir des arguments : par exemple,
    #si url = /topics/7, on veut pouvoir récupérer le 7. Le router appelle donc
    #systématiquement actions(args). Les actions qui n'ont pas besoin d'argument
    # prennent donc quand même args en argument (qui sera vide). 
    #Est-ce gênant/nécessaire ?
    def words_cloud(self, args): 
        """
        Charge la page words_cloud.html.twig qui affiche un nuage contenant les mots
        représentatifs des topics du corpus.
        
        """

        try:
            engine = create_engine('sqlite:///' + self.__database_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            topics = session.query(Topic).all()
        except:
            raise IOError('Impossible de se connecter à la base de données')
        
        self.send_headers()
        template = loader.get_template('words_cloud.html.twig')
        words = [{'id_topic' : topic.id, 'weight' : topic.weight_in_corpus*word['weight_in_topic'],
                   'word' : word['word']} for topic in topics 
                 for word in topic.get_related_words(3)]
        context = Context({'words' : words})
        self.__server.wfile.write(template.render(context).encode('utf-8'))
        #Merci python 2 qui sait pas gérer unicode
        
    def voir_topics(self, args): 
        """
        Charge la page voir_topics.html.twig qui affiche la liste des topics du corpus
        
        """

        try:
            engine = create_engine('sqlite:///' + self.__database_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            topics = session.query(Topic).all()
        except:
            raise IOError('Impossible de se connecter à la base de données')
        
        self.send_headers()
        template = loader.get_template('voir_topics.html.twig')
        context = Context({'topics' : topics})
        self.__server.wfile.write(template.render(context).encode('utf-8'))
        #Merci python 2 qui sait pas gérer unicode
        
    def details_topic(self, args):
        """
        Charge la page details_topic.html.twig qui affiche les détails d'un topic donné
        
        :Parameters:
            -`args['id']` : l'id du topic dont on veut les détails
        """
        
        try:
            engine = create_engine('sqlite:///' + self.__database_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            
        except:
            raise IOError('Impossible de se connecter à la base de données')
            
        topic = session.query(Topic).\
                        filter(Topic.id == args['id']).\
                        one()

        related_documents = session.query(Document).\
                                join(Document.topics).\
                                join(DocumentTopic.topic).\
                                filter(Topic.id == args['id']).\
                                order_by(desc(DocumentTopic.weight_in_document)).\
                                limit(10).\
                                all()     
                                
        topic_history = session.query(func.sum(DocumentTopic.weight_in_document), 
                                      extract('year', Document.date).label('year')).\
                                join(Document).\
                                join(Topic).\
                                filter(Topic.id == args['id']).\
                                group_by("year").\
                                all()        
        
        topic_history = [{'value' : weight_in_corpus, 'date': year}
                          for weight_in_corpus, year in topic_history]       
        self.send_headers()
        template = loader.get_template('details_topic.html.twig')
        context = Context({'topic': topic,
                           'related_documents' : related_documents,
                           'topic_history' : json.dumps(topic_history)}
                          );
        self.__server.wfile.write(template.render(context).encode('utf-8'))
        
    def voir_article(self, args):
        try:
            engine = create_engine('sqlite:///' + self.__database_path, echo=True)
            Session = sessionmaker(bind=engine)
            session = Session()
            document = session.query(Document).\
                                     filter(Document.id == args['id']).\
                                     one()                        
            document_topics = document.topics[:3] #on affiche les 3 topics les plus significatifs
        except:
            raise IOError('Impossible de se connecter à la base de données')
        
        self.send_headers()
        template = loader.get_template('voir_article.html.twig')
        context = Context({'document' : document, 'document_topics' : document_topics})
        self.__server.wfile.write(template.render(context).encode('utf-8'))
        #Merci python 2 qui sait pas gérer unicode
        
class HabeasCorpusRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def __init__(self, request, client_adress, server):
            
        routes = [
                  {'regexp' : r'/topics/(?P<id>\d*)', 'action' : 'details_topic'},
                  {'regexp' : r'/topics$', 'action' : 'voir_topics'},
                  {'regexp' : r'/cloud', 'action' : 'words_cloud'},
                  {'regexp' : r'/articles/(?P<id>\d*)', 'action' : 'voir_article'}
                  ]
        
        self.__router = Router(self, Controller(self))
        for route in routes:
            self.__router.add_route(route['regexp'], route['action'])
            
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_adress, server) 
        
    def do_GET(self):  
        
        browser_dir = os.path.dirname(os.path.realpath(__file__))
        
        if self.path.endswith('.js'):
            js_file = self.path.lstrip('/')
            with open(os.path.join(browser_dir, js_file)) as js_file:
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.end_headers()
                self.wfile.write(js_file.read())
                
        elif self.path.endswith('.css'):
            css_file = self.path.lstrip('/')
            with open(os.path.join(browser_dir, css_file)) as css_file:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(css_file.read())

        elif self.path.endswith('.eot'):
            eot_file = self.path.lstrip('/')
            with open(os.path.join(browser_dir, eot_file)) as eot_file:
                self.send_response(200)
                self.send_header('Content-type', 'application/vnd.ms-fontobject')
                self.end_headers()
                self.wfile.write(eot_file.read())

        elif self.path.endswith('.svg'):
            svg_file = self.path.lstrip('/')
            with open(os.path.join(browser_dir, svg_file)) as svg_file:
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(svg_file.read())

        elif self.path.endswith('.woff'):
            woff_file = self.path.lstrip('/')
            with open(os.path.join(browser_dir, woff_file)) as woff_file:
                self.send_response(200)
                self.send_header('Content-type', 'application/font-woff')
                self.end_headers()
                self.wfile.write(woff_file.read())

            
        else:
            self.__router.route(self.path) 
                
if __name__ == '__main__':
    
    #Si la base de données n'existe pas, on stop
    database = glob.glob('*.db')
    if not database:
        raise IOError("Base de données introuvable dans le dossier %s" % (os.getcwd()))
    
    adress = ('', 9000)
    httpd = BaseHTTPServer.HTTPServer(adress, HabeasCorpusRequestHandler)

    print "Ouvrir la page http://localhost:9000/cloud dans un navigateur"
    
    httpd.serve_forever()
