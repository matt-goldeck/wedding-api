import csv
import io
from typing import List


def dicts_to_csv(dict_list: List[dict]):
    headers = [k for k in dict_list[0]]

    new_csvfile = io.StringIO()
    wr = csv.DictWriter(new_csvfile, fieldnames=headers)
    wr.writeheader()
    wr.writerows(dict_list)

    return new_csvfile


def rsvps_to_csv(rsvp_list):
    rsvp_dict_list = [rsvp.to_csv_dict() for rsvp in rsvp_list]
    return dicts_to_csv(rsvp_dict_list)
