#!/usr/bin/env bash


cd code_path
exec_pull=$(git pull)
up_to_data="Already up to date."

if [[ $exec_pull =~ $up_to_data ]]; then
  echo "code already up to date."
else
  echo "upgrading..."
fi

