#/bin/bash

# create a virtual env
python3 -m venv ./venv

# activate a new virtual env
source venv/bin/activate

# install all the required libs
pip install --no-cache-dir -r requirements.txt
