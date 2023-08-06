"""Defines a class for storing a person's slack profile information."""
import attr
from nameparser import HumanName


def _makenames(user):
    fname = ''
    lname = ''
    if 'first_name' in user['profile']:
        fname = user['profile']['first_name']
    if 'last_name' in user['profile']:
        lname = user['profile']['last_name']
    if not fname:
        if 'real_name' in user['profile']:
            name = HumanName(user['profile']['real_name'])
            fname = name.first
            lname = name.last
        elif 'display_name' in user['profile']:
            name = HumanName(user['profile']['display_name'])
            fname = name.first
            lname = name.last
        else:
            fname = ''
            lname = ''
    return fname, lname

@attr.s
class SlackPerson(object):
    """Class for storing/getting slack profile information."""
    userid = attr.ib()
    email = attr.ib()
    username = attr.ib()
    fname = attr.ib()
    lname = attr.ib()
    team = attr.ib()

    @classmethod
    def from_userlist(cls, team_user_list, username=None,
                      userid=None):
        """Initializes SlackPerson.

        Arguments:
        username: the handle with or without @ used to mention someone
        userid: the internal userid from slack.
        team_user_list: json object returned by the slack api `users.list`
        method.
        """
        if username:
            if username[0] == '@':
                username = username[1:]
            test_value = username
            key = 'name'
        elif userid:
            test_value = userid
            key = 'id'
        else:
            raise AttributeError("username or user_id is required")

        try:
            for user in team_user_list['members']:
                if test_value == user[key]:
                    fname, lname = _makenames(user)
                    # parse the json to get the user's info
                    return cls(username=user['name'],
                               userid=user['id'],
                               email=user['profile']['email'],
                               fname=fname,
                               lname=lname,
                               team=user['profile']['team']
                               )
        except (KeyError, TypeError) as err:
            raise SlackDataError(
                "team_user_list is not formed correctly: {}".format(err))

        raise SlackDataError("{} was not found in the user list".format(
            test_value))

    @classmethod
    def from_userinfo(cls, userinfo):
        """Initializes SlackPerson.

        Arguments:
        userinfo: json object returned by slackapi 'user.info'
        """
        # parse the json to get the user's info
        if not isinstance(userinfo, dict):
            raise TypeError('userinfo is not a dict')
        try:
            user = userinfo['user']
        except KeyError:
            try:
                _ = userinfo['name']
                user = userinfo
            except KeyError as err:
                raise SlackDataError(("userinfo is not formed correctly: "
                                      " {}".format(err)))

        try:
            fname, lname = _makenames(user)
            return cls(username=user['name'],
                       userid=user['id'],
                       email=user['profile']['email'],
                       fname=fname,
                       lname=lname,
                       team=user['profile']['team']
                       )
        except (KeyError, TypeError) as err:
            raise SlackDataError(("userinfo is not formed correctly: "
                                  " {}".format(err)))


class SlackDataError(Exception):
    """Exception raised if input data is invalid in some way."""
    pass
