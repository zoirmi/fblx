# -*- coding: utf-8 -*-
"""
This script is checking if IP exists on Redis DenyList
"""

import falcon
from wsgiref import simple_server
import redis
import logging
from datetime import datetime


REDIS_IP = '127.0.0.1'
REDIS_PORT = '6379'
LSNR_IP = '127.0.0.1'
LSNR_PORT = 7000


def main():
    log_filename = str.format('logs\hitDenyList_{}.log', datetime.now().strftime('%Y-%m-%d_%H%M'))
    logging.basicConfig(filename=log_filename,
                        format="%(asctime)s.%(msecs)03d %(levelname)s>  %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        level=logging.INFO)
    logging.info("Session started")
    logging.info("Verifying Redis connectivity... ")
    redisConnectivity(REDIS_IP,REDIS_PORT)
    logging.info("Starting hitDenyList server on {0}:{1}".format(LSNR_IP, LSNR_PORT))
    try:
        app = falcon.API()
        app.add_route('/check_status', HandleRequest())
        httpd = simple_server.make_server(LSNR_IP, LSNR_PORT, app)
        httpd.serve_forever()
    except:
        logging.error("Failed to start server. ")
        sys.exit(2)


class HandleRequest(object):
    def on_post(self, req, resp,rCon):
        token = req.get_header('X-Real-IP', required=True)
        # try to get token from redis


def redisConnectivity(ip,port):
    try:
        connect = redis.Redis(host=ip, port=port, db=0)
        logging.info("Redis server is available")
        return connect
    except:
        logging.error("Failed to connect to Redis. ")
        sys.exit(1)


if __name__ == '__main__':
    main()
