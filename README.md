# Information
This package to connect TradOvate API
## Installation
```bash

# Create an isolated Python virtual environment
pip3 install virtualenv
virtualenv ./virtualenv --python=$(which python3)

# Activate the virtualenv
# IMPORTANT: it needs to be activated every time before you run
. virtualenv/bin/activate

# Install Python requirements
pip install -r requirements.txt

# Install cointrol-*
pip install -e .

# Set param enviroment env.env
TO_ENV=DEMO
TO_NAME=Your credentials here
TO_PASSWORD=Your credentials here
TO_APPID="Sample App"
TO_CID=0
TO_SEC=Your API secret here

# OR export in terminal to test local
export TO_ENV=DEMO
export TO_NAME=Your credentials here
export TO_PASSWORD=Your credentials here
export TO_APPID="Sample App"
export TO_CID=0
export TO_SEC=Your API secret here

# run test
python -m test

# run test bot trading demo
python -m es5m_test

# Demo logic on Trading View
Please refer to repo https://github.com/dearvn/trading-futures-tradingview-script to view my logic to trade Futures on Tradovate
