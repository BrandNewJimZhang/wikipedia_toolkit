import requests
import time
from bs4 import BeautifulSoup

class en_wikipedia_toolkit:
    '''
    This toolkit is used to edit Wikipedia for an auto-confirmed user.
    I'm BrandNew Jim Zhang. Please contact me via:
    1. http://www.brandnewjimzhang.com
    2. https://en.wikipedia.org/wiki/User:BrandNew_Jim_Zhang
    '''
    def fetch_code(self,page):
        '''
        Fetch the code of a page.
        '''
        starttime = time.time()

        URL = "https://en.wikipedia.org/w/api.php"
        S = requests.Session()

        PARAM_code = {
            "action": "query",
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "*",
            "titles": page,
            "format": "json",
            }
        R = S.post(URL, data=PARAM_code)
        DATA = R.json()
        #Can be used only for one page.
        for i in DATA['query']['pages'].keys():
            text=DATA['query']['pages'][i]['revisions'][0]['slots']['main']['*']
        file=open(page+".wikitext",'w',encoding='utf-8')
        file.write(text)
        print('Done. The source code was written in',"'"+page+".wikitext'.")

        endtime = time.time()
        dtime = endtime - starttime
        print("All processes were done in %.3f second(s)." % dtime)

    def upload(self,page,path,summary="",minor=False):
        '''
        Upload the code of a page.

        Page is the page you want to upload to, like 'Taylor Swift' and 'Bill Gates'.
        Path is the place where you store the text, both relative and absolute path are OK.
        
        Arguments:
        Summary is the way like you did in Wikipedia.
        Minor is Boolean, which will identify the edit is minor or not, default False.
        '''
        starttime = time.time()

        file=open(path,'r',encoding='utf-8')
        text=file.read()

        S = requests.Session()
        URL = "https://en.wikipedia.org/w/api.php"

        # Step 1: GET request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }
        R = S.get(url=URL, params=PARAMS_0)
        DATA = R.json()
        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

        # Step 2: POST request to log in. 
        PARAMS_1 = {
            "action": "login",
            "lgname": "username",
            "lgpassword": "password",
            "lgtoken": LOGIN_TOKEN,
            "format": "json"
        }
        R = S.post(URL, data=PARAMS_1)

        # Step 3: GET request to fetch CSRF token
        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }
        R = S.get(url=URL, params=PARAMS_2)
        DATA = R.json()
        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

        summary_new="Edit via an opensourced program on [GitHub https://github.com/BrandNewJimZhang/en_wikipedia_toolkit].// "+summary

        # Step 4: POST request to edit a page
        PARAMS_3 = {
            "action": "edit",
            "title": page,
            "token": CSRF_TOKEN,
            "summary": summary_new,
            "format": "json",
            "text": text,
            "minor": minor
        }
        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        try:
            if DATA['edit']['result']=='Success':
                print('Upload done. See the page on '+'https://en.wikipedia.org/w/index.php?title='+'_'.join(page.split()))
        except:
            print('Oh shit!')

        PARAMS_4 = {
            "action": "query",
            "meta": "userinfo",
            'uiprop': 'editcount',
            "format": "json"
        }
        R = S.post(URL, data=PARAMS_4)
        DATA = R.json()

        editcount=DATA["query"]["userinfo"]["editcount"]
        print('After uploading, your editcount is ',str(editcount),'.',sep='')

        endtime = time.time()
        dtime = endtime - starttime
        print("All processes were done in %.3f second(s)." % dtime)

class spider:
    '''
    All the functions are used to scratch the content into wikitext reference.
    '''
    def billboard(self,url):
        '''
        Fetch content from www.billboard.com.
        '''

        starttime = time.time()

        r = requests.get(url)
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text,'html.parser')
        title=soup.select('#main > main > section.main-well.js-mainWell > article > div.article__header > h1')[0].get_text().strip()
        try:
            date=soup.select('#main > main > section.main-well.js-mainWell > article > div.article__details > p.article__meta.article__meta--below-media > span.js-publish-date.article__publish-date')[0].get_text().strip()
        except:
            date=soup.select('#main > main > section.main-well.js-mainWell > article > div.article__header > p.article__meta > span.js-publish-date.article__publish-date')[0].get_text().strip()
        try:
            author=soup.select('#main > main > section.main-well.js-mainWell > article > div.article__details > p.article__meta.article__meta--below-media > span.js-authors-list > span > a')[0].get_text().strip()
        except:
            author=soup.select('#main > main > section.main-well.js-mainWell > article > div.article__header > p.article__meta > span.js-authors-list > span > a')[0].get_text().strip()
        first,last=author.split()[0],author.split()[1]
        date=time.strftime('%b %d, %Y', time.strptime(date,'%m/%d/%Y'))
        accessdate=time.strftime('%b %d, %Y', time.gmtime(time.time()))
        final='<ref>{{cite web|url='+url+'|title='+title+'|first='+first+'|last='+last+'|date='+date+'|accessdate='+accessdate+'|publisher=[[Billboard (magazine)|Billboard]]}}</ref>'
        print(final)

        endtime = time.time()
        dtime = endtime - starttime
        print("All processes were done in %.3f second(s)." % dtime)

    def edm(self,url):
        '''
        Fetch content from www.edm.com.
        '''
        starttime = time.time()

        r = requests.get(url)
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text,'html.parser')
        title=soup.select('#lyra-wrapper > div > div.m-advertisement-off-canvas--pusher > section > div.m-page.m-detail.mm-detail.mm-feature > section.m-component-detail > article > div > header > div > div > h1')[0].get_text()
        author=soup.select('#lyra-wrapper > div > div.m-advertisement-off-canvas--pusher > section > div.m-page.m-detail.mm-detail.mm-feature > section.m-component-detail > article > div > header > div > div > div.m-detail-header--meta > dl > dd:nth-child(2) > a')[0].get_text()
        date=soup.find('time').get('title')
        first,last=author.split()[0],author.split()[1]
        date=time.strftime('%b %d, %Y', time.strptime(date,'%Y-%m-%dT%H:%M:%SZ'))
        accessdate=time.strftime('%b %d, %Y', time.gmtime(time.time()))        
        final='<ref>{{cite web|url='+url+'|title='+title+'|first='+first+'|last='+last+'|date='+date+'|accessdate='+accessdate+'|website=edm.com}}</ref>'
        print(final)

        endtime = time.time()
        dtime = endtime - starttime
        print("All processes were done in %.3f second(s)." % dtime)

    def pitchfork_news(self,url):
        '''
        Fetch the news from www.pitchfork.com.
        '''
        starttime = time.time()

        r = requests.get(url)
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text,'html.parser')
        author=soup.select('#news-detail-page > div > div.clearfix > div > article > div > div.article-meta.article-meta--news > div:nth-child(2) > ul.authors-detail > li > div > a')[0].get_text()
        title=soup.select('#news-detail-page > div > div.clearfix > div > article > div > div.article-content > div > div:nth-child(1) > header > h1')[0].get_text()
        date=soup.find('time').get('datetime')
        first,last=author.split()[0],author.split()[1]
        date=time.strftime('%b %d, %Y', time.strptime(date,'%Y-%m-%dT%H:%M:%S'))
        accessdate=time.strftime('%b %d, %Y', time.gmtime(time.time()))        
        final='<ref>{{cite web|url='+url+'|title='+title+'|first='+first+'|last='+last+'|date='+date+'|accessdate='+accessdate+'|publisher=[[Pitchfork (website)|Pitchfork]]}}</ref>'
        print(final)

        endtime = time.time()
        dtime = endtime - starttime
        print("All processes were done in %.3f second(s)." % dtime)
