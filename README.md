# Crawl data on web/social: Twitter/X

## Description: Crawl Profile data, Number of Followers, Media, Tweets of a User Using Python


### Main Functions of XAuth Module
- **CrawlProfileData**: Crawl basic information of a User including: Name, Avatar, Follower, Following.

- **CrawlMediaUser**: Crawl photos, videos of a User.

- **CrawlTweetUser**: Crawl tweets of a User.

- **GetCommentOfTweet**: Crawl comments of a Tweet. Input will be the id of that post.
- **TopicSearchLatest**: Crawl comments related to the topic that a User wants to search.

- **SearchJob**: Search for jobs with the input Job name, Location

### Tools for Crawl and Data Analysis:

- **Tool_Crawl_Auth**: Use cookies to crawl. Run multi-threaded, helping crawl speed quickly. Use asynchronous (aiohttp) to download multiple images at the same time.

- **SentimentAnalysisComment**: With the input being the post id that you want to Crawl the comments. This tool helps analyze comments to see if this comment is positive, negative or neutral. From there, users will evaluate whether this Tweet is negative or positive.

- **SentimentAnalysisTopic**: Similar to SentimentAnalysisComment, this tool helps analyze how users express their feelings about this topic.
