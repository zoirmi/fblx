# -*- coding: utf-8 -*-
"""
This script is checking if IP exists on Redis DenyList
"""

import falcon
from wsgiref import simple_server
import redis
import logging
from datetime import datetime
import argparse
import sys


def main():
    args = parse_args()
    log_filename = str.format('logs/hitDenyList_{}.log', datetime.now().strftime('%Y-%m-%d_%H%M'))
    logging.basicConfig(filename=log_filename,
                        format="%(asctime)s.%(msecs)03d %(levelname)s>  %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        level=logging.INFO)
    logging.info("Session started")

    logging.info("Verifying Redis connectivity... ")
    logging.info("Starting hitDenyList server on {0}:{1}".format(args.webserver_ip, args.webserver_port))
    try:
        app = falcon.API()
        app.add_route('/check_status', RequestHandler(redis_ip=args.redis_ip, redis_port=args.redis_port,
                                                      redis_db=args.redis_db_num, ws_ip=args.webserver_ip,
                                                      ws_port=args.webserver_port))
        httpd = simple_server.make_server(args.webserver_ip, args.webserver_port, app)
        httpd.serve_forever()
    except:
        logging.error("Failed to start server. ")
        sys.exit(2)


class RequestHandler(object):
    def __init__(self, redis_ip, redis_port, redis_db, ws_ip, ws_port):
        connection_string = ([redis_ip, redis_port, redis_db])
        logging.info("Attempting to connect to :{}".format(connection_string))
        self.connection = redis.Redis(connection_string)

        a = 5


    def on_post(self, req, resp,rCon):
        token = req.get_header('X-Real-IP', required=True)
        # try to get token from redis

    def connect_to_redis(ip,port):
        try:
            connect = redis.Redis(host=ip, port=port, db=0)
            logging.info("Redis server is available")
            return connect
        except:
            logging.error("Failed to connect to Redis. ")
            sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description='Hit Redis DenyList')
    parser.add_argument('-ri', '--redis-ip',
                        dest='redis_ip',
                        default='127.0.0.1',
                        help='Redis server IP')
    parser.add_argument('-rp', '--redis-port',
                        dest='redis_port',
                        default='6379',
                        help='Redis server port')
    parser.add_argument('-rdb', '--redis-db',
                        dest='redis_db_num',
                        default='0',
                        help='Redis DB number')
    parser.add_argument('-wi', '--webserver-ip',
                        dest='webserver_ip',
                        default='127.0.0.1',
                        help='Local web server IP')
    parser.add_argument('-wp', '--webserver-port',
                        dest='webserver_port',
                        default='7000',
                        help='Local web server port')
    result = parser.parse_args()
    return result


if __name__ == '__main__':
    main()
