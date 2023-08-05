[![Build Status](https://travis-ci.com/iamjohnnym/salesforce-analytics.svg?token=jwXMHmbEfJmrxyLSfYtH&branch=master)](https://travis-ci.com/iamjohnnym/salesforce-analytics)
[![Coverage Status](https://coveralls.io/repos/github/iamjohnnym/salesforce-analytics/badge.svg?branch=master)](https://coveralls.io/github/iamjohnnym/salesforce-analytics?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/699af2d695f94865bacfd770c9ddfd90)](https://www.codacy.com/app/iamjohnnym/salesforce-analytics?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=iamjohnnym/salesforce-analytics&amp;utm_campaign=Badge_Grade)

# SalesForce Analytics
===================

## Overview

Python library to injest SalesForce Cases from SFDC.  From the injested data,
gather statistics on trends over time and current standings of tickets.  

## Installation

From PyPi

```
pip install salesforce-analytics
```

From GitHub

```
git clone git@github.com:iamjohnnym/salesforce-analytics.git
```

## Usage

### Invocation


```
## You must pass in a SFDC Object for a series of cases to build the proper
## analytics.

import pprint
from salesforce_analytics import SalesForceAnalytics


analytics = SalesForceAnalytics(
    tickets=tickets
    ).run()

pprint.pprint(analytics)

{'count': {u'accountNumber': {'100': 75,
                              '101': 71,
                              '102': 56,
                              '...',
                              '148': 55,
                              '149': 61,
                              '150': 59},
           'compliance': {'old_compliance': 659},
           u'createdDate': {},
           u'handoff': 3182,
           u'lastModifiedDate': {},
           u'owner': {u'Abbott Alvarez': 1,
                      u'Abbott Carr': 1,
                      u'Abby Stevenson': 1,
                      '....',
                      u'Zelma Morgan': 1,
                      u'Zimmerman Merrill': 1},
           u'priority': {'1': 1065, '2': 1075, '3': 1042},
           u'status': {u'Closed': 749,
                       u'In-Progress': 829,
                       u'New': 782,
                       u'Waiting-Customer': 822},
           u'subject': {},
           u'typev2': {u'Change Request': 527,
                       u'Compliance': 532,
                       u'Networking': 525,
                       u'Other': 543,
                       u'System': 531,
                       u'System / Environment Build': 524}},
 'mtc': {'total': datetime.timedelta(372, 58373, 305740)},
 'trend': {'days': {'Friday': 458,
                    'Monday': 450,
                    'Saturday': 457,
                    'Sunday': 442,
                    'Thursday': 462,
                    'Tuesday': 449,
                    'Wednesday': 464},
           'months': {'April': 241,
                      'August': 281,
                      'December': 275,
                      'February': 259,
                      'January': 258,
                      'July': 277,
                      'June': 270,
                      'March': 291,
                      'May': 275,
                      'November': 231,
                      'October': 260,
                      'September': 264},
           'weeks': {'00': 14,
                     '01': 58,
                     '02': 55,
                     '03': 73,
                     '04': 52,
                     '05': 56,
                     '06': 62,
                     '07': 64,
                     '08': 63,
                     '09': 63,
                     '10': 74,
                     '11': 73,
                     '12': 66,
                     '13': 46,
                     '14': 49,
                     '15': 64,
                     '36': 62,
                     '...',
                     '37': 71,
                     '38': 56,
                     '39': 70,
                     '40': 56,
                     '41': 54,
                     '42': 65,
                     '43': 54,
                     '44': 66,
                     '45': 41,
                     '46': 66,
                     '47': 54,
                     '48': 48,
                     '49': 60,
                     '50': 56,
                     '51': 72,
                     '52': 64},
           'years': {'2016': 3182}}}
          
```

### Testing
```
pip install nose
cd ${PATH}/salesforce-analytics
nosetests -v
```

## Features

* Conversion of SFDC field name to JSON Standard of camelCase
* Trends by CreatedDate
  * Days
  * Weeks
  * Months
  * Years
* Counts
  * Priority
  * Handoffs
  * Status
  * Compliance
  * Security
  * Mean Time to Close

## Purpose

Libary used with API Gateway and Lambda function to track analytics on
support based KPI's in real time, for teams, individuals, and by time frame

## Contribute

Do your thing, make some MR's.  

## Report Bugs

Please toss up any bugs here:

[Issues](https://github.com/iamjohnnym/salesforce-analytics/issues)
