# POTENTIALLY SUPPORT MULTIPLE ENVIRONMENTS
from __future__ import absolute_import, division, print_function, unicode_literals

envs = {'local', 'dev', 'staging', 'production'}

ENVIRONMENT = 'production'
API_VERSION = 'v1.0'

LOCAL_ENDPOINT = 'http://localhost:8000'
BASE_URLS = {
    'production': 'https://api.amaas.com',
    'staging': 'https://api-staging.amaas.com',
    'dev': 'https://api-dev.amaas.com'
}

ENDPOINTS = {
    'asset_managers': 'assetmanager',
    'assets': 'asset',
    'books': 'book',
    'corporate_actions': 'corporateaction',
    'fundamentals': 'fundamental',
    'market_data': 'marketdata',
    'monitor': 'monitor',
    'parties': 'party',
    'transactions': 'transaction'
}

# Do not change this
COGNITO_REGION = 'ap-southeast-1'
COGNITO_POOL = 'ap-southeast-1_De6j7TWIB'
# This is not secret - it is just an identifier
COGNITO_CLIENT_ID = '2qk35mhjjpk165vssuqhqoi1lk'
