#!/bin/env python

import requests
import json
import math

import _tkinter

from matplotlib import pyplot as plt

import numpy as np
import scipy.stats as stats


def main():

    api_key = get_api_key("config.json")
    event = "2019cc"

    matches_url = get_matches_url(api_key, event)
    matches = get_data(matches_url)

    matches = filter_matches(matches)
    matches = parse_matches(matches)

    figure = plt.figure()

    plot(matches, figure, 211, "blue")
    plot(matches, figure, 212, "red")

    plt.show()


def plot(matches, figure, axis, color):

    matches = [match[color] for match in matches]
    num_bins = round(math.sqrt(len(matches)))
    subplot = figure.add_subplot(axis)
    n, bins, patches = subplot.hist(matches, num_bins, facecolor=color)


def parse_matches(matches):
    return [
        {
            "blue": match["score_breakdown"]["blue"]["totalPoints"],
            "red": match["score_breakdown"]["red"]["totalPoints"],
        }
        for match in matches
    ]


def filter_matches(matches):
    return [match for match in matches if not not match["winning_alliance"]]


def get_data(url):
    return requests.get(url).json()


def get_matches_url(api_key, event):
    base_url = "https://www.thebluealliance.com/api/v3"
    call = f"event/{event}/matches"
    url = f"{base_url}/{call}?X-TBA-Auth-Key={api_key}"
    return url


def get_api_key(file):
    with open(file, "r") as f:
        return json.load(f)["api_key"]


def printj(data):
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
