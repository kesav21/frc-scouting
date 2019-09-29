#!/bin/env python

import requests
import json


def main():

    api_key = get_api_key("config.json")

    teams_url = get_teams_url(api_key)
    teams = get_data(teams_url)

    my_data = init_teams(team["key"] for team in teams)

    matches_url = get_matches_url(api_key)
    matches = get_data(matches_url)

    matches = filter_matches(matches)
    parse_matches(my_data, matches)

    for (key, team) in my_data.items():
        team["avgscore"] = round(team["totalscore"] / (team["wins"] + team["losses"]))
        team["totalscore"] = round(team["totalscore"])

    printj(my_data)


def init_teams(teams):
    return {
        team: {"wins": 0, "losses": 0, "totalscore": 0, "avgscore": 0} for team in teams
    }


def filter_matches(matches):
    return [match for match in matches if not not match["winning_alliance"]]


def parse_matches(my_data, matches):

    for match in matches:

        # printj(match)

        match_stats = get_match_stats(match)

        # print(match_stats["winners"]["score"], "-", match_stats["losers"]["score"])

        for team in match_stats["winners"]["teams"]:
            my_data[team]["wins"] += 1
            my_data[team]["totalscore"] += match_stats["winners"]["score"] / 3

        for team in match_stats["losers"]["teams"]:
            my_data[team]["losses"] += 1
            my_data[team]["totalscore"] += match_stats["losers"]["score"] / 3

        # break


def get_match_stats(match):

    win_alliance = match["winning_alliance"]
    win_stats = get_alliance_stats(match, win_alliance)

    lose_alliance = invert_alliance(win_alliance)
    lose_stats = get_alliance_stats(match, lose_alliance)

    return {"winners": win_stats, "losers": lose_stats}


def get_alliance_stats(match, alliance):
    return {
        "teams": match["alliances"][alliance]["team_keys"],
        "score": match["alliances"][alliance]["score"],
    }


def invert_alliance(a):
    if a == "red":
        return "blue"
    elif a == "blue":
        return "red"
    else:
        raise ValueError("alliance must be either red or blue")


def get_data(url):
    return requests.get(url).json()


def get_teams_url(api_key):
    base_url = "https://www.thebluealliance.com/api/v3"
    call = "event/2019cc/teams/simple"
    url = f"{base_url}/{call}?X-TBA-Auth-Key={api_key}"
    return url


def get_matches_url(api_key):
    base_url = "https://www.thebluealliance.com/api/v3"
    call = "event/2019cc/matches"
    url = f"{base_url}/{call}?X-TBA-Auth-Key={api_key}"
    return url


def printj(data):
    print(json.dumps(data, indent=4))


def get_api_key(file):
    with open(file, "r") as f:
        return json.load(f)["api_key"]


if __name__ == "__main__":
    main()
