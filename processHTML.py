import re
from stringoperations import *
from misc import *

try:
    from bs4 import BeautifulSoup
except:
    sys.exit("\n\n\tCouln't import the BeautifulSoup4 library, shutting down\n\n")

def getSoup(response):
    return BeautifulSoup(response, "html.parser")

def isClosed(soup):
    status = soup.find("span", "status-title")
    if status and status.text == "Closed: Inactive":
        return True

def getNextLinkFormat(soup):
    nextLink = soup.find("a", href = True, title = "Next")

    if nextLink:
        nextLink = nextLink["href"]
        print nextLink
        return nextLink[nextLink.index("page=") - 1]
    return None

def nextPageExist(soup):
    if soup.find("a", href = True, title = "Next"):
        return True
    return False

def wasInvited(soup, member):
    msgs = [x.text for x in soup.find_all("div", {"class" : ["alert-error", "alert-success"]})]

    for x in msgs:
        if " is already a member of this club" in x:
            return "%s is already a member of this club" %member
        elif "Invitations sent to 0 members." in x:
            return "failed to invite %s" %member
        elif "Invitations sent to 1 members." in x:
            return "Invite sent to %s" %member
        else:
            return("This Should NOT happen, please contact the developer")

    return "\nthis should NOT have happened, please send this to your friendly neighbour sudo:\n%s\n" %str(msgs)



#return [int day, int month, int year]
#not working correctly, might sometimes give wrong date
#work in progress. need months ago, years ago and weeks ago, and possibly more
def getLastOnline(soup):
    res = soup.find("div", {"class" : "member-info-row"}).text.split("\n")
    for x in range(len(res)):
        if res[x] == "Last Login":
            if res[x + 1] == "In Live" or res[x + 1] == "Online Now" or "min ago" in res[x + 1]:
                return todaysDate()
            if "hrs ago" in res[x + 1]:
                hoursAgo = int(res[x + 1][0: res[x + 1].index("hrs ago")])
                return dateHoursAgo(hoursAgo)
            if "days ago" in res[x + 1]:
                daysAgo = int(res[x + 1][0: res[x + 1].index("days ago")])
                return dateDaysAgo(daysAgo)

#return [int day, int month, int year]
def getJoinDate(soup):
    res = soup.find("div", {"class" : "member-info-row"}).text.split("\n")
    for x in range(len(res)):
        if res[x] == "Joined":
            date = res[x + 1].split(" ")
            return [int(date[1][:-1]), int(streplacer(date[0], (["Jan", "01"], ["Feb", "02"], ["Mar", "03"], ["Apr", "04"], ["May", "05"], ["Jun", "06"], ["Jul", "07"], ["Aug", "08"], ["Sep", "09"], ["Oct", "10"], ["Nov", "11"], ["Dec", "12"]))), int(date[2])]


#input res, member object
def setRatings(res, member):
    soup = getSoup(res)

    for tmp in soup.find_all("h3"):
        section = tmp.text.split()
        if len(section) == 2:
            if section[0] == "Daily":
                member.daily = int(section[1])

            elif section[0] == "Tactics":
                member.tactics = int(section[1])

            elif section[0] == "Lessons":
                member.lessons = int(section[1])

            elif section[0] == "Rapid":
                member.rapid = int(section[1])

            elif section[0] == "Bullet":
                member.bullet = int(section[1])

            elif section[0] == "Blitz":
                member.blitz = int(section[1])


#input soup object, member object
def setName(soup, member):
    details = soup.find("div", {"class" : "details"})
    if details:
        name = details.text.strip().split("\n")[0]
    else:
        return

    for x in soup.find_all("span", {"class" : "username"}):
        if "data-name" in x:
            if name in x:
                member.name = name
                return


def getMemberID(soup):
    res = str(soup.find("div", {"class" : "load-more-container"})).split()

    for tmp in res:
        if "userId" in tmp:
            return re.findall(r'\d+', tmp)[0]

def gettoken(soup):
    for x in str(soup).strip().split():
        if '{"userId":"userId","user":{"id":' in x:
            return x[x.index('"token":"') + 9: -4]
