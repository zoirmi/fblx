FROM redis

RUN mkdir -p /redis_data && touch /redis_data/6379.log

COPY ./data/redis.conf /redis-data/redis.conf

CMD [ "redis-server", "/redis-data/redis.conf" ]

