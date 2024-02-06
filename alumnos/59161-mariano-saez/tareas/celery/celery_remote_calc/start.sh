#!/bin/bash

celery -A calc_config worker --detach --loglevel=INFO
sudo docker run -d -p 6379:6379 redis