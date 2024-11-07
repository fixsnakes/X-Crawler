
import requests,time
import re
from pathlib import Path

from fake_useragent import UserAgent





BASE_URL = "https://x.com/?mx=2"
ONBOARDING_TASK = "https://api.x.com/1.1/onboarding/task.json"
CT0_FINAL = "https://api.x.com/graphql/-876iyxD1O_0X0BqeykjZA/Viewer?variables=%7B%22withCommunitiesMemberships%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22isDelegate%22%3Afalse%2C%22withAuxiliaryUserLabels%22%3Afalse%7D"
LOGIN_1 = "https://api.x.com/1.1/onboarding/task.json?flow_name=login"
MEDIAREQ = "https://x.com/i/api/graphql/HaouMjBviBKKTYZGV_9qtg/UserMedia"
BASIC_DATA_PROFILE = "https://x.com/i/api/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName"
USERTW_URL = "https://api.x.com/graphql/Tg82Ez_kxVaJf7OPbUdbCg/UserTweets?"




class XCrawlNonAuth:
    def __init__(self,username,proxy = 'none') -> None:
        self.username = username
        self.req = requests.Session()
        self.userID = ""
        self.cookie = ""
        self.csrftoken = ""
        self.ua = UserAgent().chrome
        self.proxy = proxy

    
    def GetCookiesNonAuth(self):
        
        if self.proxy != 'none':

            if len(self.proxy.split(":")) == 2:
                
                proxyies = self.proxy
            
                
            else:
                #IP:PORT:USER:PASS
                #https://user:password@proxyip:port
                proxyies = self.proxy.split(":")[2] + ":" + self.proxy.split(":")[3] + "@" + self.proxy.split(":")[0] + ":" +self.proxy.split(":")[1]
                

            data =  {
                'http': f'http://{proxyies}',
                'https': f'http://{proxyies}',
                'socks4': f'socks4://{proxyies}',
                'socks5': f'socks5://{proxyies}'
            }

            self.req.proxies.update(data)
            
        
        try:
            header = {
                "User-Agent" : self.ua
            }
            
            
            cookieSet = self.req.get(BASE_URL, headers=header,timeout=30)
            
            #GT VARIABLE Example : 1844311148763689453
            
            gt = re.findall(r'gt=(.*?);',cookieSet.text)[0]

            cookiefull = f"gt={gt}; "
            
            for key in cookieSet.cookies.get_dict().keys():
                cookiefull += f"{key} = {cookieSet.cookies.get_dict()[key]}; "
            
            
            self.csrftoken = gt
            
            self.cookie = cookiefull
            return "SUCCESS"

        except Exception as err:
            return "ERRGetCookiesNonAuth" +  str(err)
    
    
    def CrawlBasicDataProfile(self):
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-guest-token': self.csrftoken,
                'x-twitter-client-language': 'en',
            }

        
            params = f"variables=%7B%22screen_name%22%3A%22{self.username}%22%7D&features=%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"
            

            response = self.req.get(BASIC_DATA_PROFILE + "?" + params,headers=headers)
            
            
            data = response.json()['data']
            
            self.userID =  data['user']['result']['rest_id']
            
 
            return {
                "username" : data['user']['result']['legacy']['screen_name'],
                "followers" : data['user']['result']['legacy']['followers_count'],
                "following" : data['user']['result']['legacy']['friends_count'],
                "posts" : data['user']['result']['legacy']['statuses_count'],
                "avatar" : data['user']['result']['legacy']['profile_image_url_https'].replace("_normal","")
            }

        except Exception as err:
            return "ERRCrawlBasicDataProfile--" +  str(err)

    
    
    def CrawlTweetUser(self):
        
        
        try:

            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'origin': 'https://x.com',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': self.ua,
                'x-guest-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'vi',
            }
            params = f"variables=%7B%22userId%22%3A%22{self.userID}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D"

            response = self.req.get('https://api.x.com/graphql/Tg82Ez_kxVaJf7OPbUdbCg/UserTweets?' + params,headers=headers)
            
            data = response.json()
            
            
            if 'TimelinePinEntry' in  str(data['data']['user']['result']['timeline_v2']['timeline']['instructions']):
            
                listData = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][2]['entries']
            else:
                listData = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries']

            listItems = []

            for items in listData:
                
                
                try:
                
                    media = items['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media']

                    
                    listUrlMedia = []
                    for itemMedia in media:
                        listUrlMedia.append(itemMedia['media_url_https'])
                    
                    item = {
                        "idPost" : items['content']['itemContent']['tweet_results']['result']['rest_id'],
                        "urlPost" : media[0]['display_url'],
                        "content" :  items['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace("\n",""),
                        "like_count" : items['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count'],
                        "comment_count" : items['content']['itemContent']['tweet_results']['result']['legacy']['reply_count'],
                        "mediaUrl" : listUrlMedia
                        
                    }
                    
                    listItems.append(item)
                except:
                    iscontinue = True
            
            
            return listItems
            
        except Exception as err:
            return "ERRCrawlTweetUser--" +  str(err)
    
                       
    

        
        
    
    
