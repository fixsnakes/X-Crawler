

#JNP 2024
#This Module Help Us Crawl ProfilePic,Media Of A User


#------------------------------------------ENJOY-------------------------------------------#



#auth_token=d357db4223d497f2ac8677bd8cafde3f99620d4c;guest_id=v1%3A171509247305175565;twid=u%3D1391335171362746369;_twitter_sess=BAh7CCIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADofbGFzdF9wYXNzd29yZF9jb25maXJtYXRpb24i%250AFTE3MjA4NjA3MzI5MjYwMDA6HnBhc3N3b3JkX2NvbmZpcm1hdGlvbl91aWQi%250AGDEzOTEzMzUxNzEzNjI3NDYzNjk%253D--8027d5d670ab075116de1e5fee1998d7f912395b;lang=en;lang=en;ct0=53f5c6d209ec69cc198b0b587d23d005d4b413e7214ec1fc56d8a1a66723aeae73324bc19b701596ff066b2d2a6878e4ee464c397dbd7b0257ae7c5bad83e3ab8f1389f0e5a5e23838d103b82f37e43f;guest_id_ads=v1%3A171509247305175565;guest_id_marketing=v1%3A171509247305175565;personalization_id="v1_f6MaHzRgZt2jGfuGEQaIkg=="



import requests,time
import re
from pathlib import Path

from fake_useragent import UserAgent

import string
import random,uuid

BASE_URL = "https://x.com/?mx=2"
ONBOARDING_TASK = "https://api.x.com/1.1/onboarding/task.json"
CT0_FINAL = "https://api.x.com/graphql/-876iyxD1O_0X0BqeykjZA/Viewer?variables=%7B%22withCommunitiesMemberships%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22isDelegate%22%3Afalse%2C%22withAuxiliaryUserLabels%22%3Afalse%7D"
LOGIN_1 = "https://api.x.com/1.1/onboarding/task.json?flow_name=login"
MEDIAREQ = "https://x.com/i/api/graphql/HaouMjBviBKKTYZGV_9qtg/UserMedia"
BASIC_DATA_PROFILE = "https://x.com/i/api/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName"


def RandomString():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(20))




class XCrawler:
    def __init__(self,user,password,cookie = '',proxy = '') -> None:
        self.user = user
        self.password = password
        self.proxy = proxy
        self.cookie = cookie
        self.req = requests.Session()
        self.ua = UserAgent().chrome
        self.csrftoken = 'none'
        self.uuid = str(uuid.uuid4())
        
        if self.cookie != '':
            self.csrftoken = re.findall(r'ct0=(.*?);',self.cookie)[0]


    
    def LoginToGetCookie(self):
        
        
        try:
            
            if self.proxy != '':
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
                
            #Get Gt Cookie
            header = {
                "User-Agent" : self.ua
            }
            
            
            cookieSet = self.req.get(BASE_URL, headers=header,timeout=30)
            
            #GT VARIABLE Example : 1844311148763689453
            
            gt = re.findall(r'gt=(.*?);',cookieSet.text)[0]
            
            
            cookiefull = f"gt={gt}; "
            
            for key in cookieSet.cookies.get_dict().keys():
                cookiefull += f"{key} = {cookieSet.cookies.get_dict()[key]}; "
            
            
            #gt=1844311776898449568; guest_id_marketing = v1%3A172855316789827854; guest_id_ads = v1%3A172855316789827854; personalization_id = "v1_UtANgJJIRUxxIv1fdOEZxw=="; guest_id = v1%3A172855316789827854;
            
            
        
            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': cookiefull,
                'origin': 'https://x.com',
                'priority': 'u=1, i',
                'referer': 'https://x.com/',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': self.ua,
                'x-guest-token':gt ,
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'vi',
            }

            json_data = {
                'input_flow_data': {
                    'flow_context': {
                        'debug_overrides': {},
                        'start_location': {
                            'location': 'splash_screen',
                        },
                    },
                },
                'subtask_versions': {
                    'action_list': 2,
                    'alert_dialog': 1,
                    'app_download_cta': 1,
                    'check_logged_in_account': 1,
                    'choice_selection': 3,
                    'contacts_live_sync_permission_prompt': 0,
                    'cta': 7,
                    'email_verification': 2,
                    'end_flow': 1,
                    'enter_date': 1,
                    'enter_email': 2,
                    'enter_password': 5,
                    'enter_phone': 2,
                    'enter_recaptcha': 1,
                    'enter_text': 5,
                    'enter_username': 2,
                    'generic_urt': 3,
                    'in_app_notification': 1,
                    'interest_picker': 3,
                    'js_instrumentation': 1,
                    'menu_dialog': 1,
                    'notifications_permission_prompt': 2,
                    'open_account': 2,
                    'open_home_timeline': 1,
                    'open_link': 1,
                    'phone_verification': 4,
                    'privacy_options': 1,
                    'security_key': 3,
                    'select_avatar': 4,
                    'select_banner': 2,
                    'settings_list': 7,
                    'show_code': 1,
                    'sign_up': 2,
                    'sign_up_review': 4,
                    'tweet_selection_urt': 1,
                    'update_users': 1,
                    'upload_media': 1,
                    'user_recommendations_list': 4,
                    'user_recommendations_urt': 1,
                    'wait_spinner': 3,
                    'web_modal': 1,
                },
            }

            response = self.req.post(
                LOGIN_1,

                headers=headers,
                json=json_data,
            )

            
            #Get att Atribute
            
            
            
            att = re.findall(r'att=(.*?);', str(response.headers))[0]
            cookiefull += f'att={att};'

            
            flow_token = response.json()['flow_token']
            

        

            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': cookiefull,
                'origin': 'https://x.com',
                'priority': 'u=1, i',
                'referer': 'https://x.com/',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': self.ua,
                'x-guest-token': gt,
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'vi',
            }

            json_data = {
                'flow_token': flow_token,
                'subtask_inputs': [
                    {
                        'subtask_id': 'LoginJsInstrumentationSubtask',
                        'js_instrumentation': {
                            'response': str({"rf":{"":RandomString(),RandomString():50,RandomString():18,RandomString():106},"s":RandomString()}),
                            'link': 'next_link',
                        },
                    },
                ],
            }

            #POST USER
            response = self.req.post(ONBOARDING_TASK,  headers=headers, json=json_data)
            
            flow_token = response.json()['flow_token']
        

            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': cookiefull,
                'origin': 'https://x.com',
                'priority': 'u=1, i',
                'referer': 'https://x.com/',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': self.ua,
                'x-guest-token': gt,
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'vi',
            }

            json_data = {
                'flow_token': flow_token,
                'subtask_inputs': [
                    {
                        'subtask_id': 'LoginEnterUserIdentifierSSO',
                        'settings_list': {
                            'setting_responses': [
                                {
                                    'key': 'user_identifier',
                                    'response_data': {
                                        'text_data': {
                                            'result': self.user,
                                        },
                                    },
                                },
                            ],
                            'link': 'next_link',
                        },
                    },
                ],
            }

            response = self.req.post('https://api.x.com/1.1/onboarding/task.json',  headers=headers, json=json_data)
            
            
            
            if "Hành vi đăng nhập đáng ngờ đã bị chặn" in response.text:
                return "ERRLOGIN--BLOCK IP LOGIN "
            
            flow_token = response.json()['flow_token']
            
           
                
            

            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': cookiefull,
                'origin': 'https://x.com',
                'priority': 'u=1, i',
                'referer': 'https://x.com/',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': self.ua,
                'x-guest-token': gt,
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'vi',
            }

            json_data = {
                'flow_token': flow_token,
                'subtask_inputs': [
                    {
                        'subtask_id': 'LoginEnterPassword',
                        'enter_password': {
                            'password': self.password,
                            'link': 'next_link',
                        },
                    },
                ],
            }

            response = self.req.post('https://api.x.com/1.1/onboarding/task.json',  headers=headers, json=json_data)
            

            if "screen_name" in response.text:
                kdt = re.findall(r'kdt=(.*?);',str(response.headers))[0]
                cookiefull += f'kdt={kdt}; '
                auth_token = re.findall(r'auth_token=(.*?);',str(response.headers))[0]
                cookiefull += f'auth_token={auth_token}; '
                twid = re.findall(r'twid="(.*?)"',str(response.headers))[0]
                cookiefull += f'twid={twid}; '
                
                
                #GET FULL ACCESS CT0
                
                cookieFullTemp = cookiefull
                
                ct0 =  re.findall(r'ct0=(.*?);',str(response.headers))[0]
                
                
                cookieFullTemp += f'ct0={ct0}; '
                
                
                header_full = {
                    
                    "Cookie": cookieFullTemp,
                
                
                    "X-Guest-Token": gt,

                    "User-Agent": self.ua,
                    "X-Twitter-Client-Language": "vi"
                }
            
                reponse_token = self.req.get(CT0_FINAL,headers=header_full,timeout=30)
            
                ct0 = re.findall(r'ct0=(.*?);',str(reponse_token.headers))[0]
                cookiefull += f'ct0={ct0}; '
                #gt=1844333277978747243; guest_id_marketing = v1%3A172855829416144622; guest_id_ads = v1%3A172855829416144622; personalization_id = "v1_kWciCuudCl3A3KF6adZVbg=="; guest_id = v1%3A172855829416144622; att=1-NnTreso3scyolfX2hY1VMN15Sy4DBl8nAqcePVGE;kdt=8iTO5VV1fBpVPSInhy1OLuakm4fig5wmgpZu9iit; auth_token=1b4bd07913702ecc9469b81fe2b23a181d986c91; twid=u=1391335171362746369; ct0=761fd1523edcc5caf07657ebd005c1817416d63f2eab0e2763f93e325356a19e27586e57cc22c6b188474f7e39e6819722c1b96132f39470d9f64560990a983f5b18d597f0310988deeee8714c213e42;
                
                self.cookie = cookiefull
                
                self.csrftoken = ct0
                
                return "SUCCESS"

            else:
                return 'ERRLOGIN--Unknow'
        except Exception as err:
            return 'ERRLOGIN--' + str(err)
    
    
    def CrawlProfileData(self,profile = 'none'):
        
        
        if profile == 'none':
            profile = self.user
            
            
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
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }

        
            params = f"variables=%7B%22screen_name%22%3A%22{profile}%22%7D&features=%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"
            

            response = self.req.get(BASIC_DATA_PROFILE + "?" + params,headers=headers)
            
            data = response.json()['data']
            
            
            return {
                "userid" : data['user']['result']['rest_id'],
                "username" : data['user']['result']['legacy']['screen_name'],
                "followers" : data['user']['result']['legacy']['followers_count'],
                "following" : data['user']['result']['legacy']['friends_count'],
                "posts" : data['user']['result']['legacy']['statuses_count'],
                "avatar" : data['user']['result']['legacy']['profile_image_url_https'].replace("_normal","")
            }

        except Exception as err:
            return "ERRCrawlProfileData--" + str(err)
        
    
    
    
    def CrawlMediaUser(self,userid):

            
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
                    'x-csrf-token': self.csrftoken,
                    'x-twitter-active-user': 'yes',
                    'x-twitter-auth-type': 'OAuth2Session',
                    'x-twitter-client-language': 'en',
                }
                    
                itemsMedia = []
                itemsPostId = []
                params = f"variables=%7B%22userId%22%3A%22{userid}%22%2C%22count%22%3A{100}%2C%22includePromotedContent%22%3Afalse%2C%22withClientEventToken%22%3Afalse%2C%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D"

                response = self.req.get(MEDIAREQ + "?" + params,headers=headers)
                data = response.json()
                items = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][2]['entries'][0]['content']['items']
                
                bottomCursor = ""
                for mediaElement in items:
                    try:
                        mediaPostID = mediaElement['item']['itemContent']['tweet_results']['result']['rest_id']
                        
                        
                        # if "video_info" in mediaElement['item']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]:
                        #     mediaUrl = mediaElement['item']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['video_info']['variants'][-1]['url']
                        # else:
                        
                        mediaUrl = mediaElement['item']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['media_url_https']
                        
                        itemsMedia.append(mediaUrl)
                        itemsPostId.append(mediaPostID)
                        
                        
                        bottomCursor = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][2]['entries'][-1]['content']['value']
                    except:
                        isContinue = True
                        
                
                return {
                    "TotalItemsValid" : len(itemsMedia),
                    "mediaUrlList" : itemsMedia,
                    "mediaPostIdList" : itemsPostId
                }
                    
            
            except Exception as err:
                return "ERRCrawlMediaUser--" + str(err)
    def CrawlTweetUser(self,userid):
        try:

            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
          
                'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
        
                'x-client-uuid': self.uuid,
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }
            
            params = f"variables=%7B%22userId%22%3A%22{userid}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D"

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
            
        except ValueError as err:
            return "ERRCrawlTweetUser--" +  str(err)

    
    
    
    def CreateTweet(self,content):
        
        
        try:

            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'origin': 'https://x.com',
                'priority': 'u=1, i',
                'referer': 'https://x.com/home',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }
            
            json_data = {
                'variables': {
                    'tweet_text': content,
                    'dark_request': False,
                    'media': {
                        'media_entities': [],
                        'possibly_sensitive': False,
                    },
                    'semantic_annotation_ids': [],
                    'disallowed_reply_options': None,
                },
                'features': {
                    'communities_web_enable_tweet_community_results_fetch': True,
                    'c9s_tweet_anatomy_moderator_badge_enabled': True,
                    'responsive_web_edit_tweet_api_enabled': True,
                    'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                    'view_counts_everywhere_api_enabled': True,
                    'longform_notetweets_consumption_enabled': True,
                    'responsive_web_twitter_article_tweet_consumption_enabled': True,
                    'tweet_awards_web_tipping_enabled': False,
                    'creator_subscriptions_quote_tweet_preview_enabled': False,
                    'longform_notetweets_rich_text_read_enabled': True,
                    'longform_notetweets_inline_media_enabled': True,
                    'articles_preview_enabled': True,
                    'rweb_video_timestamps_enabled': True,
                    'rweb_tipjar_consumption_enabled': True,
                    'responsive_web_graphql_exclude_directive_enabled': True,
                    'verified_phone_label_enabled': False,
                    'freedom_of_speech_not_reach_fetch_enabled': True,
                    'standardized_nudges_misinfo': True,
                    'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                    'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                    'responsive_web_graphql_timeline_navigation_enabled': True,
                    'responsive_web_enhance_cards_enabled': False,
                },
                'queryId': 'znq7jUAqRjmPj7IszLem5Q',
            }

            response = self.req.post('https://x.com/i/api/graphql/znq7jUAqRjmPj7IszLem5Q/CreateTweet',headers=headers,json=json_data)
            
            
            if response.status_code == 200:
                return "SUCCESS"

            else:
                return "ERRCreateTweet--" + response.text
        except Exception as err:
            return "ERRCreateTweet--" + str(err)
    

    def SearchTweets(self, content):
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
                'referer': 'https://x.com/search?q=m%C3%B9a%20xu%C3%A2n&src=typed_query',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-client-uuid': self.uuid,
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }
            count = 20
            params = {
                'variables': f'{{"rawQuery":"{content}","count":{count},"querySource":"typed_query","product":"Top"}}',
                'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}'
            }
    
            response = self.req.get(
                'https://x.com/i/api/graphql/MJpyQGqgklrVl_0X9gNy3A/SearchTimeline',
                params=params,
                headers=headers,
            )
            list_Data = response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']
            tweet_Data = []
    
            for i in range(len(list_Data)):
                if 'content' in list_Data[i] and 'itemContent' in list_Data[i]['content']:
                    tweet_info = {
                        "rest_id": list_Data[i]['content']['itemContent']['tweet_results']['result']['rest_id'],
                        "user": {
                            "name": list_Data[i]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['name'],
                            "username": list_Data[i]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name'],
                            "followers_count": list_Data[i]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['followers_count'],
                            "statuses_count": list_Data[i]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['statuses_count'],
                            "profile_image": list_Data[i]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['profile_image_url_https']
                        },
                        "content": list_Data[i]['content']['itemContent']['tweet_results']['result']['legacy']['full_text'],
                        "created_at": list_Data[i]['content']['itemContent']['tweet_results']['result']['legacy']['created_at'],
                        "favorites_count": list_Data[i]['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count'],
                        "reply_count": list_Data[i]['content']['itemContent']['tweet_results']['result']['legacy']['reply_count'],
                        "retweet_count": list_Data[i]['content']['itemContent']['tweet_results']['result']['legacy']['retweet_count'],
                        "hashtags": [hashtag['text'] for hashtag in list_Data[i]['content']['itemContent']['tweet_results']['result']['legacy']['entities']['hashtags']],
                        "link_tweet": "https://x.com/" + list_Data[i]['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name'] + "/status/" + list_Data[i]['content']['itemContent']['tweet_results']['result']['rest_id']
                    }
                    tweet_Data.append(tweet_info)
            return tweet_Data
        except Exception as err:
            return "ERRSearchTweets--" + str(err)        
    def TrendForYou(self):
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
                'referer': 'https://x.com/home',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-client-uuid': self.uuid,
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }
            params = {
                'variables': '{}',
                'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}'
            }
    
            response = self.req.get(
                'https://x.com/i/api/graphql/SQF2aB791cUu02BkZk1HcA/ExploreSidebar',
                params=params,
                headers=headers,
            )
            list_content = []
            list_data = response.json()['data']['explore_sidebar']['timeline']['instructions'][1]['entries'][1]['content']['items']
            
            for x in list_data:
                list_content.append(x['item']['itemContent']['name'])
            
            return list_content
    
        except Exception as err:
            return "ERRTrendForYou--" + str(err) 
        
    def GetCommentOfTweet(self,IdPost):

        
        controllerData = 'DAACDAABDAABCgABAIAAwkICAAEKAAKAAAAAAAEgAAoACbSKfyE8lv9kCAALAAAAAA8ADAMAAAAaAQACQsIAgAAAIAEAAAAAgAAAAAAAAAAAgBAKAA7o/gpl5OhO7QoAEIbfbFS2gEofAAAAAA=='
        
        try:
        

            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }

            params = f'variables=%7B%22focalTweetId%22%3A%22{IdPost}%22%2C%22with_rux_injections%22%3Afalse%2C%22rankingMode%22%3A%22Relevance%22%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Atrue%2C%22withVoice%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticleRichContentState%22%3Atrue%2C%22withArticlePlainText%22%3Afalse%2C%22withGrokAnalyze%22%3Afalse%2C%22withDisallowedReplyControls%22%3Afalse%7D'

            response = self.req.get('https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail?' + params,headers=headers)
            
            
            data = response.json()
            bottomCursor = data['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][-1]
            
            
            commentList = data['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][1:]
            

            dataComment = []


            for comment in commentList:
                
                try:
                    userComment = comment['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['name']
                    contentCommment = " ".join(comment['content']['items'][0]['item']['itemContent']['tweet_results']['result']['legacy']['full_text'].split("\n"))
                    like_count = comment['content']['items'][0]['item']['itemContent']['tweet_results']['result']['legacy']['favorite_count']
                    
                    dataComment.append({
                        'user' : userComment,
                        'content' : contentCommment,
                        'like' : like_count,
                    })
                    
                except:
                    isContinue = True
                    
            for _ in range(100):
                try:
                    bottomCursor = data['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][-1]['content']['itemContent']['value']
                    params = {
                        'variables': f'{{"focalTweetId":"{IdPost}","cursor":"{bottomCursor}","referrer":"tweet","controller_data":"{controllerData}","with_rux_injections":false,"rankingMode":"Relevance","includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":true,"withVoice":true}}',
                        'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                        'fieldToggles': '{"withArticleRichContentState":true,"withArticlePlainText":false,"withGrokAnalyze":false,"withDisallowedReplyControls":false}',
                    }

                    response = self.req.get(
                        'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail',
                        params=params,
                        headers=headers,
                    )
                    
                    data = response.json()
                    
                    commentList = data['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][1:]
                    
                    for comment in commentList:
                
                        try:
                            userComment = comment['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['name']
                            contentCommment = " ".join(comment['content']['items'][0]['item']['itemContent']['tweet_results']['result']['legacy']['full_text'].split("\n"))
                            like_count = comment['content']['items'][0]['item']['itemContent']['tweet_results']['result']['legacy']['favorite_count']
                            
                            dataComment.append({
                                'user' : userComment,
                                'content' : contentCommment,
                                'like' : like_count,
                            })
                            
                            
                            
                        except:
                            isContinue = True
                except:
                    break

            return dataComment
        except Exception as err:
            return "GetCommentOfTweet--" + str(err) 



    def TopicSearchLatest(self,content):
       
        try:
            
            
            dataComment = []
            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                'x-client-uuid': self.uuid,
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }

            params = {
                'variables': f'{{"rawQuery":"{content}","count":100,"querySource":"typed_query","product":"Latest"}}',
                'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
            }

            response = self.req.get('https://x.com/i/api/graphql/MJpyQGqgklrVl_0X9gNy3A/SearchTimeline',params=params,headers=headers)
            
        
            data = response.json()
   
            
            
            commentList = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']


            for comment in commentList:
                
                try:
                    userComment = comment['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['name']
                    contentCommment = " ".join(comment['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].split("\n"))
                    like_count = comment['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count']
                    
                    dataComment.append({
                        'user' : userComment,
                        'content' : contentCommment,
                        'like' : like_count,
                    })
                    
                            
                            
                except:
                    isContinue = True
            
       
            bottomCursor = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries'][-1]['content']['value']
            for _ in range(30):
                
                try:
                    
                    
                    
                    params = {
                        'variables': f'{{"rawQuery":"{content}","count":100,"cursor":"{bottomCursor}","querySource":"typed_query","product":"Latest"}}',
                        'features': '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                    }

                    response = self.req.get(
                        'https://x.com/i/api/graphql/MJpyQGqgklrVl_0X9gNy3A/SearchTimeline',
                        params=params,
                        headers=headers,
                    )
                    
                    data = response.json()
             
                    
                    commentList = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']

                    
                    for comment in commentList:
                        
                        try:
                            userComment = comment['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['name']
                            contentCommment = " ".join(comment['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].split("\n"))
                            like_count = comment['content']['itemContent']['tweet_results']['result']['legacy']['favorite_count']
                            
                            dataComment.append({
                                'user' : userComment,
                                'content' : contentCommment,
                                'like' : like_count,
                            })
                            
                            
                        except:
                            
                            isContinue = True
                    bottomCursor = data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][-1]['entry']['content']['value']
                    
                            
                except Exception as e:
                    isContinue = True

            return dataComment

            
        except ValueError as err:
            return "ERRTopicSearchLatest--" + str(err) 


    #Crawl Job
    def SearchJob(self,job,location): 
        
        try:
            
            headers = {
                'accept': '*/*',
                'accept-language': 'vi-VN,vi;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': self.cookie,
                'priority': 'u=1, i',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-client-uuid': self.uuid,
                'x-csrf-token': self.csrftoken,
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
            }
    
            params = {
                'variables': f'{{"count":100,"cursor":null,"searchParams":{{"keyword":"{job}","job_location_id":null,"job_location":"{location}","job_location_type":[],"seniority_level":[],"company_name":null,"employment_type":[],"industry":null}}}}',
            }
    
            response = self.req.get(
                'https://x.com/i/api/graphql/JyATh-zc07YHeyDDl3rDgg/JobSearchQueryScreenJobsQuery',
                params=params,
                headers=headers,
            ) 
            
            data_job=[] 
            
            list_job=response.json()['data']['job_search']['items_results']
            
            for data in list_job:
                
                rest_id = data['rest_id']

                headers = {
                    
                    'sec-ch-ua-platform': '"Windows"',
                    'cookie': self.cookie,
                    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                    'x-csrf-token': self.csrftoken,
                    'Referer': 'https://x.com/jobs/1833642168541712385?q=it&lid=1721618121382125959&lval=Vietnam',
                    'X-Client-UUID': self.uuid,
                    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                    'x-twitter-client-language': 'en',
                    'sec-ch-ua-mobile': '?0',
                    'x-twitter-active-user': 'yes',
                    'x-twitter-auth-type': 'OAuth2Session',
                    'User-Agent':  self.ua,
                    'content-type': 'application/json',
                    
                }
    
                params = {
                    'variables': f'{{"jobId":"{rest_id}","loggedIn":true}}',
                }
    
                response = self.req.get('https://x.com/i/api/graphql/lkS1Zj_iyLY_hmJCQIqqJg/JobScreenQuery', params=params, headers=headers)
    
                job_description=response.json()['data']['jobData']['result']['core']['job_description']
                job_description_data = json.loads(job_description)
                
                text_content = [block["text"] for block in job_description_data["blocks"]]
                name_job=response.json()['data']['jobData']['result']['core']['title']
                link_apply=response.json()['data']['jobData']['result']['core']['external_url']
                job_location=response.json()['data']['jobData']['result']['core']['location']
                company=response.json()['data']['jobData']['result']['company_profile_results']['result']['core']['name']
    
                important_info = {
                    
                    "name_job": name_job,
                    "job_description":text_content,
                    "link_apply": link_apply,
                    "job_location": job_location,
                    "company": company,
                    
                }
                data_job.append(important_info)
                time.sleep(5)
                
            return data_job
            
        except ValueError as err:
            
            return "ERRSearchJob--" + str(err) 
