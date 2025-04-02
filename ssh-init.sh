#!/bin/bash

eval "$(ssh-agent -s)"

if [ -f ~/.ssh/aude ]; then
  ssh-add ~/.ssh/audessh
else
  echo "SSH key ~/.ssh/aude not found."
fi
