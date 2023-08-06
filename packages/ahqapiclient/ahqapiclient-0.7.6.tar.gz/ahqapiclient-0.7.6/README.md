# AbuseHQ API Client

## About
**ahqapiclient** is a library which reflects the AbuseHQ API on client side.

## Usage

import Client from ahqapiclient

### Setup

endpoint = {
  "auth_method": "JWT",
  "auth_options": {
    "token": "<YOUR_API_KEY>"
  },
  "url": "https://<yourcompany>.abusehq.net/api/v1"
}

api_client = Client(endpoint)

### Usage

#### Get a case
case = api_client.case.get_case('case_id')

#### Perform a transition

api_client.case.trigger_transition('case_id', 'transition_id')
