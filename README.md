# Company Sentiment Analyzer

This script analyzes the sentiment of news articles for a given company using the NewsAPI and VADER sentiment analysis.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Get a NewsAPI Key:**
   - Go to [newsapi.org](https://newsapi.org) and register for a free API key.

2. **Configure the script:**
   - Open `analyzer.py` and replace `<YOUR NEWSAPI KEY HERE>` with your actual NewsAPI key.
   - You can also change the `COMPANY_QUERY` and `TIME_HORIZON_DAYS` variables in the `if __name__ == "__main__":` block to analyze different companies or time periods.

3. **Run the script:**
   ```bash
   python analyzer.py
   ```

## Output

The script will print the following to the console:

- **Top 5 Analyzed Articles:** A table showing the 5 most recent articles, including their publication date, title, and sentiment compound score. The compound score ranges from -1 (most negative) to +1 (most positive).

- **Sentiment Verdict:** A summary of the analysis, including:
    - **Company:** The company that was analyzed.
    - **Time Horizon Days:** The number of days back that were analyzed.
    - **Sentiment Score:** The average compound sentiment score of all the analyzed articles.
    - **Interpretation:** The overall sentiment interpretation, which can be 'Positive', 'Negative', or 'Neutral'.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

