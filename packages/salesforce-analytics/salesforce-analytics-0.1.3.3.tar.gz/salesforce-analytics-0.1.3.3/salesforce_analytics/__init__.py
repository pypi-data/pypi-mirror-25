#!/usr/bin/env python
""" This is a docstring!
"""
import json
import datetime
from dateutil import parser

def set_json_compliant_name(salesforce_field):
    name = salesforce_field[:1].lower() + salesforce_field[1:]
    name = name.replace('__c', '')
    name = name.replace('_', '')
    return name


class SalesForceAnalytics(object):
    """SalesForce Analytics
    """
    def __init__(self, tickets):
        """Init
        """
        self.trend_topics = ['days', 'weeks', 'months', 'years']
        self.tickets = json.loads(tickets)
        self.dataset = {}
        self.count = {}
        self.trend = {}
        self.mtc_time = {}
        self.mtc_counts = {}
        self.mtc = {}
        self.prepare_analytics()

    def __build_counts(self):
        for key in self.tickets[0].keys():
            if 'attribute' not in key:
                self.count.update({set_json_compliant_name(key): {}})
        return self.count

    def __build_trends(self):
        for key in self.trend_topics:
            self.trend.update({set_json_compliant_name(key): {}})
        return self.trend

    def __build_dataset(self):
        self.dataset.update({'count': self.count})
        self.dataset.update({'trend': self.trend})
        self.dataset.update({'mtc': self.mtc})

    def __add_key(self, key):
        if key not in self.count:
            self.count[set_json_compliant_name(key)] = {}

    def __build_priority(self):
        for priority in ['1', '2', '3']:
            self.count['priority'].update({priority: 0})

    def __set_count_keys(self, key, value):
        """ See if the count contains the value, if not, create key with a
        value of 0"""
        if value not in self.count[set_json_compliant_name(key)]:
            self.count[set_json_compliant_name(key)][value] = 0
        self.count[set_json_compliant_name(key)][value] += 1

    def __set_mtc_times(self, key, value, ticket):
        name = set_json_compliant_name(key)
        if name not in self.mtc_time:
            self.mtc_time.update({name: {}})
        if value not in self.mtc_time:
            self.mtc_time[name].update({value: {}})

    def __set_dates(self, created_date_timestamp):
        timestamp = parser.parse(
            created_date_timestamp).strftime('%A : %U : %B : %Y').split(' : ')
        self.weekday = timestamp[0]
        self.week = timestamp[1]
        self.month = timestamp[2]
        self.year = timestamp[3]

    def __calculate_mean_time_to_close(self):
        for category in self.mtc_counts:
            calculation = 0
            for date in self.mtc_counts[category]:
                try:
                    calculation += date
                except TypeError:
                    calculation = date
            mtc = calculation / len(self.mtc_counts[category])
            self.mtc.update({category: str(mtc)})

    def get_weekday(self):
        return self.weekday

    def get_week(self):
        return self.week

    def get_month(self):
        return self.month

    def get_year(self):
        return self.year

    def describe_count(self, key, value):
        """Method used for gathering the count of each field returned from
        saleforce.
        VAR :: key :: This is a SalesForce field within the ticket
        VAR :: value :: The value of the SalesForce Field
        """
        key = set_json_compliant_name(key)
        if not 'attribute' in key:
            try:
                # This will try and execute against a custom method for
                # given fields.
                getattr(self, 'count_'+key.lower())(value)
            except AttributeError:
                # If nothing special needs to happen when counting the
                # fields, default to a default counter
                self.default_counter(salesforce_field=key, value=value)

    def describe_trend(self, created_date):
        self.__set_dates(created_date_timestamp=created_date)
        for trend in ['day', 'week', 'month', 'year']:
            try:
                getattr(self, 'trend_'+trend)()
            except AttributeError:
                pass

    def describe_dataset(self):
        return self.dataset

    def prepare_analytics(self):
        """Prepare the count by building the keys and setting them as a dict.
        Also excuting the build priority count"""
        #self.keys = self.__build_counts()
        #for key in self.keys:
        #    self.count.update({key: {}})
        self.__build_counts()
        self.__build_trends()
        self.__build_priority()

    def iterate_tickets(self):
        """Iterate through the list of tickets and begin building analytics
        against the returned data from SalesForce"""
        for ticket in self.tickets:
            for key, value in ticket.iteritems():
                if isinstance(value, int):
                    value=str(value)
                self.describe_count(key=key, value=value)
                if 'CreatedDate' in key:
                    self.describe_trend(created_date=value)
            if 'Closed' in ticket['Status']:
                self.mean_time_to_close("total", ticket)
        self.__calculate_mean_time_to_close()
        self.__build_dataset()
        return self.dataset

    def count_priority(self, priority):
        self.count['priority'][str(priority)] += 1

    def default_counter(self, salesforce_field, value):
        self.__set_count_keys(salesforce_field, value)

    def mean_time_to_close(self, key, ticket):
        if ticket['LastModifiedDate']:
            opened_date = datetime.datetime.strptime(ticket['CreatedDate'][:19], '%Y-%m-%dT%H:%M:%S')
            closed_date = datetime.datetime.strptime(ticket['LastModifiedDate'][:19], '%Y-%m-%dT%H:%M:%S')
            time_to_close = closed_date-opened_date
            if key not in self.mtc_counts:
                self.mtc_counts.update({key: []})
            self.mtc_counts[key].append(time_to_close)

    def count_handoff(self, handoff):
        if isinstance(self.count['handoff'], dict):
            self.count['handoff'] = 0
        if handoff:
            self.count['handoff'] += 1

    def count_owner(self, owner):
        self.__set_count_keys('owner', owner['Name'])

    def count_lastmodifieddate(self, value):
        """We want to ignore last modified date being added to counts"""
        pass

    def count_createddate(self, value):
        """We want to ignore created date being added to counts"""
        pass

    def count_subject(self, subject):
        """From the Subject field, parse the string and determine where in
        compliance this fits.  For legacy, discover if its legacy complaince"""
        self.__add_key('compliance')
        if not subject:
            subject = "NO_SUBJECT_FILLED"
        if 'Compliance Drop' in subject:
            if 'failing' in subject:
                compliance_reason = subject.split('failing')[1]
            else:
                compliance_reason = 'old_compliance'
            self.__set_count_keys("compliance", compliance_reason)

        if 'Patching Notification' in subject:
            self.__set_count_keys("compliance", 'patching')

    def count_compliance(self, subject):
        pass

    # All trends are repeating...refactor this

    def trend_day(self):
        """Create trend by day of week"""
        day = self.get_weekday()
        if day not in self.trend['days']:
            self.trend['days'].update({day: 0})
        self.trend['days'][day] += 1

    def trend_month(self):
        """Create trend by month"""
        month = self.get_month()
        if month not in self.trend['months']:
            self.trend['months'].update({month: 0})
        self.trend['months'][month] += 1

    def trend_week(self):
        """create trend by week"""
        week = self.get_week()
        if week not in self.trend['weeks']:
            self.trend['weeks'].update({week: 0})
        self.trend['weeks'][week] += 1

    def trend_year(self):
        """create trend by year"""
        year = self.get_year()
        if year not in self.trend['years']:
            self.trend['years'].update({year: 0})
        self.trend['years'][year] += 1

    def run(self):
        self.results = self.iterate_tickets()
        return self.results
