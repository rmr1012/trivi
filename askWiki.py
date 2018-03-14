
import requests
import json
import re
import sys
import urllib
import random
from bs4 import BeautifulSoup
SPLITWEIGHT=0.5
MERGEWEIGHT=0.75
GOOGLEWEIGHT=2

keyword='A knish is traditionally stuffed with what filling?'

answers=['potato','creamed corn','lemon custard','raspberry jelly']


exclusionList=['the','be','to','of','and','a','in','that','have','I','it','for','on','with','he','as','you','do','at','this','but','his','by','from','they','we','say','her','she','or','an','will','my','all','would','there','their','what','so','up','out','if','about','who','get','which','go','me','when','make','can','like','time','just','him','know','take','people','into','year','your','good','some','could','see','other','than','then','now','look','only','come','its','over','think','also','back','after','use','how','our','work','first','well','way','even','new','want','because','any','these','give','day','most','us']

def askWiki(keyword,answers):
    url='https://www.google.com/search?q='+urllib.parse.quote_plus(keyword+' wikipedia')+'&format=json'
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    contentData=str(jsonData['query']['pages'])
    hits=[]
    for ans in answers:
        anshits=re.findall(ans,contentData)
        hits.append(len(anshits))

    return answers[hits.index(max(hits))]

def askGoogleQuestion(question,answers):
    hits=[0]*len(answers)
    url='https://www.google.com/search?q='+urllib.parse.quote_plus(question)+'&format=json'
    response = requests.get(url)
    text=cleanMe(response.content)
    for idx,ans in enumerate(answers):
        anshits=re.findall(ans,str(text))
        ansNoSpacehits=re.findall(ans.replace(" ", ""),str(text))
        splithits=0
        for apart in ans.split():
            if apart not in exclusionList:
                print(apart+'   is not in exclusion list')
                splithits+=len(re.findall(apart,str(text)))*SPLITWEIGHT
        hits[idx]+=GOOGLEWEIGHT*(len(anshits)+len(ansNoSpacehits)*MERGEWEIGHT+splithits)
        print('|---'+str(hits[idx])+'   '+ans)

    return hits
def cleanMe(html):
    soup = BeautifulSoup(html,"html.parser") # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
def askGoogleLink(question):
    url='https://www.google.com/search?q='+urllib.parse.quote_plus(question+' wikipedia')+'&format=json'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    links = soup.findAll("a")
    urlList=[]
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        target=re.search(r'(en.wikipedia.org.*?)(&amp)',str(link))
        try:
            url=target.group(1)
            noQstring=urllib.parse.quote_plus(question+' wikipedia').replace('+','%2B')
            if noQstring not in url:
                urlList.append(url)
        except:
            url='no match'
    return urlList

def pollWiki(sources,answers,hits=None):
    #print(sources)
    # print(answers)

    #work on NOT
    if hits==None:
        hits=[0]*len(answers)
    for source in sources:
        print(source)
        response = requests.get('http://'+source)
        text=cleanMe(response.content)

        for idx,ans in enumerate(answers):
            anshits=re.findall(ans,str(text))
            ansNoSpacehits=re.findall(ans.replace(" ", ""),str(text))
            splithits=0
            for apart in ans.split():
                if apart not in exclusionList:
                    print(apart+'   is not in exclusion list')
                    splithits+=len(re.findall(apart,str(text)))*SPLITWEIGHT
            hits[idx]+=len(anshits)+len(ansNoSpacehits)*MERGEWEIGHT+splithits
            print('|---'+str(hits[idx])+'   '+ans)

    return answers[hits.index(max(hits))]
if __name__=="__main__":
    # keyword=sys.argv[1]
    # answers=sys.argv[2:len(sys.argv)]

    # hi=pollWiki(askGoogle(keyword)[0:1],answers)
    trivias=json.load(open('QA.json'))
    record=[2]*100

    #badkey=[6,7,8,10,13,15,18,21,22,24,25]
    badkey=[7,8,18,21,24,25]
    badRange=[1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
    #badkey=[6]
    for i in range(len(badRange)):
        idx=i
        if not badRange[i]:
            ques=trivias[idx]['question']
            answers=[trivias[idx]['A'],trivias[idx]['B'],trivias[idx]['C'],trivias[idx]['D']]
            print('=======================================')
            print(ques)
            rightanswer=trivias[idx]['answer']
            ans=pollWiki(askGoogleLink(ques)[0:2],answers,hits=askGoogleQuestion(ques,answers))

            print(ans)
            if trivias[idx][rightanswer] == ans:
                print('BOT got it right :))')
                record[idx]=1
            else:
                print('BOT got it wrong :((')
                record[idx]=0
