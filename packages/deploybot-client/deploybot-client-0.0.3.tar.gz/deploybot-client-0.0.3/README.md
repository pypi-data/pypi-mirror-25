# Deploybot Client

[![Build Status](https://travis-ci.org/mrprompt/deploybot-client.svg?branch=master)](https://travis-ci.org/mrprompt/deploybot-client)
[![Code Climate](https://codeclimate.com/github/mrprompt/deploybot-client/badges/gpa.svg)](https://codeclimate.com/github/mrprompt/deploybot-client)
[![Test Coverage](https://codeclimate.com/github/mrprompt/deploybot-client/badges/coverage.svg)](https://codeclimate.com/github/mrprompt/deploybot-client/coverage)
[![Issue Count](https://codeclimate.com/github/mrprompt/deploybot-client/badges/issue_count.svg)](https://codeclimate.com/github/mrprompt/deploybot-client)
[![GitHub issues](https://img.shields.io/github/issues/mrprompt/deploybot-client.svg)](https://github.com/mrprompt/deploybot-client/issues)
[![GitHub stars](https://img.shields.io/github/stars/mrprompt/deploybot-client.svg)](https://github.com/mrprompt/deploybot-client/stargazers)
[![GitHub license](https://img.shields.io/badge/license-AGPL-blue.svg)](https://raw.githubusercontent.com/mrprompt/deploybot-client/master/LICENSE)

A library to access [Deploybot](https://www.deploybot.com) API.

## Install

```
pip install deploybot-client
```

## Usage

### Client

Client is the main library, this is responsible to make and receive requests from API.

The first step, is instantiate to your application using your account name and API token.

```python
from deploybot.client import Client
import os

account = os.environ.get('DEPLOYBOT_ACCOUNT')
token = os.environ.get('DEPLOYBOT_TOKEN')

client = Client(account, token)
```

This client return methods GET and POST to use Deploybot API.


## Testing

```
python setup.py test
```