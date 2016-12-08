
def streplacer(text, rplst):
    for rptup in rplst:
        text = text.replace(rptup[0], rptup[1])
    return text


def processMsgStr(inData):
    inData = inData.split("\n")

    i = 0
    while i < len(inData):
        if inData[i] == "<Image>":
            inData[i] = ""
            inData[i + 1] = """<img src="%s">""" %inData[i + 1]

        elif inData[i] == "<Text>":
            inData[i] = ""
            inData[i + 1] = inData[i + 1].replace("/newline", """<br>""")

        elif inData[i] == "<Video>":
            inData[i] = ""
            inData[i + 1] = """<iframe width="640" height="360" src="//www.youtube.com/embed/%s?rel=0" frameborder="0" allowfullscreen></iframe>""" %inData[i + 1]

        i += 1

    return u"%s" %"".join(inData)

