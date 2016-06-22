#!/bin/bash

ps -ef | grep python | grep index.py | awk '{print $2}'| xargs kill &>> /dev/null
python index.py &> server.log &