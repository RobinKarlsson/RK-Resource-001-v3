from datetime import datetime, timedelta
from os.path import isfile
from stringoperations import streplacer
import sys
import os

class URL:
    def __init__(self, url, start = None, stop = None):
        self.url = url
        self.start = start
        self.stop = stop

def writeUsrPas(usr, pas):
    with open("config/login/data.dll", "wb") as f:
        f.write("%s %s" %(usr, pas))

def readUsrPas():
    with open("config/login/data.dll", "rb") as f:
        return f.read().split()
        

#return [int day, int month, int year]
def todaysDate():
    now = datetime.now()
    return [now.day, now.month, now.year]

def dateDaysAgo(x):
    date = datetime.now() - timedelta(days = x)
    return [date.day, date.month, date.year]

def dateHoursAgo(x):
    date = datetime.now() - timedelta(hours = x)
    return [date.day, date.month, date.year]

def fileopen(filename):
    msg = list()
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as doc:
                msg = doc.read()
        else:
            sys.exit("\n\nThe file %s is empty!!!\n\n" %filename)
    else:
        open(filename, "wb").close()
        sys.exit("\n\n%s doesn't exist, it has now been created!!!\n\n" %filename)

    return msg

def readMemFile(filename):
    target = []
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as placeholder:
                for line in placeholder.readlines():
                    if line != "\n":
                        target.append(streplacer(line, (["\n", ""], [" ", ""])))
    else:
        open(filename, "wb").close()

    return list(set(target))

def loadconfig(filename):
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as rowlist:
                condic = {}

                for line in rowlist:
                    data = line.split("==")
                    value = data[1].replace("\n", "")

                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            None

                    if value == "":
                        value = None

                    condic[data[0]] = value
                return condic
        else:
            print 2
            sys.exit("\n\nThe file %s is empty!!!\n\n" %filename)
    else:
        print 1
        sys.exit("\n\n%s doesn't exist!!!\n\n" %filename)

def createconfig(name, ID):
    with open("config/invites/%s.ini" %name, "wb") as setupfile:
        setupfile.write("Min online chess rating==\nMax online chess rating==\nMember on chess.com for days==\nGroup ID==%i\nFile containing the main invites list==data/invite lists/%s\nFile containing those who should receive priority invites (circumvents filter)==data/invite lists/%s priority\nInvites file for those who has left the group==data/invite lists/%s members who has left\nFile containing those who has received an invite==data/invite lists/%s already invited\nFile containing your invites message for members who has left your group==data/messages/%s Deserter message\nFile containing your invites message for standard and priority invites lists==data/messages/%s Standard Message\nComma seperated list of usernames that should not be invited==" %(ID, name, name, name, name, name, name))

    createfileifmissing("data/messages/%s Standard Message" %name, True)
    createfileifmissing("data/messages/%s Deserter message" %name, True)
    createfileifmissing("data/invite lists/%s already invited" %name)
    createfileifmissing("data/invite lists/%s members who has left" %name)
    createfileifmissing("data/invite lists/%s priority" %name)
    createfileifmissing("data/invite lists/%s" %name)


def createfileifmissing(filename, ismsg = False):
    if not os.path.isfile(filename):
        if not ismsg:
            open(filename, "wb").close()
        else:
            with open(filename, "wb") as mfile:
                mfile.write("<Text>\nHello this is an example message\n<Image>\nhttp://images.chesscomfiles.com/uploads/user/10117446.a001a3bf.600x450i.a24be423b414.jpeg\n<Video>\nhttp://www.youtube.com/watch?v=GY8YBF8dHQo")

def getfilelist(path, endswith):
    lst = list()
    counter = 1
    for files in os.walk(path):
        for flst in files:
            if type(flst) is list and len(flst) != 0:
                for fname in flst:
                    if fname.endswith(endswith):
                        lst.append([counter, fname])
                        counter += 1
    return lst

def enterint(text):
    while True:
        number = raw_input(text)
        if number == "":
            return number
        try:
            number = int(number)
            return number
        except ValueError:
            print "\n\nInvalid input, try again\n\n"

def makefolder(flst):
    for folder in flst:
        if not os.path.exists(folder):
            os.makedirs(folder)

def tlstcreator():
    targetlist = []
    choice = None

    while choice != "n":
        url = raw_input("Paste the url here: ")

        start = enterint("\nEnter pagenumber to start on: ")
        if start == "":
            targetlist.append(URL(url))
        else:
            stop = enterint("Enter pagenumber to end on: ")

            if stop == "":
                stop = 99

            targetlist.append(URL(url, start, stop))

        choice = None
        while choice not in ["y", "n"]:
            choice = raw_input("\nDo you wish to process any additional targets? (y/n): ")
            
    return targetlist

def memberfilter(member, minonlinerat = None, maxonlinerat = None, membersince = None):
    if membersince:
        if datetime(member.joined[2], member.joined[1], member.joined[0]) > datetime(membersince[2], membersince[1], membersince[0]):
            print datetime(member.joined[2], member.joined[1], member.joined[0])
            return False

    if minonlinerat:
        if member.daily < minonlinerat:
            print member.daily
            return False

    if maxonlinerat:
        if member.daily > maxonlinerat:
            print member.daily
            return False

    return True

def buildMsgList():
    print "\n\n\n\nsupported commands, will be replaced with each members respective info\n /name - members name or username (if name is unavailable)\n /username - member username\n /newline - pagebreak\n\n\n"

    msgList = []
    while True:
        additionType = None
        while additionType not in [1,2,3]:
            additionType = enterint("\n\nAdd a snippet containing\n 1. Text\n 2. Image\n 3. Youtube Video\nYour choice: ")

        if additionType == 1:
            txt = raw_input("Enter text: ")
            msgList.append("<Text>")
        elif additionType == 2:
            txt = raw_input("enter url of image: ")
            msgList.append("<Image>")
        elif additionType == 3:
            txt = raw_input("enter id of video: ")
            msgList.append("<Video>")

        msgList.append(txt)

        while additionType not in ["y", "n"]:
            additionType = raw_input("add another snippet? (y/n) ")
        if additionType == "n":
            break

    return msgList












