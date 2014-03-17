#import BeautifulSoup                             
import urllib,urllib2,re,xbmcplugin,xbmcgui
#import locale

#locale.setlocale(locale.LC_ALL, 'slovenian')

#http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=A
#http://tvslo.si/?c_mod=play&op=videonews&func=videonews&group=all&page=0
#http://tvslo.si/?c_mod=play&op=recommended&func=recommended&page=0
#http://tvslo.si/?c_mod=play&op=zadnje&func=zadnje&page=tv
#http://tvslo.si/?c_mod=play&op=search&func=search&search_text=&search_media=tv&search_type=&search_extid=39&search_orderby=date
#http://motherjones.com/files/images/PodcastLogo.png
#http://3.bp.blogspot.com/_QfXGjzBR4dk/SwMtLgNjxAI/AAAAAAAAAFo/Dp7ShIt1Y2s/s1600/rss%2Bpodcast%2Bmax%2Bversion.jpg
#http://earthonline.files.wordpress.com/2009/12/rss-icon.jpg
#http://jeasolar.com/joomla1/images/stories/radio%2520tower.png
#http://www.iconarchive.com/icons/icontoaster/icons-10-bundle/256/location-news-icon.png
#http://www.veryicon.com/icon/png/System/Crystal%2520Clear%2520Actions/Update%2520Recommended.png

#zaèetna izbira
def CATEGORIES():
        addDir('Audio Podcasts','http://www.rtvslo.si/podcast/',1,'http://img.rtvslo.si/upload/aktualno/podcast-mali_show.gif')
        addDir('Video Podcasts','http://www.rtvslo.si/podcast/',2,'http://img.rtvslo.si/upload/aktualno/podcast-mali_show.gif')
        addDir('RSS Feeds','',14,'http://img.rtvslo.si/upload/aktualno/rss-mali2_1_show.gif')
        addDir('V Živo','',9,'http://img.rtvslo.si/upload/aktualno/p2p_show.gif')
        addDir('Priporočamo','http://tvslo.si/?c_mod=play&op=recommended&func=recommended&group=all&page=0',15,'http://userserve-ak.last.fm/serve/252/5094398.png')
        addDir('Videonovice','',16,'http://userserve-ak.last.fm/serve/252/5094398.png')
        addDir('Zadnje Oddaje','',17,'http://userserve-ak.last.fm/serve/252/5094398.png')
        addDir('Oddaje po zvrsti','',12,'http://userserve-ak.last.fm/serve/252/5094398.png')
        addDir('Oddaje po abecedi','',19,'http://userserve-ak.last.fm/serve/252/5094398.png')
        addDir('Hitro Iskanje','',3,'http://userserve-ak.last.fm/serve/252/5094398.png')


#audio podcast
def AudioPod(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="http://www.rtvslo.si/podcasts/(.+?).xml"><img border="0" src="(.+?)"').findall(link)
        for name,img in match:
                if img == audiopng:
                        addDir(name,'http://www.rtvslo.si/podcasts/'+name+'.xml',5,img)
#                        addDir(name,'http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group='+name,5,img)

#video podcast
def VideoPod(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="http://www.rtvslo.si/podcasts/(.+?).xml"><img border="0" src="(.+?)"').findall(link)
        for name,img in match:
                if img != audiopng:
                        addDir(name,'http://www.rtvslo.si/podcasts/'+name+'.xml',5,img)

#linki do podcast videov
def Podcast(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        match=re.compile('<item> <title>(.+?)</title><description>(.+?)</description><itunes:subtitle>.+?</itunes:subtitle><itunes:summary>.+?</itunes:summary><pubDate>.+?</pubDate><itunes:duration>.+?</itunes:duration> <guid isPermaLink="false">.+?</guid><enclosureurl=".+?"length=".+?"type=".+?"/><media:content url="(.+?)"fileSize=".+?"type=".+?" expression=".+?"duration=".+?" bitrate=".+?"/> </item>').findall(code)
        for name, plot, url in match:	           
                addLink(name,url,plot,'')


def Iskanje():
        addDir('NOVO ISKANJE','',3,'')
#        addDir('Išči: '+str,str,22,'')
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
                str = keyboard.getText()
                url = 'http://tvslo.si/?c_mod=play&op=search&func=search&search_text='+str+'&search_media=&search_type=&search_orderby=date&page=0'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                Vecposnetkov(url)
#                addDir('Išči: '+str,ISK,22,'')


def RSS(url,icon):
        addDir('NAZAJ NA MENI','',None,'')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        code=re.sub('&amp;','&',code)
        match=re.compile('<title>(.+?)</title>').findall(code)
        match=re.compile('<item> <title>(.+?)</title> <pubDate>(.+?), (.+?) (.+?) (.+?) .+? .+?</pubDate> <link>(.+?)</link>').findall(code) # <description><![CDATA[ Prvi in drugi ]]></description></item><item>').findall(code)
        for name, dan, dat, mesec, leto,url in match:
                print name
                date = dan+', '+dat+'.'+mesec+'.'+leto
                print date
                print url
                match=re.compile('<link>(.+?)</link>').findall(code)
                idnt = url.replace('http://www.rtvslo.si','')
                idnt = idnt.replace('/rss/','')
                idnt = idnt.replace('/play/?id=ava2.','')
                print idnt
                xmlplaylist = 'http://www.rtvslo.si/media.php?id='+idnt+'&mt=flv&mq=hi&wm=true&rm=false&file=playlist.xml'
                req = urllib2.Request(xmlplaylist)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<location>(.+?)</location>').findall(link)
                for playpath in match:
#                    print playpath
                        match=re.compile('.mp(\d+?)').findall(playpath)
                for codec in match:
                        print codec
                if codec == '3':
                        playpath = playpath.replace('.mp3','')    
                        playpath = 'mp3:'+playpath
                        if icon == '':
                                icon = 'http://tvslo.si/_static/img/play/ico-nislike-avdio.gif'
                elif codec == '4':
                        playpath = 'mp4:'+playpath
                        if icon == '':
                                icon = 'http://tvslo.si/_static/img/play/ico-nislike-video.gif'
                addFlash(name+' dne: '+date,playpath,'',icon)
                

def Videonovice():
        addDir('Skupne','http://www.rtvslo.si/feeds/video-videonovice.xml',7,'')
        addDir('Novice','http://www.rtvslo.si/feeds/video-videonovice-glavni.xml',7,'')
        addDir('Šport','http://www.rtvslo.si/feeds/video-videonovice-sport.xml',7,'')
        addDir('Kultura','http://www.rtvslo.si/feeds/video-videonovice-kultura.xml',7,'')
        addDir('Zabava','http://www.rtvslo.si/feeds/video-videonovice-zabava.xml',7,'')

def Live():
        addDir('TV','',10,'http://www.thevictoryformation.com/wp-content/uploads/2011/02/IdiotBox.jpg')
        addDir('Radio','',11,'http://www.marketingmagazin.si/images/custom//radio.jpg')

def TV():
        addFlashLive('TV Slovenija 1','slo1','','http://img.rtvslo.si/upload/staticna/tvslo1-logo_show.gif')
        addFlashLive('TV Slovenija 2','slo2','','http://img.rtvslo.si/upload/staticna/tvslo2-logo_show.gif')
        addFlashLive('TV Slovenija 3','slo3','','http://img.rtvslo.si/upload/staticna/tvslo3-logo_show.gif')
        addFlashLive('TV Koper-Capodistria','tvkp','','')
        addFlashLive('TV Maribor','tvmb','','')
        addFlashLive('MMC','mmctv','','')

def Radio():
#        addLink('Prvi Program','mms://helix10.rtvslo.si/wmtencoder/ra.a1.wma','http://img.rtvslo.si/_up/upload/2010/11/16/64743978_radioprvi_show.gif','')
#        addLink('Val 202','mms://helix10.rtvslo.si/wmtencoder/val202.wma','http://img.rtvslo.si/upload/staticna/val202.png','')
#        addLink('Ars','mms://helix10.rtvslo.si/wmtencoder/ars.wma','http://img.rtvslo.si/upload/staticna/ars_show.gif','')
#        addLink('Maribor','mms://helix10.rtvslo.si/wmtencoder/mb1.wma','','')
#        addLink('Rsi','mms://helix10.rtvslo.si/wmtencoder/rsi.wma','','')
#        addLink('Koper','mms://helix10.rtvslo.si/wmtencoder/kp.wma','','')
#        addLink('Capodistria','mms://helix10.rtvslo.si/wmtencoder/capo.wma','','')
#        addLink('MMR','mms://helix10.rtvslo.si/wmtencoder/mmr.wma','','')
        addFlashLive('Prvi Program','ra1','Prvi Program','http://img.rtvslo.si/_up/upload/2010/11/16/64743978_radioprvi_show.gif')
        addFlashLive('Val 202','val202','Val 202','http://img.rtvslo.si/upload/staticna/val202.png')
        addFlashLive('Ars','ars','Ars','http://img.rtvslo.si/upload/staticna/ars_show.gif')
        addFlashLive('Radio Si International','rsi','Radio Si International','')
        addFlashLive('Radio Maribor','rmb','Maribor','')
        addFlashLive('Radio Koper','rakp','Koper','')
        addFlashLive('Radio Capodistria','capo','Capodistria','')
        addFlashLive('MMR','mmr','MMR','')

def OddajeZvrst():
        addDir('Vse','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=all&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_vse.gif')
        addDir('Informativne','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=3&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_informativne.gif')
        addDir('Izobraževalne','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=4&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_izobrazevalne.gif')
        addDir('Kulturno umetniške','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=7&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_kulturne.gif')
        addDir('Otroške in mladinske','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=6&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_otroske.gif')
        addDir('Razvedrilne','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=1&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_razvedrilne.gif')
        addDir('Športne','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=2&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_sportne.gif')
        addDir('Verske','http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group=5&page=0',13,'http://img.rtvslo.si/_static/img/play/plr_verske.gif')

def Oddaje(url):
        addDir('NAZAJ NA MENI','',None,'')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        code=re.sub('&amp;','&',code)
        match=re.compile('<img height=".+?" width=".+?" src="(.+?)" alt=""/></a></div> <div style=".+?"><div class=".+?"><div class=".+?"></div></div></div> </div><div align=".+?" style=".+?"> <div style=".+?">(.+?)</div> <p><a href=".+?" onclick="search_play\(\'ava2.(.+?)\'\); return false;"><b>.+?</a></b></p> <small>(.+?)</small>').findall(code)
#print code
        for image, name, idn, date in match:
                if image[0] == '/':
                    icon = 'http://www.rtvslo.si/'+image
                else:
                    icon = image    
                xmlplaylist = 'http://www.rtvslo.si/media.php?id='+idn+'&mt=flv&mq=hi&wm=true&rm=false&file=playlist.xml'
                req = urllib2.Request(xmlplaylist)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<location>(.+?)</location>').findall(link)
        #                for playpath in match:
                for playpath in match:
                    match=re.compile('.mp(\d+?)').findall(playpath)
                for codec in match:
                        print codec
                if codec == '3':
                    playpath = playpath.replace('.mp3','')    
                    playpath = 'mp3:'+playpath
                elif codec == '4':
                    playpath = playpath.replace('.mp4','')
                    playpath = 'mp4:'+playpath
         #       print name
                addFlash(name+' '+date,playpath,'',icon)  
        match=re.compile('&func=(.+?)&group=(.+?)&page=(\d+.?\d*)').findall(url)
        for func, grp, pg in match:
                print func
                print grp
                pg = int(pg) + 1
                page = int(pg) + 1
                site = 'http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group='+grp+'&page='+str(pg)
                print site
        addDir('STRAN: '+str(page),'http://tvslo.si/?c_mod=play&op=oddaje&func=oddaje&group='+grp+'&page='+str(pg),13,'http://www.clker.com/cliparts/3/f/f/d/1194985689770236807arrow_-_next_01.svg.hi.png')
        
def RSSFeeds():
        addDir('Priporočamo','http://www.rtvslo.si/feeds/video-priporocamo.xml',7,'')
        addDir('Videonovice','',8,'')

        

def Priporocamo(url):
        addDir('NAZAJ NA MENI','',None,'http://userserve-ak.last.fm/serve/252/5094398.png')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        code=re.sub('&amp;','&',code)
        match=re.compile('<img height=".+?" width=".+?" src="(.+?)" alt=""/></a></div> <div class=".+?"><div class=".+?"><div class=".+?"></div></div></div> </div><div align=".+?" style=".+?"> <div class=".+?"></div> <p><a href=".+?" onclick="search_play\(\'ava2.(.+?)\'\); return false;"><b>(.+?)</b></a></p> <small><b>.+?</b>(.+?)</small>').findall(code)
#print code
        for image, idn, name, date in match:
                if idn.count('return false'):
                    idn = idn[0:9]
                if  len(idn) >= 10:  
                    idn = idn+"'"
                    print idn
                    match = re.compile("(.+?)','(.+?)','(.+?)'").findall(idn)
                    for idn, start, stop in match:
                        start = (int(start[0])*10 + int(start[1]))*3600 + (int(start[3])*10 + int(start[4]))*60 + (int(start[6])*10 + int(start[7]))
                        start = int(start)*1000
                        stop = (int(stop[0])*10 + int(stop[1]))*3600 + (int(stop[3])*10 + int(stop[4]))*60 + (int(stop[6])*10 + int(stop[7]))
                        stop = int(stop)*1000
                        print start
                        print stop
                    if start == stop:
                        stop = ''
                        print 'dela'
                else:
                        start = ''
                        stop = ''
                xmlplaylist = 'http://www.rtvslo.si/media.php?id='+idn+'&mt=flv&mq=hi&wm=true&rm=false&file=playlist.xml'
                req = urllib2.Request(xmlplaylist)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<location>(.+?)</location>').findall(link)
                for playpath in match:
                        match=re.compile('.mp(\d+?)').findall(playpath)
                for codec in match:
                        print codec
                if codec == '3':
                        playpath = playpath.replace('.mp3','')    
                        playpath = 'mp3:'+playpath
                elif codec == '4':
                        playpath = 'mp4:'+playpath
                else:
                        None
                playpath = playpath + ' start='+str(start)+' stop='+str(stop)
                print playpath
                print start
                addFlash(name+' '+date,playpath,'',image)
        match=re.compile('&func=(.+?)&group=(.+?)&page=(\d+.?\d*)').findall(url)
        for func, grp, pg in match:
                pg = int(pg) + 1
                page = int(pg) + 1
        addDir('STRAN: '+str(page),'http://tvslo.si/?c_mod=play&op='+func+'&func='+func+'&group='+grp+'&page='+str(pg),15,'http://www.clker.com/cliparts/3/f/f/d/1194985689770236807arrow_-_next_01.svg.hi.png')
        
#            print url             
    
def ZadOd(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        code=re.sub('&amp;','&',code)
        match=re.compile('<img height=".+?" width=".+?" src="(.+?)" alt=""/></a></div></div><div align=".+?" style=".+?"> <p><a href=".+?" onclick="search_play\(\'ava2.(.+?)\'\); return false;"><b>(.+?)</b></a></p> <small>(.+?)</small>').findall(code)
        #print code
        for image, idn, name, date in match:
            if image[0] == '/':
                icon = 'http://www.rtvslo.si/'+image
            else:
                icon = image    
            xmlplaylist = 'http://www.rtvslo.si/media.php?id='+idn+'&mt=flv&mq=hi&wm=true&rm=false&file=playlist.xml'
            req = urllib2.Request(xmlplaylist)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('<location>(.+?)</location>').findall(link)
            for playpath in match:
                    match=re.compile('.mp(\d+?)').findall(playpath)
            for codec in match:
                    print codec
            if codec == '3':
                    playpath = playpath.replace('.mp3','')   
                    playpath = 'mp3:'+playpath
            elif codec == '4':
                    playpath = 'mp4:'+playpath
            else:
                    None
            print playpath
            addFlash(name+' '+date,playpath,'',image)
               
def Videonews():
        addDir('Skupne','http://tvslo.si/?c_mod=play&op=videonews&func=videonews&group=all&page=0',15,'http://img.rtvslo.si/_static/img/play/plr_skupno_on.gif')
        addDir('Novice','http://tvslo.si/?c_mod=play&op=videonews&func=videonews&group=condor&page=0',15,'http://img.rtvslo.si/_static/img/play/plr_novice.gif')
        addDir('Šport','http://tvslo.si/?c_mod=play&op=videonews&func=videonews&group=sport&page=0',15,'http://img.rtvslo.si/_static/img/play/plr_sport.gif')
        addDir('Kultura','http://tvslo.si/?c_mod=play&op=videonews&func=videonews&group=kultura&page=0',15,'http://img.rtvslo.si/_static/img/play/plr_kultura.gif')
        addDir('Zabava','http://tvslo.si/?c_mod=play&op=videonews&func=videonews&group=zabava&page=0',15,'http://img.rtvslo.si/_static/img/play/plr_zabava.gif')
        
def Zadnje():
        addDir('TV','http://tvslo.si/?c_mod=play&op=zadnje&func=zadnje&page=tv',18,'http://www.thevictoryformation.com/wp-content/uploads/2011/02/IdiotBox.jpg')
        addDir('Radio','http://tvslo.si/?c_mod=play&op=zadnje&func=zadnje&page=ra',18,'http://www.marketingmagazin.si/images/custom//radio.jpg')


def ABCOddaje():
        addDir('Vse','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=vse',20,'')
	addDir('0-9','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=0-9',20,'')
	addDir('A','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=A',20,'')
	addDir('B','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=B',20,'')
	addDir('C','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=C',20,'')
	addDir('Č','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=3',20,'')
	addDir('D','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=D',20,'')
	addDir('E','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=E',20,'')
	addDir('F','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=F',20,'')
	addDir('G','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=G',20,'')
	addDir('H','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=H',20,'')
	addDir('I','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=I',20,'')
	addDir('J','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=J',20,'')
	addDir('K','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=K',20,'')
	addDir('L','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=L',20,'')
	addDir('M','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=M',20,'')
	addDir('N','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=N',20,'')
	addDir('O','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=O',20,'')
	addDir('P','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=P',20,'')
	addDir('R','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=R',20,'')
	addDir('S','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=S',20,'')
	addDir('Š','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=19',20,'')
	addDir('T','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=T',20,'')
	addDir('U','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=U',20,'')
	addDir('V','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=V',20,'')
	addDir('Z','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=Z',20,'')
	addDir('Ž','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=24',20,'')
	addDir('Ostalo','http://tvslo.si/?c_mod=play&op=oddaje&func=abcOddaje&group=ostalo',20,'')

def AVAOddaje(url):
        addDir('NAZAJ NA MENI','',None,'')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        code=re.sub('&amp;','&',code)
        match=re.compile('loadItem\(\'(.+?)\',\'(.+?)\',\'(.+?)\'\);" href="javascript:void\(0\);">(.+?)</a>').findall(code)
        for ava_id, media, show_id, name in match:
#                print ava_id
#                print show_id
#                print name
                url = 'http://tvslo.si/?c_mod=play&op=oddaje&func=ava2arhiv&media='+media+'&ava_id='+ava_id+'&show='+show_id+'&page=0'
                addDir(name,url,21,'')
                
                
def Oddaja(url):
        addDir('NAZAJ NA MENI','',None,'')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"id":"(\d+?)","title":"(.+?)","date":"(.+?)"').findall(link)
        for idnt, name, date in match:
#                print idnt
#                print name
                name = name.replace('\u017d','Ž')
                name = name.replace('\u017e','ž')
                name = name.replace('\u010d','č')
                name = name.replace('\u0160','Š')
                name = name.replace('\u0161','š')
                name = name.replace('\u010c','Č')
                xmlplaylist = 'http://www.rtvslo.si/media.php?id='+idnt+'&mt=flv&mq=hi&wm=true&rm=false&file=playlist.xml'
                req = urllib2.Request(xmlplaylist)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<location>(.+?)</location>').findall(link)
                for playpath in match:
                        if len(playpath) == 14:
                                link = 'http://www.rtvslo.si/media.php?id='+idnt+'&mt=wm&mq=hi&wm=true&rm=true'
                                req = urllib2.Request(link)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                #print link
                                match=re.compile('<ref href="(.+?)"/>').findall(link)
                                for playpath in match:
                                        print playpath
                                addLink(name+' '+date,playpath,plot,'')

                        else:
                                match=re.compile('.mp(\d+?)').findall(playpath)                     
                                for codec in match:
                                        None
 #                                       print codec
                                        if codec == '3':
                                                playpath = playpath.replace('.mp3','')    
                                                playpath = 'mp3:'+playpath
                                        elif codec == '4':
                                                playpath = 'mp4:'+playpath
                                        else:
                                                None
#                                print playpath
                                addFlash(name+' '+date,playpath,'','')
#                test = 'http://tvslo.si/?c_mod=play&op=search&func=search&search_text=&search_media='+media+'&search_type=&search_extid='+show_id+'&search_orderby=date'
                print url
                match=re.compile('&media=(.+?)&ava_id=.+?&show=(.+?)&page=0').findall(url)
        for media, show_id in match:
                print media
                print show_id
                addDir('VEČ POSNETKOV','http://tvslo.si/?c_mod=play&op=search&func=search&search_text=&search_media='+media+'&search_type=&search_extid='+show_id+'&search_orderby=date&page=0',22,'http://www.clker.com/cliparts/3/f/f/d/1194985689770236807arrow_-_next_01.svg.hi.png')

def Vecposnetkov(url):
        addDir('NAZAJ NA MENI','',None,'')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        code=re.sub('&lt;','',code)
        code=re.sub('/&gt;','',code)
        code=re.sub('&amp;','&',code)
        match=re.compile('<a href=".+?" onClick="search_play\(\'ava2.(.+?)\'\); return false;" title="(.+?)" style=".+?">(.+?)</a></td><td width=".+?" class=".+?">(.+?)</td>').findall(code)
#print code
        for idnt, plot, name, date in match:
                name = name.replace('\u017d','Ž')
                name = name.replace('\u017e','ž')
                name = name.replace('\u010d','č')
                name = name.replace('\u0160','Š')
                name = name.replace('\u0161','š')
                name = name.replace('\u010c','Č')
                xmlplaylist = 'http://www.rtvslo.si/media.php?id='+idnt+'&mt=flv&mq=hi&wm=true&rm=false&file=playlist.xml'
                req = urllib2.Request(xmlplaylist)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<location>(.+?)</location>').findall(link)
                for playpath in match:
                        if len(playpath) == 14:
                                link = 'http://www.rtvslo.si/media.php?id='+idnt+'&mt=wm&mq=hi&wm=true&rm=true'
                                req = urllib2.Request(link)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                #print link
                                match=re.compile('<ref href="(.+?)"/>').findall(link)
                                for playpath in match:
                                        print playpath
                                addLink(name+' '+date,playpath,plot,'')
                        else:

                                match=re.compile('.mp(\d+?)').findall(playpath)
                                for codec in match:
                                        print codec
                                if codec == '3':
                                        playpath = playpath.replace('.mp3','')    
                                        playpath = 'mp3:'+playpath
                                elif codec == '4':
                                        playpath = 'mp4:'+playpath
                                else:
                                        None
                                print playpath
                                addFlash(name+' '+date,playpath,plot,'')
        text = ''
        match=re.compile('&search_text=(.+?)&search_media=&search_type=&search_orderby=date&page=(.+?)').findall(url)
        for text, pg in match:
                pg = int(pg) + 1
                print text
                url = 'http://tvslo.si/?c_mod=play&op=search&func=search&search_text='+text+'&search_media=&search_type=&search_orderby=date&page='+str(pg)
        match=re.compile('&search_media=(.+?)&search_type=&search_extid=(.+?)&search_orderby=date&page=(\d+.?\d*)').findall(url)
        for media, show_id, pg in match:
                print text
                print media
                print show_id
                print pg
                pg = int(pg) + 1
                print pg
                url = 'http://tvslo.si/?c_mod=play&op=search&func=search&search_text='+text+'&search_media='+media+'&search_type=&search_extid='+show_id+'&search_orderby=date&page='+str(pg)
                print url
        addDir('STAREJŠI POSNETKI',url,22,'http://www.clker.com/cliparts/3/f/f/d/1194985689770236807arrow_-_next_01.svg.hi.png')
 

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,plot,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://www.rtvslo.si/podcasts/mmc.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addFlash(name,playpath,plot,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://www.rtvslo.si/podcasts/mmc.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot":  plot} )
        finalUrl = videoUrl + '?slist='+playpath+' swfUrl='+swfUrl
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=finalUrl,listitem=liz)

def addFlashLive(name,playpath,plot,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://www.rtvslo.si/podcasts/mmc.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot":  plot} )
        finalUrl = videoUrl + '/live/ app=live  playpath='+playpath+' swfUrl='+swfUrl+' live=True'
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=finalUrl,listitem=liz)
        print finalUrl
#        ok=xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(finalUrl, listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
#listItem=xbmcgui.ListItem("Test");
#
#playpath= "23/2/Sportob22hx201101112237x700000x351x413x.mp4"
#videoUrl = "rtmp://fms.rtvslo.si/vod/"
#finalUrl = videoUrl + ' app=vod  playpath=mp4:'+playpath + ' swfUrl= http://tvslo.si/media_player.swf'
#
#xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(finalUrl, listItem)
#              
#



params=get_params()
plot = 'Oddaje iz arhiva MMC RTV Slovenije'
Codec = None
finalUrl = None
url=None
name=None
mode=None
img=None
date=''
ava_id=str()
media=None
videoUrl = "rtmp://ios.rtvslo.si/simplevideostreaming32"
swfUrl = 'http://tvslo.si/media_jwplayer_5.7.swf'

audiopng = 'http://img.rtvslo.si/modules/content/videopodcast/img/podcast.gif'
housepng = "http://img.rtvslo.si/modules/content/kazalo/icons/spletnastran-icon.gif"
icon = ''

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or 0: 
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        AudioPod(url)

elif mode==2:
        print ""+url
        VideoPod(url)
        
elif mode==3:
        print ""
        Iskanje()
        
elif mode==5:
        print ""+url
        Podcast(url,name)

elif mode==7:
        print ""+url
        RSS(url,icon)

elif mode==8: 
        print ""
        Videonovice()

elif mode==9: 
        print ""
        Live()

elif mode==10: 
        print ""
        TV()

elif mode==11: 
        print ""
        Radio()

elif mode==12: 
        print ""
        OddajeZvrst()

elif mode==13: 
        print ""
        Oddaje(url)
        
elif mode==14: 
        print ""
        RSSFeeds()

elif mode==15: 
        print ""
        Priporocamo(url)

elif mode==16: 
        print ""
        Videonews()

elif mode==17: 
        print ""
        Zadnje()

elif mode==18: 
        print ""
        ZadOd(url)

elif mode==19: 
        print ""
        ABCOddaje()

elif mode==20: 
        print ""
        AVAOddaje(url)

elif mode==21: 
        print ""
        Oddaja(url) 

elif mode==22: 
        print ""
        Vecposnetkov(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
