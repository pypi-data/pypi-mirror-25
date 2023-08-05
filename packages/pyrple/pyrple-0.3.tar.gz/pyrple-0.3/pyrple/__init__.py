#!/usr/bin/env python

# Dependencies
import requests
import hmac
from datetime import datetime
import hashlib
import json

class purple(object):

    # Class attributes
    base_url = "https://purpleportal.net"

    # Instance attributes
    def __init__(self, public_key, private_key):

        self.public_key = public_key
        self.private_key = private_key

        # The request time has to be defined when the instance is created because the datetime is used in both
        # the plaintext API request and the hashed signature, and the values have to match.
        self.__request_time = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        self.__request_string = ""
        self.__request_url = ""

    def __generate_signature(self):

        line_1 = "application/json\n"
        line_2 = "purpleportal.net\n"
        line_3 = self.__request_string
        line_4 = self.__request_time

        signature = "{}{}{}\n{}\n\n".format(line_1, line_2, line_3, line_4)

        return signature

    def __generate_hash(self):

        # String must be converted to bytes for Python 3 compatibility.
        pkey_bytes = bytes(self.private_key, "latin-1")
        sig_bytes = bytes(self.__generate_signature(), "latin-1")

        hash_message = hmac.new(
            pkey_bytes,
            sig_bytes,
            hashlib.sha256
        ).hexdigest()

        return hash_message

    def __generate_header(self):

        header = {"Host":"purpleportal.net",
                  "Accept":"*/*",
                  "Content-Type":"application/json",
                  "Content-Length":"0",
                  "Date":self.__request_time,
                  "X-API-Authorization":self.public_key+":"+self.__generate_hash()}

        return header

    def venues_json(self):

        """Returns a json object containing full details of all venues in the Purple instance.
        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venues"

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the GET request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        venues_json = get_request.json()
        return venues_json

    def venues(self):

        """Returns a simple dictionary with the format:
            {"venue name":"venue unique id"}"""

        venue_json = self.venues_json()

        if venue_json["success"] == False:
            return venue_json
        names = [venue_json["data"]["venues"][venue]["name"] for venue in range(len(venue_json["data"]["venues"]))]
        ids = [venue_json["data"]["venues"][venue]["id"] for venue in range(len(venue_json["data"]["venues"]))]
        venue_dict = {}
        for venue in range(len(venue_json["data"]["venues"])):
            venue_dict.update({names[venue]: ids[venue]})

        return venue_dict

    def visitor_json(self, venue, date_from = "", date_to = ""):

        """Returns a dictionary of all visitors to a specified venue.
        To obtain the unique venue IDs run .venues() first to get a full list.
        If no dates are passed as arguments default query is for visitors who are online now.

        Args:

            * venue: unique ID representing the venue, e.g. 12324.
            * date_from: optional argument specifying start of date range to be queried. Date format must be YYYYMMDD.
            * date_to: optional argument specifying end of date range to be queried. Date format must be YYYYMMDD.

        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/{}/visitors".format(venue)
        if date_from != "" and date_to != "":
            self.__request_string = "{}?from={}&to={}".format(self.__request_string, date_from, date_to)

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the GET request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        visitor_json = get_request.json()
        return visitor_json

    def visits_json(self, venue_id, user_id, date_from = "", date_to = ""):

        """Returns a dictionary of all visits that a specified visitor has made to a given venue.
        To obtain the unique venue IDs run .venues() first to get a full list.
        If no dates are passed as arguments the default query will return all visits that the
        visitor has made.

        Args:

            * venue_id: unique ID representing the venue, e.g. 12324.
            * user_id: unique ID representing a specific user.
            * date_from: optional argument specifying start of date range to be queried.
              Date format must be YYYYMMDD.
            * date_to: optional argument specifying end of date range to be queried.
              Date format must be YYYYMMDD.

        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/{}/visitor/{}".format(venue_id, user_id)
        if date_from != "" and date_to != "":
            self.__request_string = "{}?from={}&to={}".format(self.__request_string, date_from, date_to)

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the GET request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        visits_json = get_request.json()
        return visits_json

    def presence_json(self, venue_id, date = "", from_utc = "", to_utc = ""):

        """Returns a dictionary of associated or unassociated clients seen at the specified
        venue_id, including enhanced visitor info for any recognised clients. Defaults to
        the last hour, or can accept optional parameters date, or from_utc and to_utc.

        To obtain the unique venue IDs run .venues() first to get a full list.

        If date is provided, data will be returned for that date for a 24 hour period from
        midnight to midnight (UTC). More granular selections can be achieved by passing
        from_utc and to_utc instead, but queries are limited to a maximum of 24 hours. Any
        from_utc/to_utc that exceeds 24 hours will return an error.

        Args:

            * venue_id: unique ID representing the venue, e.g. 12324.
            * date: optional argument specifying date to query data from.
            * from_utc: optional argument specifying specific start time for data to be
              queried from. Date-time format must be YYYYMMDDHHMMSS in UTC.
            * to_utc: optional argument specifying specific end time for data to be
              queried from. Date-time format must be YYYYMMDDHHMMSS in UTC.

        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/{}/presence".format(venue_id)
        if date != "":
            self.__request_string = "{}?date={}".format(self.__request_string, date)

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the GET request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        presence_json = get_request.json()
        return presence_json

    def positioning_json(self, venue_id, from_utc = ""):

        """Returns a dictionary of associated or unassociated clients seen in a venue and
        a list of X/Y coordinates for each client including a floor and matching zones.
        Displays additional data for recognised clients. Returns exactly one hour of data,
        either the previous hour or an hour from a requested start time.

        To obtain the unique venue IDs run .venues() first to get a full list.

        Args:

            * venue_id: unique ID representing the venue, e.g. 12324.
            * from_utc: optional argument specifying specific start time for data to be
              queried from. Date-time format must be YYYYMMDDHHMMSS in UTC.

        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/{}/positioning".format(venue_id)
        if from_utc != "":
            self.__request_string = "{}?from={}".format(self.__request_string, from_utc)

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the GET request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        positioning_json = get_request.json()
        return positioning_json

    def unsubscribe(self, venue_id, user_id):

        """Unsubscribes the user from receiving future emails from the Portal.

        To obtain the unique venue IDs run .venues() first to get a full list, and run
        .visitor_json() to get user IDs.

        Args:

            * venue_id: unique ID representing the venue, e.g. 12324.
            * user_id: unique ID representing the user to unsubscribe.

        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/{}/visitor/{}/unsubscribe".format(venue_id, user_id)

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        unsubscribe_json = get_request.json()
        return unsubscribe_json

    def miscrosurveys(self):

        """Returns a complete list of available published MicroSurveys for the company.
        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/microsurveys"

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        miscrosurveys_json = get_request.json()
        return miscrosurveys_json

    def miscrosurvey_responses(self, microsurvey_id):

        """Returns a list of MicroSurvey responses for a specific MicroSurvey, using a
        MicroSurvey ID retrieved from the .miscrosurveys() method.
        """

        # Set the request variable.
        self.__request_string = "/api/company/v1/venue/microsurveys/{}".format(microsurvey_id)

        # Set the request url variable.
        self.__request_url = "{}{}".format(self.base_url, self.__request_string)

        # Make the request.
        get_request = requests.get(self.__request_url, headers = self.__generate_header())

        # Return the JSON.
        miscrosurvey_responses_json = get_request.json()
        return miscrosurvey_responses_json
