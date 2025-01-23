import tweepy
import pickle
from django.shortcuts import render
from .models import Tweet
import plotly.express as px
import plotly.io as pio

# Load the trained model and vectorizer
model = pickle.load(open('analysis/model/trained_Model_logisticRegression.pkl', 'rb'))
vectorizer = pickle.load(open('analysis/model/vectorizer_logisticRegression.pkl', 'rb'))

# Twitter API credentials
BEARER_TOKEN = " "
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def index(request):
    return render(request, 'home/index.html')







def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')  
        try:
            response = client.search_recent_tweets(query=query, max_results=10)
            tweets = response.data if response else []
            
            # Variables to count positive and negative sentiments
            positive_count = 0
            negative_count = 0

            results = []
            for tweet in tweets:
                text = tweet.text
                vectorized_text = vectorizer.transform([text])
                prediction = model.predict(vectorized_text)[0]
                sentiment = "Positive" if prediction == 1 else "Negative"
                
                # Save tweet to database
                Tweet.objects.create(tweet_text=text, sentiment=sentiment)
                
                # Update sentiment counts
                if sentiment == "Positive":
                    positive_count += 1
                else:
                    negative_count += 1
                
                results.append({
                    'tweet': text,
                    'sentiment': sentiment,
                })
                
            # Create a pie chart using Plotly
            fig = px.pie(values=[positive_count, negative_count], names=["Positive", "Negative"], title="Sentiment Distribution")
            graph = pio.to_html(fig, full_html=False)    

            return render(request, 'home/index.html', {'results': results, 'graph': graph})

        except Exception as e:
            return render(request, 'home/index.html', {'error': str(e)})
