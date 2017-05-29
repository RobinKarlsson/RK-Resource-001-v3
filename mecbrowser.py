import time
import cookielib
import urllib
from processHTML import *
from stringoperations import *
from misc import *
from urllib2 import HTTPError

try:
    import mechanize
except:
    sys.exit("\n\n\tCouln't import the mechanize library, shutting down\n\n")
mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 100



def mecbrowser():
    br = mechanize.Browser()

    cookiejar = cookielib.LWPCookieJar() 
    br.set_cookiejar(cookiejar) 

    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_gzip(False)
    br.set_handle_referer(True)
    br.set_handle_refresh(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    return br


def mecopner(br, url):
    while True:
        try:
            response = br.open(url)
            return response

        except HTTPError:
            return
        except Exception, errormsg:
            print repr(errormsg)
            print "reopening %s" %url
            time.sleep(1.5)


def meclogin(br, usr, pas):
    response = mecopner(br, "https://www.chess.com/login")

    counter = 0
    for form in br.forms():
        br.select_form(nr = counter)
        try:
            br["_username"] = usr
            br["_password"] = pas
            res = br.submit()
            break
        except:
            counter += 1

#mecbrowser object, list of URL objects
def extractMemberList(br, targetList):
    memberlist = []

    for target in targetList:
        nextgagectrl = None

        nextCtrl = getNextLinkFormat(getSoup(mecopner(br, target.url)))

        if target.start:
            pages = [str(x) for x in range(target.start, target.stop + 1)]
        else:
            pages = [None]

        for page in pages:
            if page and nextCtrl:
                url = target.url + nextCtrl + "page=" + page
            else:
                url = target.url

            while True:
                try:
                    print "processing %s" %url
                    res = mecopner(br, url)
                    time.sleep(0.5)
                    break
                except Exception, e:
                    print repr(e)

            for usr in br.links(url_regex="chess.com/member/"):
                member = usr.text
                if not member[-5:] == "[IMG]" and member not in memberlist:
                    memberlist.append(member)

            if not nextPageExist(getSoup(res)):
                break

    return memberlist
        
#work in progress
def sendInvite(br, groupID, member, message):
    mecopner(br, "https://www.chess.com/clubs/%s/members/invite" %groupID)

    message = processMsgStr(message.replace("/name", member.name).replace("/username", member.username))

    counter = 0
    for form in br.forms():
        if "TextareaControl" in str(form):
            br.select_form(nr = counter)
            form.set_all_readonly(False)
            br["club_members_invite_type[usernames]"] = member.username
            br["club_members_invite_type[message]"] = message
            res = br.submit(nr = 0)

            soup = getSoup(res)
            print wasInvited(soup, member.username)
            time.sleep(0.5)
            return True
        else:
            counter += 1
    return False


#work in progress
def sendNote(br, member, message, delay = 30):
    res = mecopner(br, "https://www.chess.com/member/%s" %member.username)
    soup = getSoup(res)

    usrID = getMemberID(soup)

    parameters = {"user_id" : usrID, "user_note" : message.replace("/name", member.name).replace("/username", member.username)}
    data = urllib.urlencode(parameters)
    br.open("https://www.chess.com/callback/user/note", data)
    time.sleep(delay)


#input browser object, member object
def buildMember(br, member):
    res = mecopner(br, "https://www.chess.com/member/%s" %member.username)

    if not res:
        return

    soup = getSoup(res)
    if isClosed(soup):
        return

    print "building member: " + member.username

    setName(soup, member)
    member.joined = getJoinDate(soup)

    res = mecopner(br, "https://www.chess.com/stats/daily/%s" %member.username)
    setRatings(res, member)
    return True

#work in progress
def sendPM(br, member, message, delay = 60):
    res = mecopner(br, "https://www.chess.com/messages/compose/%s" %member.username)
    soup = getSoup(res)
    message = processMsgStr(message.replace("/name", member.name).replace("/username", member.username))

    token = gettoken(soup) #get your unique session token

    parameters = {"_token" : token, "message" : message, "receiver[username]" : member.username}
    data = urllib.urlencode(parameters)
    br.open("https://www.chess.com/callback/messages/%s" %member.username, data)
    time.sleep(delay)
