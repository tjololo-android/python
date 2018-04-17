import requests
import json
import os
import time

base_dir = 'd:/music/'

def get(url):
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
        "Accept-Encoding":"gzip",
        "Accept-Language":"zh-CN,zh;q=0.8",            
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
    }    
    times = 10
    while times:
        times -= 1
        try:
            response = requests.get(url,headers=headers) 
            if response.status_code == 200:
                return response
        except Exception, e:
            time.sleep(5)
            print e
    
def down(word):
    url1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w='
    url2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='
    url3 = 'http://dl.stream.qqmusic.qq.com/C400'
    
    print 'start download json'
    res1 = get(url1+word)    
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']['song']['list']
    mids = []
    songmids = []
    srcs = []
    songnames = []
    singers = []
    for j in jm1:
        try:
            mids.append(j['media_mid'])
            songmids.append(j['songmid'])
            songnames.append(j['songname'])
            singers.append(j['singer'][0]['name'])
        except:
            print('wrong') 
            return

    for n in range(0,len(mids)):
        print 'start download vkey'
        res2 = get(url2+songmids[n]+'&filename=C400'+mids[n]+'.m4a&guid=6612300644')
        time.sleep(5)
        jm2 = json.loads(res2.text)
        vkey = jm2['data']['items'][0]['vkey']
        srcs.append(url3+mids[n]+'.m4a?vkey='+vkey+'&guid=6612300644&uin=0&fromtag=66')
        break

    x = len(srcs)
    for m in range(0,x):
        print(str(m)+'***** '+songnames[m]+' - '+singers[m]+'.m4a *****'+' Downloading...')         
        p = base_dir +songnames[m]+' - '+singers[m]+'.m4a'
        if os.path.exists(p):
            return
        print 'start download ' + songnames[m]                
        response = get(srcs[m])
        if not response:
            return
        with open(p, 'wb') as f:
            f.write(response.content)        
        print 'download ' + songnames[m] + ' successful!'
        return

def main(): 
    requests.adapters.DEFAULT_RETRIES = 5 
    names = os.listdir(base_dir)
    names = [i[:i.find('-')].strip() for i in names]    
    names = [i.decode('gb2312').strip() for i in names]
    try:
        with open('songs.txt', 'r') as f:            
            for w in f:                
                w = w.decode('utf-8').strip()
                if w in names:
                    continue
                print w                
                down(w)
    except Exception, e:
        print e
        
if __name__ == '__main__':
    main()