from stringoperations import *
from misc import *

try:
    from bs4 import BeautifulSoup
except:
    sys.exit("\n\n\tCouln't import the BeautifulSoup4 library, shutting down\n\n")

def getSoup(response):
    return BeautifulSoup(response, "html.parser")

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
            raw_input("This Should NOT happen, please contact the developer")



#return [int day, int month, int year]
#needs more work
def getLastOnline(soup):
    res = soup.find("div", {"class" : "member-info-row"}).text.split("\n")
    for x in range(len(res)):
        if res[x] == "Last Login":
            if res[x + 1] == "In Live":
                return todaysDate()

#return [int day, int month, int year]
def getJoinDate(soup):
    res = soup.find("div", {"class" : "member-info-row"}).text.split("\n")
    for x in range(len(res)):
        if res[x] == "Joined":
            date = res[x + 1].split(" ")
            return [int(date[1][:-1]), int(streplacer(date[0], (["Jan", "01"], ["Feb", "02"], ["Mar", "03"], ["Apr", "04"], ["May", "05"], ["Jun", "06"], ["Jul", "07"], ["Aug", "08"], ["Sep", "09"], ["Oct", "10"], ["Nov", "11"], ["Dec", "12"]))), int(date[2])]



#returns nation if no name found, NOT OPERATIONAL
def getName(soup):
    details = soup.find("div", {"class" : "details"})
    if details:
        name = details.text.strip().split("\n")[0]
        return name
    else:
        print "invalid user"
        return None
