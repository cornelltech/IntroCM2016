1. Generate an oauth token by:
curl -i -u your_username -d '{"scopes": ["repo", "gist", "notifications", "user"], "note": "getting-started"}' https://api.github.com/authorizations
or by going to: https://github.com/settings/tokens/new (select all but the admin categories and delete_repo)
2. Check access:
curl -i -H 'Authorization: token GITHUB_TOKEN' https://api.github.com/user
3. Browse to docs: http://pygithub.readthedocs.org/en/stable/github.html and https://developer.github.com/v3/

# view user repos
curl -i -H 'Authorization: token GITHUB_TOKEN' https://api.github.com/user/repos

# view user owned repos
curl -i -H 'Authorization: token GITHUB_TOKEN' https://api.github.com/user/repos?type=owner

# repo events
curl -i -H 'Authorization: token GITHUB_TOKEN' https://api.github.com/repos/USER_NAME/REPO_NAME/events

# repo push events
curl -i -H 'Authorization: token GITHUB_TOKEN' https://api.github.com/repos/USER_NAME/REPO_NAME/events?type=PushEvent

###########################
# PYTHON  (requires PyGithub)

from github import Github
g = Github('GITHUB_TOKEN')

# get user info
u = g.get_user('USER_NAME')
# print raw user info
print u.raw_data
# print user id, name, number of public repos
print u.id, u.name, u.public_repos

# get user repos
for repo in u.get_repos():
	# print repo name
    print repo.name

# get specific repo activity
for e in u.get_repo('REPO_NAME').get_events():
	# print event time, user and type
    print e.created_at, e.actor.name, e.type

###########################
# Instagram
1. Go to https://www.instagram.com/developer create app, uncheck implicit permission
2. Browse to https://api.instagram.com/oauth/authorize/?client_id=<CLIENT_ID>&redirect_uri=http://localhost&response_type=token&scope=basic+likes+comments+follower_list+public_content
3. Check access: 
curl https://api.instagram.com/v1/users/self/?access_token=INSTAGRAM_TOKEN
Alternatively, get token from https://apigee.com/embed/console/instagram
4. Browse to docs: https://github.com/Instagram/python-instagram and https://www.instagram.com/developer/endpoints/

from instagram.client import InstagramAPI
api = InstagramAPI(access_token="INSTAGRAM_TOKEN")

# get user info
u = api.user()
# print user id, username, full name
print u.id, u.username, u.full_name
# print activity counts
print u.counts

# get followers
followers, next_ = api.user_followed_by()
while next_:
    more_followers, next_ = api.user_followed_by(with_next_url=next_)
    followers.extend(more_followers)

# get followees
followees, next_ = api.user_follows()
while next_:
    more_followees, next_ = api.user_follows(with_next_url=next_)
    followees.extend(more_followees)

# intersect followers and followees 
set([f.username for f in followers]) & set([f.username for f in followees])

# get user feed
media_feed, next_ = api.user_media_feed(count=20)
for media in media_feed:
	# print user 
    print media.user
    # print caption
    if media.caption:
        print media.caption.text
    print "++"

# get followed people media and info
crawled={}
for media in media_feed:
    if media.user.id in crawled: 
    	continue
    crawled[media.user.id] = True
    # friend's recent media
    recent_media, next_ = api.user_recent_media(user_id=media.user.id, count=10)
    # friend's info
    user_info           = api.user(user_id=media.user.id)
    # print number of media elements
    print ("Got %d items for user %s"%(len(recent_media), media.user))
    # print user full name, id, bio, number of followers
    print ("This is %s, ID %s, bio %s, followed by %s"%(user_info.full_name, 
                                                        user_info.id, 
                                                        user_info.bio, 
                                                        user_info.counts['followed_by']))
    print ("++")

# search public content posted around a geo-location (cornell tech)
crawled_media = api.media_search(lat=40.741, lng=-74.002)
print "Got %d results\n" % len(crawled_media)