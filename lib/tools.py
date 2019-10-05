import sys
import json

# project tools


def get_json_data(url):
    return requests.get(url).json()


def get_url(api_key, endpoint):
    base_url = "https://www.thebluealliance.com/api/v3"
    url = f"{base_url}/{endpoint}?X-TBA-Auth-Key={api_key}"
    return url


def get_api_key(file):
    with open(file, "r") as f:
        return json.load(f)["api_key"]


# system tools


def get_stdin():
    # read from standard input
    line = sys.stdin.readline()
    while line is not "":
        # return raw line data
        yield line
        # update match
        line = sys.stdin.readline()


# print tools


def printl(l):
    """
    print elements of a list
    """
    for element in l:
        print(element)


def printj(l):
    """
    print json
    """
    for element in l:
        print(json.dumps(element))


def printpj(data):
    """
    pretty print json
    """
    print(json.dumps(data, indent=4, sort_keys=True))
