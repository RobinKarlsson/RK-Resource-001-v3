from mecbrowser import buildMember

class Member:
    def __init__(self, username, name = None, daily = None, tactics = None, lessons = None, rapid = None, bullet = None, blitz = None, joined = []):
        self.username = username
        if name:
            self.name = name
        else:
            self.name = username
        self.daily = daily
        self.tactics = tactics
        self.lessons = lessons
        self.rapid = rapid
        self.bullet = bullet
        self.blitz = blitz
        self.joined = joined


def makeMember(br, usrname):
    member = Member(usrname)

    if not buildMember(br, member):
        return

    return member
    
