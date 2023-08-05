from vr.server import models as M


def test_stringify():
    for data, expected in [
            (1, '1'),
            ('a', 'a'),
            ({}, '[]'),
            ({'a': 1}, '''["['a', '1']"]'''),
            (set(), '[]'),
            ([], '[]'),
            ((), '[]'),
            ('\xa3', '\xa3'),
            (u'\xa3', u'\xa3'),
            (['\xa3'], '''['\\xa3']'''),
            ([u'\xa3'], '''[u'\\xa3']'''),
    ]:
        assert M.stringify(data) == expected


def test_make_hash():
    for data, expected in [
            (1, 'c4ca4238a0b923820dcc509a6f75849b'),
            ('a', '0cc175b9c0f1b6a831c399e269772661'),
            ({}, 'd751713988987e9331980363e24189ce'),
            (set(), 'd751713988987e9331980363e24189ce'),
            ([], 'd751713988987e9331980363e24189ce'),
            ((), 'd751713988987e9331980363e24189ce'),
            ('\xa3', 'd527ca074d412d9d0ffc844872c4603c'),
            (u'\xa3', 'd99731d14c7750048538404febb0e357'),
    ]:
        assert M.make_hash(data) == expected
