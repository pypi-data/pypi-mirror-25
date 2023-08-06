import sys
import os

if sys.argv[1] == "server":
    from wsgiref.simple_server import make_server
    from app import application
    with make_server("", 8023, application) as server:
        print("Serving on port 8023...")
        server.serve_forever()
elif sys.argv[1] == "start":
    lines = "\n\n".join([
     "from firebolt.wsgi import create_application",
     "application = create_application()"
    ])
    name = sys.argv[2]
    os.mkdir(name)
    with open("{}/app.py".format(name), "w") as f:
        f.write(lines)
