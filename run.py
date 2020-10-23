#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import requests
#import json


DEBUG = True
# Декоратор для логов 
def log( f ):
    def new_func( *args, **kwargs ):
        if DEBUG:
            logging.info( "Вызов #%s#( #%s#, #%s# )"%( f.__name__, args, kwargs) )
        r = f( *args, **kwargs )
        if DEBUG:
            logging.info( "Возврат:#%s#"%( r ) )
        return( r )
    return new_func

class Api:
    ADDRESS = 'https://ismp.crpt.ru/api/v3/auth/cert/key'
    
    
    @log
    def __init__( self ):
        self.command = {'get_question':self.get_question}

    @log
    def get_question( self, data ):
        res = requests.get( self.ADDRESS )
        if res.status_code == 200:
            r = res.json() 
            self.uuid = r['uuid']
            self.data = r['data']
            if 'filename' in data:
                with open( data['filename'], 'wt' ) as f:
                    f.write( r['data'] )
            result = {'Result':'OK', 'data':r}
        else:
            result = {'Result':'ERROR'}
        return result

    def do(self, cmd, data):
        if cmd in self.command:
            result = self.command[cmd]( data ) 
            
        else:
            result = { 'Result':'ERROR', 'data':'Unknown command' }
        return result

if __name__ == "__main__":
    
    logging.basicConfig( level = logging.INFO )
    logging.info('Запуск')
    api = Api()
    print( api.do('get_question', {'filename':'out.txt'}) )
