from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash

app=Flask(__name__)

#raw url
@app.route('/')  
  return render_template('index.html')

#Going to home page, displaying details for the User
@app.route('/home', methods=['POST'])  
def home():
  import tweepy
  username=request.form['one_user']

  auth = tweepy.OAuthHandler("aU39ahEGFuTOWxYKsJ9gDw", "kfxj6ngmHcbwaWKeGfBdCGrbFZJAsUYd21EOl5mQ")
  api=tweepy.API(auth)

  #Taking user attributes in 'user' class.
  user = tweepy.api.get_user(username)


  #Calculating grade_1 based on the count on followers
  #UpperBound := 500
  grade_1 = user.followers_count / 500.0000 * 45.0000
  

  #Calculating grade_2 based on the power of followers
  #UpperBound := 500(power)
  power=0
  i=0
  c = tweepy.Cursor(api.followers,username)
  user_followers = c.items()

  for follower in user_followers:
     power += follower.followers_count

  power = power / user.followers_count
  if power < 500:
      grade_2 = power / 500.0000 * 20.0000
  else:
      grade_2 = 20.0000
      

  #Calculating grade_3 based on retweets of user's tweets
  #UpperBound := 100
  retweet_cnt=0
  c = tweepy.Cursor(api.user_timeline,username)
  user_tweets = c.items()
  tweepy.api.user_timeline(screen_name=username)
  disp_tweet = []
  ii=0
  
  for tweet in user_tweets:
     retweet_cnt+=tweet.retweet_count
     if ii < 10:
        disp_tweet.append(tweet.text)
     ii=ii+1
  
  if retweet_cnt < 100:
     grade_3 = retweet_cnt / 100.00 * 25
  else:
     grade_3 = 25
	


  #Calculating grade_5 based on how many user is following
  #UpperBound := 300
  if user.friends_count < 300:
     grade_5 =  user.friends_count / 300.000 * 6
  else:
     grade_5 = 6

	

  #Calculating grade_6 based on how much the user tweets
  #UpperBound := 3000
  if user.statuses_count < 3000:
     grade_6 =  user.statuses_count / 3000.000 * 4
  else:
     grade_6 = 4

	
  #Calculating final grade.
  grade = grade_1 + grade_2 + grade_3 + grade_5 + grade_6

  tmp = user.followers_count
  
  #Creating a list off all grades
  data =[user.name,user.profile_image_url,tmp,user.friends_count,user.statuses_count,grade]

return render_template('home.html',data = data,disp_tweet=disp_tweet)

if __name__ == '__main__':
	app.run(debug=True)
