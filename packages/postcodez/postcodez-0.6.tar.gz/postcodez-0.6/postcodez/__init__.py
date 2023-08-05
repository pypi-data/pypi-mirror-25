#!/usr/bin/env python

# Dependencies
import re
from pandas import read_csv

# Postcode data
postcodes = read_csv("./ukpostcodes.csv")
postcodes.drop(labels = ["Unnamed: 0","id"], axis = 1, inplace=True)
london = read_csv("./london_boroughs.csv")

def postcodez(postcode):

    pc_dict = {"postcode_IN":postcode,
               "postcode_OUT":"",
               "latitude":"",
               "longitude":"",
               "london_borough":""}

    try:
        pc_check = str.lower(re.sub(r"\s+", "", postcode))

        if pc_check in postcodes["postcode_clean"].values:
            # Postcode has been found.
            pc_dict["postcode_IN"] = postcode
            pc_dict["postcode_OUT"] = postcodes[postcodes["postcode_clean"]==pc_check]["postcode"].values[0]
            pc_dict["latitude"] = postcodes[postcodes["postcode_clean"]==pc_check]["latitude"].values[0]
            pc_dict["longitude"] = postcodes[postcodes["postcode_clean"]==pc_check]["longitude"].values[0]

        if pc_check in london["postcode_clean"].values:
            # London postcode.
            pc_dict["london_borough"] = london[london["postcode_clean"]==pc_check]["London_Borough"].values[0]

        return pc_dict

    except:
        return pc_dict
