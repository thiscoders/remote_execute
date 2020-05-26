#!/usr/bin/env bash

PID=$(pgrep -f 'python3 app.py')
if [ -z "$PID" ]; then
  echo 'file server is not running!'
else
  echo 'file server is running, killing...'
  kill -9 "$PID"
  echo 'file server has been killed.'
fi
