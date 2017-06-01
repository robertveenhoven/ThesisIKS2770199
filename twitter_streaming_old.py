#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "XXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXX"
consumer_key = 	"XXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXX"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by keywords: 
    stream.filter(track=['Apple','Iphone','Ipad','Ipod','Iphone7','Iphone6', 'Microsoft','Windows','Skype','skype','Windows7','Windows8','Windows10','Xbox','xbox', 'Netflix', 'Amazon'], languages=["en"])
