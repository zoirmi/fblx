import uuid
import falcon
#import json
#import logging

class HandleRequest(object):
    def on_post(self, req, resp):
        token = req.get_header('X-Auth-Token',required=True)
        if uuid.UUID(token).int % 2:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

app = falcon.API()

app.add_route('/check_status', HandleRequest())

# Useful for debugging problems in API, it works with pdb
if __name__ == '__main__':
    from wsgiref import simple_server  # NOQA
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
