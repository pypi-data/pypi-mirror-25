#!/usr/bin/python

import json
import time
import logging

import requests

from mongoengine import connect
from mongoengine.errors import NotUniqueError

from geoservice.models import IPGeolocation


def save_all_to_db():
    """
    Saves all collection to the database
    """
    MAX_RECORD = 46998
    print "{0} Records to read and save".format(MAX_RECORD)
    MAX_OFFSET = 46950

    # BATCH = 1
    # CURRENT_OFFSET = 0
    # INCREMENT_BY = 50

    BATCH = 1
    CURRENT_OFFSET = 0
    INCREMENT_BY = 50

    TAKE = 50

    URL_MASK = "http://31.222.174.143/UnnApi/api/StudentList?offset={0}&take={1}"

    HEADERS = {"API_KEY": "03376305151418054414015"}
    connect("SmallTennDB")

    start_time = time.time()

    while CURRENT_OFFSET <= MAX_OFFSET:

        #: set up logging
        logging.basicConfig(filename="error.log", level=logging.DEBUG)

        url = URL_MASK.format(CURRENT_OFFSET, TAKE)

        failed = True
        count = 0

        while failed:
            print "HTTP Request: Trying batch {} of {} items".format(BATCH, 50)
            response = requests.get(url, headers=HEADERS)
            count += 1
            failed = not response.ok

            if count > 10:
                break

        if response.ok:
            content = json.loads(response.content)
            if not content:
                print "API Traversal complete"
                break

            origin = 0
            destination = len(content)
            while origin < destination:
                student = Student()
                data = content[origin]
                student.load_data(data)
                try:
                    student.save()
                except NotUniqueError:
                    text = "Could not save: Student {0}, {1} with id - {2}"
                    message = text.format(student.surname, student.first_name, student.external_id)
                    logging.error(message)
                origin += 1
        else:
            print "###: Tried to high skies 10 times but could not read the API at this time"
        BATCH += 1
        CURRENT_OFFSET += INCREMENT_BY

    print "-------------: ENTIRE DATABASE SAVED: In {0} seconds".format(time.time() - start_time)


if __name__ == "__main__":
    save_all_to_db()
