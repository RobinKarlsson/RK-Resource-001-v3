from mecbrowser import *
from misc import *

makefolder(["data", "data/message"])

def login(br):
    x = None
    while x not in ["y", "n"]:
        x = raw_input("login? (y/n) ")

    if x == "y":
        username = raw_input("username: ")
        password = raw_input("password: ")
        meclogin(br, username, password)

def main():
    choice = enterint("What would you like to do?\n 1. Extract member lists\n 2. send invites (under construction)\nYour choice, monkeyboy: ")
    br = mecbrowser()
    print "\n"

    if choice == 1:
        targetlst = tlstcreator()
        memlist = extractMemberList(br, targetlst)

        print "\n%i members found:" %len(memlist)
        print " ".join(memlist)

    elif choice == 2:
        login(br)
        groupID = raw_input("Enter group id: ")
        invitee = raw_input("Enter member to invite: ")
        msgpath = raw_input("path to invites msg: ")
        sendInvite(br, groupID, invitee, fileopen(msgpath))

    br.close()


if __name__ == '__main__':
    while True:
        main()

        choice = None
        while choice not in ["y", "n"]:
            choice = raw_input("\n\nrun again? (y/n) ")
        if choice == "n":
            break
        print "\n\n"
