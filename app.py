from flask import Flask, request, jsonify, render_template
import openai
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv('sk-6UjBwc2m3kdzuIIzuBZtXP3LV0jcSqPOkJHV9W3gxzezTXzY')  # Use environment variable for security

def fetch_reviews(url):
    # This function should scrape or fetch reviews from the provided URL.
    # For demonstration, we will return a static list of reviews.
    # In a real application, you would implement web scraping or API calls to get actual reviews.
    return [
        "Great product! Highly recommend it.",
        "Not worth the price. Very disappointed.",
        "Average quality, could be better.",
        "Excellent service and fast delivery.",
        "The product broke after a week of use."
    ]

def analyze_sentiment(feedback):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Analyze the sentiment of the following feedback: {feedback}"}
        ]
    )
    return response['choices'][0]['message']['content']

def extract_insights(feedback):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Extract key insights from the following feedback: {feedback}"}
        ]
    )
    return response['choices'][0]['message']['content']

def generate_response_suggestion(feedback):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Suggest a response to the following feedback: {feedback}"}
        ]
    )
    return response['choices'][0]['message']['content']

def analyze_reviews(reviews):
    sentiments = []
    for review in reviews:
        sentiment = analyze_sentiment(review)
        sentiments.append(sentiment)
    
    # Count sentiments
    positive = sentiments.count("positive")
    negative = sentiments.count("negative")
    neutral = sentiments.count("neutral")
    
    return {
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'key_highlights': extract_insights(reviews),  # Top insights
        'key_feedback': extract_insights(reviews)      # Top feedback points
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    company_url = request.json['company_url']
    product_url = request.json['product_url']
    
    # Fetch reviews from the URLs
    reviews = fetch_reviews(company_url)  # Replace with actual fetching logic
    analysis = analyze_reviews(reviews)
    
    return jsonify({
        'sentiment_counts': {
            'positive': analysis['positive'],
            'negative': analysis['negative'],
            'neutral': analysis['neutral']
        },
        'key_highlights': analysis['key_highlights'],
        'key_feedback': analysis['key_feedback']
    })

if __name__ == '__main__':
    app.run(debug=True)