# callable - função(...), obj(...), (lambda)(..)
# environ, callback (default: start_response)
# return iteravel

def application(environ, start_reponse):
    # environ: as informações do request como variáveis de ambiente
    # passadas pelo servidor wsgi do próprio python

    # star_response: a função disponibilizada pelo wsgi server pra 
    # retornar os dados do response

    # montar o response
    status = "200 OK"
    headers = [("Content-type","text/html")]
    body = b"<strong>Hello World!!!</strong>"
    start_reponse(status, headers)
    return [body]

# if __name__=="__main__":  
#     from wsgiref.simple_server import make_server
#     server = make_server("0.0.0.0", 8000, application)
#     server.serve_forever()