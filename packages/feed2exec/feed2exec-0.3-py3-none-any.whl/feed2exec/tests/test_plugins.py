from __future__ import division, absolute_import
from __future__ import print_function

import datetime
import email
try:
    import unittest.mock as mock
except ImportError:
    # py2
    import mock


import pytest

import feed2exec
import feed2exec.utils as utils
from feed2exec.feeds import parse, fetch
import feed2exec.plugins as plugins
import feed2exec.plugins.maildir as maildir_plugin
from feed2exec.tests.test_feeds import test_sample
from feed2exec.tests.fixtures import (test_db, static_boundary)  # noqa


def test_maildir(tmpdir, test_db, static_boundary):  # noqa
    global LOCK
    LOCK = mock.MagicMock()

    feed = {'name': 'INBOX', "mailbox": str(tmpdir.join('Mail'))}
    entry = {'summary': 'body',
             'title': 'subject',
             'link': 'http://example.com/',
             'published_parsed': datetime.datetime.now()}

    f = maildir_plugin.output(to_addr='nobody@example.com',
                              feed=feed, entry=entry, lock=LOCK)
    message = tmpdir.join('Mail', 'inbox', 'new', f.key)
    assert message.check()
    raw = message.read()
    assert 'base64' not in raw
    assert '==' not in raw

    # subject header hijack protection
    entry['title'] = 'subject\nX-Header-Hijack: true'
    with pytest.raises(email.errors.HeaderParseError):
        maildir_plugin.output(to_addr='nobody@example.com',
                              feed=feed, entry=entry, lock=LOCK)
    sample = {'name': 'maildir test',
              'url': test_sample['url'],
              'email': 'from@example.com',
              'folder': 'folder-test',
              'output': 'feed2exec.plugins.maildir',
              'mailbox': str(tmpdir.join('Mail')),
              'args': 'to@example.com'}
    body = fetch(sample['url'])
    data = parse(body, sample, lock=LOCK)
    for entry in data['entries']:
        f = plugins.output(sample, entry, lock=LOCK)
        message = tmpdir.join('Mail', 'folder-test', 'new', f.key)
        assert message.check()
        expected = '''Content-Type: multipart/alternative; boundary="===============testboundary=="
MIME-Version: 1.0
Date: Sun, 06 Sep 2009 16:20:00 -0000
To: to@example.com
From: test author <from@example.com>
Subject: Example entry
Message-ID: 7bd204c6-1655-4c27-aeee-53f933c5395f
User-Agent: feed2exec (%s)
Precedence: list
Auto-Submitted: auto-generated
Archive-At: http://www.example.com/blog/post/1

--===============testboundary==
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable

This is the  body, which should show instead of the above
--===============testboundary==
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable

http://www.example.com/blog/post/1

This is the body, which should show instead of the above


--===============testboundary==--
'''  # noqa
        assert (expected % feed2exec.__version__) == message.read()

    sample = {'name': 'date test',
              'url': 'file://' + utils.find_test_file('weird-dates.xml'),
              'email': 'from@example.com',
              'output': 'feed2exec.plugins.maildir',
              'mailbox': str(tmpdir.join('Mail')),
              'args': 'to@example.com'}
    body = fetch(sample['url'])
    data = parse(body, sample)
    for entry in data['entries']:
        f = plugins.output(sample, entry)
        message = tmpdir.join('Mail', utils.slug(sample['name']), 'new', f.key)
        assert message.check()
        assert '''Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
Date: Sun, 03 Sep 2017 09:03:54 -0000
To: to@example.com
From: date test <to@example.com>
Subject: test item
Message-ID: http-example-com-test
User-Agent: feed2exec (%s)
Precedence: list
Auto-Submitted: auto-generated
Archive-At: http://example.com/test/

test descr1''' % feed2exec.__version__ == message.read()


def test_echo(capfd):
    e = plugins.output(feed={'output': 'feed2exec.plugins.echo',
                             'args': 'foobar'},
                       item={})
    assert e.called
    out, err = capfd.readouterr()
    assert out == """arguments received: ('foobar',)\n"""


def test_error():
    # shouldn't raise
    plugins.output(feed={'output': 'feed2exec.plugins.error',
                         'args': ''},
                   item={})


def test_exec(capfd):
    e = plugins.output(feed={'output': 'feed2exec.plugins.exec',
                             'args': 'seq 1'},
                       item={})
    out, err = capfd.readouterr()
    assert out == "1\n"
    assert e == 0


def test_filter():
    item = {'title': 'test'}
    copy = item.copy()
    p = plugins.filter(feed={'filter': 'feed2exec.plugins.echo'}, item=item)
    assert item == copy
    assert p
    assert p.called is not None
    item = {'title': 'test'}
    plugins.filter(feed={'filter': 'feed2exec.plugins.null'}, item=item)
    assert item != copy
    assert p.called is not None
