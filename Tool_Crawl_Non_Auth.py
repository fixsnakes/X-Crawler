


from XNonAuth import XCrawlNonAuth

from pathlib import Path

import threading
import requests,json





listUser =  open('datauser.txt','r').read().split("\n")
proxyList = open('proxy.txt','r').read().split("\n")



def CreateFolderFile(name,profileData,TweetData,imgContent):
    
    
    try:
        fulllpath = f'Xcrawl\\Crawled User Data Non Auth\\{name}'
        directory_path = Path(fulllpath)
        
        directory_path.mkdir(parents=True,exist_ok=True)
        
        with open(fulllpath + f"\\profile.json",'w',encoding='utf-8') as file:
            json.dump(profileData,file,ensure_ascii=False,indent=4)
        
        with open(fulllpath + f"\\tweetdata.json",'w',encoding='utf-8') as file:
            json.dump(TweetData,file,ensure_ascii=False,indent=4)
        
        with open(fulllpath + "\\profileAvatar.jpg", "wb") as file:
            file.write(imgContent)
        
        return "SUCCESS"
        
    except Exception as err:
        return 'ERR' + str(err)


def Crawl(proxy = 'none'):
    
    while len(listUser) > 0:
        
        username = listUser.pop()
    
        XObj = XCrawlNonAuth(username,proxy)
        
        
        statusGetCookie = XObj.GetCookiesNonAuth()
        
        if "ERR" in statusGetCookie:
            
            print(f"username: {username} >>> Status: {statusGetCookie}")
            continue
        
        statusCrawlProfile = XObj.CrawlBasicDataProfile()
        
        if "ERR" in statusCrawlProfile:
            print(f"username: {username} >>> Status: {statusCrawlProfile}")
            continue

        statusCrawlTweets = XObj.CrawlTweetUser()
        
        if "ERR" in statusCrawlTweets:
            print(f"username: {username} >>> Status: {statusCrawlTweets}")
            continue

        
        imgUrl = statusCrawlProfile['avatar']
        
        responseImg = requests.get(imgUrl)
        
        statusCreateFolder = CreateFolderFile(username,statusCrawlProfile,statusCrawlTweets,responseImg.content)
        
        if "ERR" in statusCreateFolder:
            print(f"username: {username} >>> Status: {statusCreateFolder}")

        else:
            print(f"username: {username} >>> Status: Crawl Data Success")
    
    return 


threads = []

proxyType = 0

#SetUp Luong'

ThreadNumber = 5

for _ in range(ThreadNumber):
    
    if proxyType == 1:
    
        proxy = proxyList.pop()
        
        Task = threading.Thread(target=Crawl,args=(proxy))
        
        proxyList.append(proxy)
    else:
        Task = threading.Thread(target=Crawl)
    
    Task.start()
    
    threads.append(Task)


for t in threads:
    t.join()

print("Crawl Done")
