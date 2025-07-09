import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer




def analyze_sentiment(text):
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Get the set of English stop words
    stop_words = set(stopwords.words('english'))
    # Tokenize the text
    words = nltk.word_tokenize(text.lower())

    # Remove stop words
    words = [word for word in words if word not in stop_words]

    # Join the words back into a string
    filtered_text = ' '.join(words)

    # Perform sentiment analysis
    sentiment_score = sia.polarity_scores(filtered_text)

    return sentiment_score['neg'], sentiment_score['neu'], sentiment_score['pos'], sentiment_score['compound']
