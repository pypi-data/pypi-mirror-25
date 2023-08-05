import treq
import re
from helga.plugins import match, ResponseNotReady
from helga import log, settings

from twisted.internet import defer

logger = log.getLogger(__name__)

def get_api_key(settings):
    return getattr(settings, 'REDMINE_API_KEY', None)

@defer.inlineCallbacks
def get_issue_subject(ticket_url, api_key=None):
    """
    Find the "subject" string in the JSON data of a ticket.
    :param ticket_url: URL for a ticket
    :param api_key: API secret key (string), or None if you do not want to
                    authenticate to Redmine.
    :returns: twisted.internet.defere.Deferred. When this Deferred fires, it
              will return a "subject" string to its callback.
    """
    api_url = "%s.json" % ticket_url
    request_headers = {}
    if api_key is not None:
        request_headers['X-Redmine-API-Key'] = api_key
    try:
        response = yield treq.get(api_url, headers=request_headers, timeout=5)
        if response.code != 200:
            subject = 'could not read subject, HTTP code %i' % response.code
            defer.returnValue((ticket_url, subject))
        else:
            content = yield treq.json_content(response)
            defer.returnValue((ticket_url, content['issue']['subject']))
    except Exception, e:
        # For example, if treq.get() timed out, or if treq.json_content() could
        # not parse the JSON, etc.
        subject = 'could not read subject, %s' % e.message
        defer.returnValue((ticket_url, subject))

def construct_message(urls_and_subjects, nick):
    """
    Return a string about a nick and a list of tickets' URLs and subjects.
    """
    msgs = []
    for url_and_subject in urls_and_subjects:
        ticket_url, subject = url_and_subject
        msgs.append('%s [%s]' % (ticket_url, subject))
    if len(msgs) == 1:
        msg = msgs[0]
    else:
        msg = "{} and {}".format(", ".join(msgs[:-1]), msgs[-1])
    return "%s might be talking about %s" % (nick, msg)

def send_message(urls_and_subjects, client, channel, nick):
    """
    Send a message to an IRC/XMPP channel about a list of tickets' URLs and
    subjects.
    """
    msg = construct_message(urls_and_subjects, nick)
    client.msg(channel, msg)

def match_tickets(message):
    tickets = []
    pattern = re.compile(r"""
       (?:               # Prefix to trigger the plugin:
            issues?      #   "issue" or "issues"
          | tickets?     #   "ticket" or "tickets"
          | bugs?        #   "bug" or "bugs"
          | redmines?    #   "redmine" or "redmines"
       )                 #
       \s+               #
       [#]?[0-9]+        # Number, optionally preceded by "#"
       (?:               # The following pattern will match zero or more times:
          ,?             #   Optional comma
          \s+            #
          (?:and\s+)?    #   Optional "and "
          [#]?[0-9]+     #   Number, optionally preceded by "#"
       )*
       """, re.VERBOSE | re.IGNORECASE
    )
    for match in re.findall(pattern, message):
        for ticket in re.findall(r'[0-9]+', match):
            tickets.append(ticket)
    return tickets


@match(match_tickets, priority=0)
def redmine(client, channel, nick, message, matches):
    """
    Match possible Redmine tickets, return links and subject info
    """
    api_key = get_api_key(settings)

    deferreds = []
    for ticket_number in matches:
        try:
            ticket_url = settings.REDMINE_URL % {'ticket': ticket_number}
        except AttributeError:
            return 'Please configure REDMINE_URL to point to your tracker.'

        deferreds.append(get_issue_subject(ticket_url, api_key))

    d = defer.gatherResults(deferreds, consumeErrors=True)
    d.addCallback(send_message, client, channel, nick)
    raise ResponseNotReady
