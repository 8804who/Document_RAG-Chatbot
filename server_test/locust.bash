#!/bin/bash

locust -f locustfile.py \
  --web-port 10005 \
  --web-host 0.0.0.0