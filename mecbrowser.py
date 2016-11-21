import time
import cookielib
from processHTML import *
from stringoperations import *
from misc import *

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

#mecbrowser object, list of tuples with urls to scrap
def extractMemberList(br, targetList):
    memberlist = []

    for targettuple in targetList:
        for url in targettuple:
            while True:
                try:
                    print "processing %s" %url
                    res = mecopner(br, url)
                    soup = getSoup(res)
                    time.sleep(0.5)
                    break
                except Exception, e:
                    print repr(e)

            for usr in br.links(url_regex="chess.com/member/"):
                member = usr.text
                if not member[-5:] == "[IMG]" and member not in memberlist:
                    memberlist.append(member)

            if soup.find(class_ = "next disabled"):
                break

    return memberlist
        

def sendInvite(br, groupID, member, message):
    mecopner(br, "https://www.chess.com/clubs/%s/members/invite" %groupID)

    message = processMsgStr(message.replace("/name", member))

    counter = 0
    for form in br.forms():
        #print [(control.name, control.type) for control in form.controls]
        if "TextareaControl" in str(form):
            br.select_form(nr = counter)
            form.set_all_readonly(False)
            br["club_members_invite_type[usernames]"] = member
            br["club_members_invite_type[message]"] = message
            res = br.submit(nr=0)

            soup = getSoup(res)
            print wasInvited(soup, member)
            time.sleep(0.5)
            break
        else:
            counter += 1


#work in progress
def sendPM(br, member, message):
    mecopner(br, "https://www.chess.com/messages/compose/%s" %member)
