
def create_application():
    def application(environment, start_response):
        start_response(
         "200 OK", headers = [('Content-type', 'text/plain; charset=utf-8')]
        )
        return [b"Hello World!"]
    return application
