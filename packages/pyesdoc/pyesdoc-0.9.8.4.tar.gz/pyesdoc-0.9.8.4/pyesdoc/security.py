# -*- coding: utf-8 -*-

"""
.. module:: security.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Wraps security related functions.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import json
import os

import requests



# GitHub - user name.
_GH_USER_NAME = 'esdoc-system-user'

# GitHub - access token.
_GH_ACCESS_TOKEN = os.getenv('ESDOC_GITHUB_ACCESS_TOKEN')

# GitHub API - credentials.
_GH_API_CREDENTIALS = (_GH_USER_NAME, _GH_ACCESS_TOKEN)

# GitHub API - organization.
_GH_API_ORG = "https://api.github.com/orgs/ES-DOC-INSTITUTIONAL"

# GitHub API - teams.
_GH_API_TEAMS = "https://api.github.com/teams"

# GitHub API - user.
_GH_API_USER = "https://api.github.com/user"

# Local cache of ES-DOC teams.
_TEAMS = None


def get_team(team_id):
    """Returns set of existing GH teams.

    :param str|int team_id: Identifier of an ES-DOC GitHub team.

    :returns: ES-DOC GitHub team information.
    :rtype: dict

    """
    key = 'id' if isinstance(team_id, int) else 'name'
    for team in get_teams():
        if team[key] == team_id:
            return team

    raise ValueError('GitHub team does not exist: {}'.format(team_id))


def get_teams():
    """Returns set of ES-DOC GitHub teams.

    :returns: Collection of ES-DOC GitHub teams.
    :rtype: list

    """
    global _TEAMS

    if _TEAMS is None:
        url = '{}/teams?per_page=100'.format(_GH_API_ORG)
        r = requests.get(url, auth=_GH_API_CREDENTIALS)
        _TEAMS = json.loads(r.text)

    return _TEAMS


def is_team_member(team_id, user_id):
    """Returns flag indicating whether user is a member of a team.

    :param str|int team_id: ES-DOC GitHub team identifier.
    :param str user_id: GitHub user login.

    :returns: Flag indicating whether user is a member of team.
    :rtype: bool

    """
    team_id = team_id if isinstance(team_id, int) else get_team(team_id)['id']
    url = '{}/{}/memberships/{}'.format(_GH_API_TEAMS, team_id, user_id)
    r = requests.get(url, auth=_GH_API_CREDENTIALS)

    return r.status_code == 200


def is_authenticated_user(user_id, access_token):
    """Returns flag indicating whether user credentials are recognized by GitHub.

    :param str user_id: GitHub user login.
    :param str access_token: GitHub user access token.

    :returns: Flag indicating whether user is authenticated by GitHub.
    :rtype: bool

    """
    r = requests.get(_GH_API_USER, auth=(user_id, access_token))

    return r.status_code == 200 and \
           'read:org' in r.headers['X-OAuth-Scopes'] and \
            json.loads(r.text)['login'] == user_id
