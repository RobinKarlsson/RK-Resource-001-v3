
def streplacer(text, rplst):
    for rptup in rplst:
        text = text.replace(rptup[0], rptup[1])
    return text


def processMsgStr(string):
    string = string.replace("/newline", """<br>""").split("\n")

    i = 0
    while i < len(string):
        if string[i] == "<Image>":
            string[i] = ""
            string[i + 1] = """<img src="%s">""" %string[i + 1]

        elif string[i] == "<Text>":
            string[i] = ""

        elif string[i] == "<Video>":
            string[i] = ""
            string[i + 1] = """<iframe width="640" height="360" src="//www.youtube.com/embed/%s?rel=0" frameborder="0" allowfullscreen></iframe>""" %string[i + 1]

        i += 1

    return u"%s" %"".join(string)

