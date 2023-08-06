"""Test for slackperson."""
import pytest
from slackperson import SlackPerson
from slackperson import SlackDataError


@pytest.fixture
def userlist():
    return {
        "members": [
            {
                "color": "ffffff",
                "id": "U00000001",
                "name": "jbiden",
                "profile": {
                    "email": "jbiden@whitehouse.gov",
                    "first_name": "Joe",
                    "last_name": "Biden",
                    "real_name": "Joe Biden",
                    "real_name_normalized": "Joe Biden",
                    "team": "T00000001",
                    "title": ""
                },
                "real_name": "Joe Biden",
                "team_id": "T00000001",
                "tz": "America/New_York",
                "tz_label": "Eastern Daylight Time",
                "tz_offset": -14400,
            },
            {
                "color": "000000",
                "id": "U00000002",
                "name": "bobama",
                "profile": {
                    "email": "bobama@whitehouse.gov",
                    "first_name": "Barack",
                    "last_name": "Obama",
                    "real_name": "Barack Obama",
                    "real_name_normalized": "Barack Obama",
                    "team": "T00000001"
                },
                "real_name": "Barack Obama",
                "team_id": "T00000001",
                "tz": "America/New_York",
                "tz_label": "Eastern Daylight Time",
                "tz_offset": -14400,
            },
            {
                "color": "000000",
                "id": "U00000003",
                "name": "mobama",
                "profile": {
                    "email": "mobama@whitehouse.gov",
                    "real_name": "Michelle Obama",
                    "real_name_normalized": "Michelle Obama",
                    "team": "T00000001"
                },
                "real_name": "Michelle Obama",
                "team_id": "T00000001",
                "tz": "America/New_York",
                "tz_label": "Eastern Daylight Time",
                "tz_offset": -14400,
            },
            {
                "color": "000000",
                "id": "U00000004",
                "name": "dmcdonough",
                "profile": {
                    "email": "dmcdonough@whitehouse.gov",
                    "display_name": 'Dennis',
                    "team": "T00000001"
                },
                "team_id": "T00000001",
                "tz": "America/New_York",
                "tz_label": "Eastern Daylight Time",
                "tz_offset": -14400,
            },
            {
                "color": "000000",
                "id": "U00000005",
                "name": "nobody",
                "profile": {
                    "email": "noname@whitehouse.gov",
                    "team": "T00000001"
                },
                "team_id": "T00000001",
                "tz": "America/New_York",
                "tz_label": "Eastern Daylight Time",
                "tz_offset": -14400,
            },
        ],
    }


@pytest.fixture
def userinfo():
    return {
        "color": "000000",
        "id": "U00000002",
        "name": "bobama",
        "profile": {
            "email": "bobama@whitehouse.gov",
            "first_name": "Barack",
            "last_name": "Obama",
            "real_name": "Barack Obama",
            "real_name_normalized": "Barack Obama",
            "team": "T00000001"
        },
        "real_name": "Barack Obama",
        "team_id": "T00000001",
        "tz": "America/New_York",
        "tz_label": "Eastern Daylight Time",
        "tz_offset": -14400,
    }


@pytest.fixture
def userinfo_full(userinfo):
    return {
        'ok': 'true',
        'user': userinfo
    }


def test_from_userlist_username(userlist):
    """Test that the SlackPerson has all the right attributes."""
    test_person = SlackPerson.from_userlist(
        username='bobama',
        team_user_list=userlist
    )
    assert test_person.userid == 'U00000002'
    assert test_person.email == 'bobama@whitehouse.gov'
    assert test_person.fname == 'Barack'
    assert test_person.lname == 'Obama'
    assert test_person.team == 'T00000001'
    assert test_person.username == 'bobama'

    # test that usernames with @s work
    test_person2 = SlackPerson.from_userlist(
        username='@jbiden',
        team_user_list=userlist
    )
    assert test_person2.userid == 'U00000001'
    assert test_person2.email == 'jbiden@whitehouse.gov'
    assert test_person2.fname == "Joe"
    assert test_person2.lname == "Biden"
    assert test_person2.team == 'T00000001'


def test_weird_names(userlist):
    # test that users with only real_name work
    test_person1 = SlackPerson.from_userlist(
        username='mobama',
        team_user_list=userlist
    )
    assert test_person1.userid == 'U00000003'
    assert test_person1.email == 'mobama@whitehouse.gov'
    assert test_person1.fname == "Michelle"
    assert test_person1.lname == "Obama"
    assert test_person1.team == 'T00000001'

    # test that users with only display_name work
    test_person2 = SlackPerson.from_userlist(
        username='dmcdonough',
        team_user_list=userlist
    )
    assert test_person2.userid == 'U00000004'
    assert test_person2.email == 'dmcdonough@whitehouse.gov'
    assert test_person2.fname == "Dennis"
    assert test_person2.lname == ""
    assert test_person2.team == 'T00000001'

    # test that users with only display_name work
    test_person3 = SlackPerson.from_userlist(
        username='nobody',
        team_user_list=userlist
    )
    assert test_person3.userid == 'U00000005'
    assert test_person3.email == 'noname@whitehouse.gov'
    assert test_person3.fname == ""
    assert test_person3.lname == ""
    assert test_person3.team == 'T00000001'


def test_from_userlist_userid(userlist):
    test_person = SlackPerson.from_userlist(team_user_list=userlist,
                                            userid='U00000002')
    assert test_person.userid == 'U00000002'
    assert test_person.email == 'bobama@whitehouse.gov'
    assert test_person.fname == 'Barack'
    assert test_person.lname == 'Obama'
    assert test_person.team == 'T00000001'
    assert test_person.username == 'bobama'


def test_userlist_exceptions(userlist):
    """Test data validation and exceptions."""
    # User is not in list
    with pytest.raises(SlackDataError):
        SlackPerson.from_userlist(username='dtrump', team_user_list=userlist)

    # team_user_list is wrong type
    with pytest.raises(SlackDataError):
        SlackPerson.from_userlist(username='bobama',
                                  team_user_list='wrongtype')

    # team_user_list doesn't have members
    with pytest.raises(SlackDataError):
        SlackPerson.from_userlist(
            username='jbiden',
            team_user_list={'ok': False, 'error': 'could not get data'}
        )

    with pytest.raises(AttributeError):
        SlackPerson.from_userlist(team_user_list=userlist)


def test_from_userinfo(userinfo, userinfo_full):
    test_person = SlackPerson.from_userinfo(userinfo=userinfo)
    assert test_person.userid == 'U00000002'
    assert test_person.email == 'bobama@whitehouse.gov'
    assert test_person.fname == 'Barack'
    assert test_person.lname == 'Obama'
    assert test_person.team == 'T00000001'
    assert test_person.username == 'bobama'

    test_person2 = SlackPerson.from_userinfo(userinfo=userinfo_full)
    assert test_person2.userid == 'U00000002'
    assert test_person2.email == 'bobama@whitehouse.gov'
    assert test_person2.fname == 'Barack'
    assert test_person2.lname == 'Obama'
    assert test_person2.team == 'T00000001'
    assert test_person2.username == 'bobama'


def test_userinfo_exceptions():
    with pytest.raises(TypeError):
        SlackPerson.from_userinfo(userinfo='fail')
    with pytest.raises(SlackDataError):
        SlackPerson.from_userinfo(userinfo={'fail': 'fail'})
    with pytest.raises(SlackDataError):
        SlackPerson.from_userinfo(userinfo={'name': 'test'})
