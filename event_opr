#!/bin/env python

import sys
import requests
import json
import math
import numpy as np
import operator


def main():
    """
    here is the formula used to calculate oprs:

    L * o = r
    L   len(matches) x len(teams)
        a matrix containing which teams are participating in which match
    o   len(teams) x 1
        a matrix containing the opr of each team
    r   len(matches) x 1
        a matrix containing the results of each match
    """

    # configuration
    event = sys.argv[1]
    print("event:", event)
    api_key = get_api_key("config.json")

    # retrieve event data

    matches_url = get_url(api_key, event, "matches")
    matches = requests.get(matches_url).json()
    matches = filter_matches(matches)
    match_stats = get_match_stats(matches)
    # printj(match_stats)

    # find L

    teams_url = get_url(api_key, event, "teams/simple")
    teams = requests.get(teams_url).json()
    teams_numbers = sorted(team["team_number"] for team in teams)

    L = get_l(match_stats, teams_numbers)

    # verify L
    # for i in range(len(L)):
    #     indices = [i for (i, e) in enumerate(L.tolist()[i]) if e == 1]
    #     for index in indices:
    #         print(teams_numbers[index], end=", ")
    #     print()

    # find results

    results = get_match_results(match_stats)
    results = parse_match_results(results)

    # verify results
    # print(results)

    # opr calculation

    oprs, error = get_oprs(L, results, teams_numbers)
    # pretty print the oprs
    pp_oprs(oprs)
    # print the error
    print("\nerror:", math.sqrt(error))


def pp_oprs(oprs):
    for (team, opr) in sorted(oprs.items(), key=operator.itemgetter(1), reverse=True):
        print(f"{team}\t{opr}")


def get_oprs(L, results, teams):
    response = np.linalg.lstsq(L, results, rcond=None)
    oprs = response[0]
    return {k[0]: k[1] for k in zip(teams, oprs)}, response[1]


def parse_match_results(results):
    return np.array([result[1] for result in sorted(results.items())]).T


def get_match_results(match_stats):
    return {number: match["score"] for (number, match) in match_stats.items()}


def get_l(match_stats, teams_numbers):
    return np.array(
        [
            [int(team in match["teams"]) for team in teams_numbers]
            for (match_number, match) in sorted(match_stats.items())
        ]
    )


def get_match_stats(matches):
    return {
        remap_match_number(match["match_number"], alliance): get_alliance_stats(
            match, alliance
        )
        for match in matches
        for alliance in ["red", "blue"]
    }


def remap_match_number(number, alliance):
    """
    since we are doubling the number of matches we look at,
    we assign matches in an alternating red, blue scheme
    ex: 1red, 1blue, 2red, 2blue...
    """
    if alliance == "red":
        return 2 * number - 1
    if alliance == "blue":
        return 2 * number
    raise ValueError("alliance must be either red or blue")


def get_alliance_stats(match, alliance):

    numbers = [int(key[3:]) for key in match["alliances"][alliance]["team_keys"]]
    return {"teams": numbers, "score": match["alliances"][alliance]["score"]}


def filter_matches(matches):
    """
    we only consider matches:
    - that are qualification matches
    - that have ended
    """
    return (
        match
        for match in matches
        if match["comp_level"] == "qm" and not not match["winning_alliance"]
    )


def get_data(url):
    return requests.get(url).json()


def get_url(api_key, event, endpoint):
    base_url = "https://www.thebluealliance.com/api/v3"
    call = f"event/{event}/{endpoint}"
    url = f"{base_url}/{call}?X-TBA-Auth-Key={api_key}"
    return url


def printj(data):
    print(json.dumps(data, indent=4, sort_keys=True))


def get_api_key(file):
    with open(file, "r") as f:
        return json.load(f)["api_key"]


if __name__ == "__main__":
    main()
