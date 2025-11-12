import pandas as pd
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import date, timedelta

def analyze_company_sentiment(query, days_ago = 3):
    """
    Fetches and analyzes the sentiment of news articles for a given company query.
    
    Args:
        query (str): The company name or search term to query news articles for.
        days_ago (int): Number of days in the past to fetch articles from (default: 3).
    
    Returns:
        pd.DataFrame: DataFrame containing article dates, titles, and compound sentiment scores,
                     sorted by date (most recent first). Returns None if no articles are found
                     or if an API error occurs.
    """

    # Calculate the start date for article retrieval (days_ago days before today)
    start_date = (date.today() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

    print(f"===== Fetching articles for '{query}' from '{start_date}' =====")

    # List of trusted financial news domains to filter article sources
    financial_domains = (
        'bloomberg.com,reuters.com,ft.com,wsj.com,businessinsider.com,'
        'cnbc.com,marketwatch.com,finance.yahoo.com,forbes.com,seekingalpha.com'
    )

    # Fetch articles from NewsAPI, sorted by popularity to prioritize high-impact news
    try:
        all_articles = newsapi.get_everything(
            q=query,
            from_param=start_date,
            language='en',
            domains=financial_domains,
            sort_by='popularity'
        )
    except Exception as e:
        print(f"ERROR: Could not fetch articles for '{query}' from '{start_date}'. Check API or connection.")
        print(e)
        return None

    articles = all_articles.get('articles', [])

    if not articles:
        print(f"Could not find any articles for '{query}'.")
        return None

    print(f"Fetched {len(articles)} articles for '{query}'.")

    # Filter articles to only include those where the query appears in the title
    # This ensures relevance by focusing on articles directly mentioning the company
    relevant_articles = []
    for article in articles:
        title = article.get('title', '')
        if query.lower() in title.lower():
            relevant_articles.append(article)

    if not relevant_articles:
        print(f"Could not find any relevant articles for '{query}'.")
        return None

    print(f"Filtered to {len(relevant_articles)} relevant articles for '{query}'.")

    # Perform sentiment analysis on each relevant article
    results = []
    for article in relevant_articles:
        title = article.get('title', '')
        description = article.get('description', '')

        # Combine title and description for comprehensive sentiment analysis
        text_to_analyze = str(title) + ". " + str(description)

        # Calculate sentiment scores using VADER sentiment analyzer
        # Returns a dictionary with 'neg', 'neu', 'pos', and 'compound' scores
        sentiment_scores = analyzer.polarity_scores(text_to_analyze)

        # Extract compound score: normalized value between -1 (most negative) and +1 (most positive)
        compound_score = sentiment_scores['compound']

        results.append({
            'date': article['publishedAt'],
            'title': title,
            'compound_score': compound_score
        })

    # Convert results to DataFrame and sort by publication date (most recent first)
    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date', ascending=False)

    return df


def interpret_sentiment(df):
    """
    Interprets the overall sentiment from a DataFrame of sentiment scores.
    
    Args:
        df (pd.DataFrame): DataFrame containing 'compound_score' column with sentiment values.
    
    Returns:
        tuple: A tuple containing:
            - decision (str): Sentiment classification ('Positive', 'Negative', or 'Neutral')
            - average_score (float): Mean compound sentiment score across all articles
    """
    if df is None or df.empty:
        return "No data to analyze.", 0.0

    # Calculate the mean compound sentiment score across all articles
    average_score = df['compound_score'].mean()

    # Define thresholds for sentiment classification
    # Scores above 0.25 are considered positive, below -0.25 are negative
    POSITIVE_THRESHOLD = 0.25
    NEGATIVE_THRESHOLD = -0.25

    # Classify sentiment based on average compound score
    if average_score >= POSITIVE_THRESHOLD:
        decision = 'Positive'
    elif average_score <= NEGATIVE_THRESHOLD:
        decision = 'Negative'
    else:
        decision = 'Neutral'

    return decision, average_score

def run_project(COMPANY_QUERY, TIME_HORIZON_DAYS):
    """
    Main execution function that orchestrates the sentiment analysis workflow.
    Configure the company query and time horizon below before running.
    """
    # Configuration parameters: modify these to analyze different companies or time periods

    df_results = analyze_company_sentiment(COMPANY_QUERY, TIME_HORIZON_DAYS)

    if df_results is not None:
        # Display the top 5 most recent articles with their sentiment scores
        print("\nTop 5 analyzed articles:")
        print(df_results.head(5).to_markdown(index=False, numalign='left', stralign='left'))

        # Calculate and display overall sentiment interpretation
        decision, avg_score = interpret_sentiment(df_results)

        print("\n==============================================")
        print("            SENTIMENT VERDICT              ")
        print("==============================================")
        print(f"Company:                {COMPANY_QUERY}")
        print(f"Time Horizon Days:      {TIME_HORIZON_DAYS}")
        print(f"Sentiment Score:        {avg_score:.4f}")
        print(f"Interpretation:         {decision}")
        print("==============================================")


if __name__ == "__main__":
    # NewsAPI authentication key (required for accessing news articles)
    API_KEY = '<YOUR NEWSAPI KEY HERE>'

    # Initialize NewsAPI client and VADER sentiment analyzer
    newsapi = NewsApiClient(api_key=API_KEY)
    analyzer = SentimentIntensityAnalyzer()

    # Configuration parameters: modify these to analyze different companies or time periods
    COMPANY_QUERY = "Tesla"
    TIME_HORIZON_DAYS = 3

    if API_KEY is None:
        print("ERROR: No API key provided.")
    else:
        run_project(COMPANY_QUERY, TIME_HORIZON_DAYS)
