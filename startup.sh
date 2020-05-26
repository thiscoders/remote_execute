#!/usr/bin/env bash

PID=$(pgrep -f 'python3 app.py')
if [ -z "$PID" ]; then
  nohup python3 app.py >/dev/null 2>&1 &
  echo 'file server started!'
else
  echo 'file server is running,please shutdown it!'
fi
