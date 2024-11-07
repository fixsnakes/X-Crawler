#ImBigJetPlane






from XAuth import XCrawler

import pandas as pd
import os

from pathlib import Path

import threading
import requests,json

import aiohttp
import asyncio




listUser =  open('datausercrawlAuth.txt','r').read().split("\n")
job_titles = open('JobCrawl/list_job.text', 'r').read().split("\n")

async def download_image(session, url, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
    except ValueError as e:
        iscontinue = True


async def download_all_images(media_urls, folder):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for idx, url in enumerate(media_urls):
            save_path = f"{folder}\\media_{idx}.jpg"
            tasks.append(download_image(session, url, save_path))
        await asyncio.gather(*tasks)


def CreateFolderFIle(usernameCrawl,dataCrawlProfile,dataCrawlMedia,dataCrawlTweer):
    try:
        
        fulllpath = f'Crawled User Data Auth\\{usernameCrawl}'
        
        pathmedia = f'Crawled User Data Auth\\{usernameCrawl}\\Media'
        
        
        directory_path = Path(fulllpath)
        
        directory_path.mkdir(parents=True,exist_ok=True)
        
        directory_path = Path(pathmedia)
        
        directory_path.mkdir(parents=True,exist_ok=True)
        
        
        
        with open(fulllpath + f"\\profile.json",'w',encoding='utf-8') as file:
            json.dump(dataCrawlProfile,file,ensure_ascii=False,indent=4)
        
        #Download IMG Avatar
        
        
        with open(fulllpath + f"\\tweetdata.json",'w',encoding='utf-8') as file:
            json.dump(dataCrawlTweer,file,ensure_ascii=False,indent=4)
        
        
        imgavatarUrl =  dataCrawlProfile['avatar']
        
        responseImg = requests.get(imgavatarUrl)
        
        with open(fulllpath + "\\profileAvatar.jpg", "wb") as file:
            file.write(responseImg.content)
            
        
        listMedia = dataCrawlMedia['mediaUrlList']
        
  
        
        
        asyncio.run(download_all_images(listMedia,pathmedia))
            
            
        #DownLoadImg
        
        return "SUCCESS"
        
    
    except ValueError as err:
        return "ERR--CreateFolder" + str(err)
    


def Crawl(XAuthObj):
    while len(listUser) > 0:
        
        usernameCrawl = listUser.pop()
        
        
        statusCrawlProfileData = XAuthObj.CrawlProfileData(usernameCrawl)
        
        if "ERRCrawlProfileData" in statusCrawlProfileData:
            print(statusCrawlProfileData)
            continue
        
        userID = statusCrawlProfileData['userid']
        
        
        statusCrawlMediaUser = XAuthObj.CrawlMediaUser(userID)
        
        if "ERRCrawlMediaUser" in statusCrawlMediaUser:
            print(statusCrawlMediaUser)
            continue
        
        statusCrawlTweet = XAuthObj.CrawlTweetUser(userID)
        
        if "ERRCrawlTweetUser" in statusCrawlTweet:
            print(statusCrawlTweet)
            continue
        
        statusCreate = CreateFolderFIle(usernameCrawl,statusCrawlProfileData,statusCrawlMediaUser,statusCrawlTweet)
        
        if "SUCCESS" in statusCreate:
            print(f"{usernameCrawl} => Crawl Done")
    return
        
def Save_jobs_to_excel(data_job, filename="JobCrawl/job_list.xlsx"):
    try:
    
        os.makedirs("JobCrawl", exist_ok=True)
        
        df = pd.DataFrame(data_job)

        df.rename(columns={
            "name_job": "Công việc",
            "job_description": "Mô tả",
            "link_apply": "Link đăng kí",
            "job_location": "Địa chỉ",
            "company": "Công ty"
        }, inplace=True)
        
        if os.path.exists(filename):
            existing_df = pd.read_excel(filename)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
        else:

            combined_df = df

        combined_df.to_excel(filename, index=False)
        
        print(f"File đã được lưu thành công")
    except ValueError as err:
        return "ERR--SaveJob" + str(err)        




CRAWLTYPE = input("CRAWL BY: 1.AUTH 2.COOKIE: ")

threads_number  = 5

threadslist = []



        
if CRAWLTYPE == 1:
    
    username = input("Username: ")
    password = input("Password: ")
    XAuthObj = XCrawler(username,password)
    LoginStatus = XAuthObj.LoginToGetCookie()
    
    if "ERR" in LoginStatus:
        print(LoginStatus)
    else:
        for _ in range(threads_number):
            Task = threading.Thread(target=Crawl, args=(XAuthObj,))
            
            Task.start()
            
            threadslist.append(Task)

        
        for thread in threadslist:
            thread.join()

        print("Crawl Done")
else:
    
    cookie = input("Cookie (optional): ").strip()
    XAuthObj = XCrawler("username","password",cookie)
    for _ in range(threads_number):
        Task = threading.Thread(target=Crawl, args=(XAuthObj,))
        
        Task.start()
        
        threadslist.append(Task)

    for thread in threadslist:
        thread.join()

    print("Crawl Done")

    for job in job_titles:
        data_job = XAuthObj.SearchJob(job, "VietNam")
        Save_jobs_to_excel(data_job)

    






