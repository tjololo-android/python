 1、音乐地址
     经过分析，页面嵌入的虾米播放器中的地址如下，后面以逗号分隔的字符为音乐的id，如音乐的地址为http://www.xiami.com/song/2088578
<span style="font-size:14px;"><span style="font-size:14px;">   <embed src="http://www.xiami.com/widget/0_2088578,163414,603408,1769697211,1519594,1944911,1769482546,1771498226,2050705,1769213208,2957497,  
    1769779902,1769897948,1770077250,1771638197,109133,1769220090,3469026,2456779,3673869,385167,1769528393,1770130506,1014582,3418745,1769554460,  
    1769692638,1279925,1769582513,136064,1769528375,1769455237,1769075782,2095209,1770618381,3427512,2108249,1771186364,2087541,1769384565,1770432131,  
    2149137,2083819,1768911382,3429194,2089207,1770177060,1770427913,1769279049,2089339,2085205,3437055,3646041,2070983,2070741,3619123,1770068122,  
    2082956,2071004,1768679,1769683697,3567557,109133,1769572701,2152946,3489617,1770292731_235_346_FF8719_494949_1/multiPlayer.swf" type="application/x-shockwave-flash"  
    width="235" height="320" wmode="opaque"></embed></span></span>  
    
2、获取所有音乐的id，形成列表
   
[html] view plain copy
<span style="font-size:14px;"><span style="font-size:14px;">    dexiazai_url="http://www.dexiazai.com/?page_id=23"  
    req=urllib2.Request(dexiazai_url, headers={  
    'Connection': 'Keep-Alive',  
    'Accept': 'text/html, application/xhtml+xml, */*',  
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
    })  
    response=urllib2.urlopen(req)  
    content=response.read().decode('utf-8')  
    pattern=re.compile('<embed.*?src="http://www.xiami.com/widget/0_(.*?)/multiPlayer.swf"',re.S)  
    ids=re.search(pattern,content).group(1)  
    idarr=ids.split(",")  
     
     
</span></span>  

<span style="font-size:14px;"><span style="font-size:14px;">        url="http://www.xiami.com/song/"+str(idarr[i])  
        print("==================num: "+str(i)+"=======================")  
        print(url)     
        #获取歌词名  
        req=urllib2.Request(url, headers={  
        'Connection': 'Keep-Alive',  
        'Accept': 'text/html, application/xhtml+xml, */*',  
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
        })  
        rep=urllib2.urlopen(req)  
        cont=rep.read().decode('utf-8')  
        pat=re.compile('<div.*?id="title">(.*?)</h1>', re.S)  
        fname=re.search(pat,cont).group(1)  
        fname=fname.strip().lstrip().rstrip().replace('<h1>','')  
        #J'Ai Deux Amours转码为J'Ai Deux Amours  
        fname=html.parser.unescape(fname)  
        fname=fname.split("<a target")[0]  
        fname=str(i+1)+"_"+fname  
  
     4、附上所有代码  
    </span><pre name="code" class="html"><span style="font-size:14px;"># -*- coding: utf-8 -*-  
                              
import re  
import urllib.request as urllib2  
import html.parser  
                              
class XiamiDownload(object):  
                              
    """虾米音乐下载"""  
                              
    def __init__(self, url_song):  
                              
        """ 初始化，得到请求xml和加密的下载地址 """  
                              
        self.url_song = url_song         
        self.url_xml = self.__get_xml()  
        self.info = self. __get_info()  
        self.url_location = self.info[0]  
        self.lyc = self.info[1]  
        self.pic = self.info[2]  
                                  
    def __get_xml(self):  
                              
        """ 得到请求的 xml 地址 """  
                              
        return 'http://www.xiami.com/song/playlist/id/%s/object_name/default/object_id/0' % re.search('\d+', self.url_song).group()  
                              
    def __get_info(self):  
                              
        """ 伪装浏览器请求，处理xml，得到 加密的 location """  
                              
        headers = {  
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
        }  
        req = urllib2.Request(  
            url = self.url_xml,  
            headers = headers  
        )  
        try:  
            xml = urllib2.urlopen(req).read().decode('utf-8')  
            #print("xml:"+xml)  
            pattern_location=re.compile('<location>(.*?)</location>',re.S)  
            location = re.search(pattern_location, xml).group(1)  
            #print("location:"+location)  
            lyc_location=re.compile('<lyric>(.*?)</lyric>',re.S)  
            lyc = re.search(lyc_location, xml).group(1)   
            pic_location=re.compile('<pic>(.*?)</pic>',re.S)  
            pic = re.search(pic_location, xml).group(1)   
            return (location, lyc, pic)  
        except:  
            return("exception","exception","exception")  
                              
    def get_url(self):  
                              
        """ 解密 location 获得真正的下载地址 """  
                              
        strlen = len(self.url_location[1:])  
        rows = int(self.url_location[0])  
        cols = strlen // rows  
        right_rows = strlen % rows  
        new_str = self.url_location[1:]   
        url_true = ''  
        #print(strlen)                      
        for i in range(strlen):  
            x = i % rows  
            y = i / rows  
            p = 0  
            if x <= right_rows:  
                p = x * (cols + 1) + y  
            else:  
                p = right_rows * (cols + 1) + (x - right_rows) * cols + y  
            #print(p)  
            url_true += new_str[int(p)]  
            #print(url_true)  
        return urllib2.unquote(url_true).replace('^', '0')  
      
          
                              
if __name__ == '__main__':  
                             
    dexiazai_url="http://www.dexiazai.com/?page_id=23"  
    req=urllib2.Request(dexiazai_url, headers={  
    'Connection': 'Keep-Alive',  
    'Accept': 'text/html, application/xhtml+xml, */*',  
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
    })  
    response=urllib2.urlopen(req)  
    content=response.read().decode('utf-8')  
    pattern=re.compile('<embed.*?src="http://www.xiami.com/widget/0_(.*?)/multiPlayer.swf"',re.S)  
    ids=re.search(pattern,content).group(1)  
    idarr=ids.split(",")  
    for i in range(len(idarr)-1):  
        url="http://www.xiami.com/song/"+str(idarr[i])  
        print("==================num: "+str(i)+"=======================")  
        print(url)     
        #获取歌词名  
        req=urllib2.Request(url, headers={  
        'Connection': 'Keep-Alive',  
        'Accept': 'text/html, application/xhtml+xml, */*',  
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'  
        })  
        rep=urllib2.urlopen(req)  
        cont=rep.read().decode('utf-8')  
        pat=re.compile('<div.*?id="title">(.*?)</h1>', re.S)  
        fname=re.search(pat,cont).group(1)  
        fname=fname.strip().lstrip().rstrip().replace('<h1>','')  
        #J'Ai Deux Amours转码为J'Ai Deux Amours  
        fname=html.parser.unescape(fname)  
        fname=fname.split("<a target")[0]  
        fname=str(i+1)+"_"+fname  
        print("歌曲名为： "+fname+"  开始下载")  
        xi = XiamiDownload(url)  
        if xi.url_location=="exception":  
            continue  
        url_download = xi.get_url()  
        url_pic = xi.pic  
        url_lyc = xi.lyc  
                                  
        print ('下载地址是: ' +url_download)  
                                  
        try:  
            urllib2.urlretrieve(url_download, fname+'.mp3')  
            urllib2.urlretrieve(url_pic, fname+'.jpg')  
            urllib2.urlretrieve(url_lyc, fname+'.lyc')  
        except:  
            continue  
                                      
        print ("完成下载...")  
  
  
</span></span>      