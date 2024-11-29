"""
Reddit Comment Analyzer with Full Documentation
This script analyzes Reddit comments for Gen Z slang usage.
It connects to Reddit's API, processes comments, and outputs statistics.

Key Features:
- Analyzes comments from a specified subreddit
- Counts Gen Z slang word usage
- Calculates a 'Gen Z Score' based on slang density
- Saves results to a CSV file

Required libraries:
- praw: Reddit API wrapper
- pandas: Data handling and CSV creation
- configparser: Reading Reddit credentials
"""

# Import required libraries. Each import serves a specific purpose
import praw  # Provides Reddit API access functionality
from datetime import datetime  # For creating timestamps on our files
import pandas as pd  # For creating and saving CSV files
import configparser  # For reading our Reddit API credentials
import sys  # For system functions like exiting program
from collections import Counter  # Specialized dictionary for counting


class RedditCommentAnalyzer:
    def __init__(self):
        """
        Class constructor: Initializes the analyzer with slang words and Reddit connection.
        This method runs automatically when creating a new RedditCommentAnalyzer object.
        Similar to a constructor in Java/C++.
        """
        # Define list of Gen Z slang terms to look for
        # Using a list for easy modification and maintenance
        self.keywords = [
            'rizz', 'gyatt', 'fr', 'fr fr', 'frfr', 'no cap', 'cap', 'bussin', 'bussin bussin',
            'slay', 'slayed', 'slaying', 'based', 'mid', 'valid', 'invalid', 'taking Ls',
            'taking Ws', 'common L', 'common W', 'rare L', 'rare W', 'massive L', 'massive W',
            'huge L', 'huge W', 'bruh', 'bruhhh', 'skull', '💀', 'crying', 'im dead', "i'm dead",
            'ded', 'wheeze', 'screaming', 'down bad', 'down horrendous', 'touch grass',
            'grass touched', 'unspoken rizz', 'no rizz', 'negative rizz', 'infinite rizz', 'ngl',
            'idk', 'idc', 'tbh', 'imo', 'imho', 'istg', 'iykyk', 'iirc', 'nvm', 'tbf', 'ratio',
            'counter ratio', 'ratioed', 'rent free', 'living rent free', 'main character', 'npc',
            'caught in 4k', 'in 4k', 'pov', 'literally me', 'lowkey', 'highkey', 'hits different',
            'hitting different', 'real', 'so real', 'peak', 'bottom tier', 'top tier', 'no shot',
            "ain't no way", 'deadass', 'on god', 'ong', 'sheesh', 'sheeesh', 'skibidi', 'ohio',
            'real ohio moment', 'chad', 'sigma', 'alpha', 'beta', 'karen', 'boomer', 'zoomer',
            'copium', 'hopium', 'propaganda', 'fam', 'bestie', 'bestie moment', 'material', 'tea',
            'spill the tea', 'pressed', 'salty', 'sus', 'sus af', 'goated', 'actually goated',
            'cracked', 'built different', 'different breed', 'trash', 'garbage', "ain't it",
            'no printer', 'straight fax', 'heard you', 'say less', 'bet', 'facts', 'big facts',
            'rizz god', 'sleeping on', 'giving', 'era', 'vibe check', 'understood the assignment',
            'passes the vibe check', 'failed the vibe check', 'clapped', 'bozo', 'deadass',
            'finna', 'hits', 'period', 'periodt', 'purr', 'respectfully', 'throwing shade',
            'yeet', 'hits', 'smoking that pack', 'caught in hd', 'ate', 'devious lick', 'til',
            'afaik', 'goat', 'rn', 'mf', 'fs', 'w rizz', 'big w', 'major l', 'huge l', 'tfw',
            'mfw', 'me when', 'mood', 'based and redpilled', 'cope', 'drip', 'clean', 'fire',
            'gas', 'slaps', 'caught lacking', 'on god', 'fr on god', 'no printer just fax',
            'sadge', 'poggers', 'thicc', 'kinda', 'cringe', 'woke', 'toxic', 'main character energy'
        ]

        # Initialize Reddit API connection using our credentials
        self.reddit = self.setup_reddit()

    def setup_reddit(self):
        """
        Establishes connection to Reddit using credentials from config file.

        Returns:
        - praw.Reddit object if successful
        - Exits program if credentials are invalid or missing

        The config file (reddit_config.ini) should contain:
        [REDDIT]
        client_id=your_client_id
        client_secret=your_client_secret
        user_agent=your_user_agent
        """
        # Create configparser object to read .ini file
        config = configparser.ConfigParser()

        try:
            # Attempt to read credentials from config file
            config.read('reddit_config.ini')

            # Create and return Reddit instance using credentials
            return praw.Reddit(
                client_id=config['REDDIT']['client_id'],  # App ID from Reddit
                client_secret=config['REDDIT']['client_secret'],  # App secret from Reddit
                user_agent=config['REDDIT']['user_agent']  # Identifies our script to Reddit
            )
        except:
            # If anything goes wrong (file missing, wrong format, etc.)
            print("Error: Please ensure reddit_config.ini exists with your API credentials")
            sys.exit(1)  # Exit program with error code 1

    def calculate_gen_z_score(self, total_keywords, total_words):
        """
        Calculates a score from 0-100 based on slang word density.

        Parameters:
        - total_keywords: Total number of slang words found
        - total_words: Total number of words analyzed

        Returns:
        - Integer score between 0 and 100

        Formula: (total_keywords / total_words) * 200, capped at 100
        This means 50% slang would score 100, 5% would score 10, etc.
        """
        # Avoid division by zero
        if total_words == 0:
            return 0

        # Calculate density score
        density = (total_keywords / total_words) * 200

        # Cap score at 100 and round to nearest integer
        return min(100, round(density))

    def analyze_comment(self, comment_text):
        """
        Analyzes a single comment for slang word usage.

        Parameters:
        - comment_text: String containing the comment text

        Returns:
        - Dictionary with slang words as keys and their counts as values

        Example:
        "bruh bruh that's based" -> {'bruh': 2, 'based': 1}
        """
        # Convert comment to lowercase for case-insensitive matching
        text = comment_text.lower()

        # Create Counter object to track word frequencies
        keyword_counts = Counter()

        # Check each slang word
        for keyword in self.keywords:
            # Count occurrences of this slang word
            count = text.count(keyword.lower())
            # If found, add to our counter
            if count > 0:
                keyword_counts[keyword] = count

        # Convert Counter to regular dictionary and return
        return dict(keyword_counts)

    def analyze_subreddit_comments(self, subreddit_name, comment_limit=1000):
        """
        Main analysis function that processes subreddit comments.

        Parameters:
        - subreddit_name: Name of subreddit to analyze (without r/)
        - comment_limit: Maximum number of comments to analyze (default 1000)

        Process:
        1. Connects to subreddit
        2. Gets comments
        3. Analyzes each comment for slang
        4. Calculates statistics
        5. Saves results to CSV
        """
        try:
            # Connect to specified subreddit
            subreddit = self.reddit.subreddit(subreddit_name)

            # Initialize counting variables
            total_words = 0  # Total words in all comments
            total_slang = 0  # Total slang words found
            keyword_counts = Counter()  # Tracks each slang word's frequency
            comments_with_slang = 0  # Comments containing any slang
            processed_comments = 0  # Total comments processed

            print(f"\nAnalyzing {comment_limit} comments from r/{subreddit_name}...")

            # Process each comment from the subreddit
            for comment in subreddit.comments(limit=comment_limit):
                try:
                    # Skip deleted or removed comments
                    if comment.body in ['[deleted]', '[removed]']:
                        continue

                    # Analyze this comment
                    comment_keywords = self.analyze_comment(comment.body)
                    # Count total words (split on whitespace)
                    words_in_comment = len(comment.body.split())
                    total_words += words_in_comment

                    # If comment contains slang
                    if comment_keywords:
                        comments_with_slang += 1
                        # Update our slang word counter
                        keyword_counts.update(comment_keywords)
                        # Add to total slang word count
                        total_slang += sum(comment_keywords.values())

                    # Track progress
                    processed_comments += 1
                    # Show progress every 100 comments
                    if processed_comments % 100 == 0:
                        print(f"Processed {processed_comments} comments...")

                except Exception as e:
                    print(f"Error processing comment: {e}")
                    continue

            # Calculate final score
            gen_z_score = self.calculate_gen_z_score(total_slang, total_words)

            # Save results to CSV
            self.save_results(
                subreddit_name,
                gen_z_score,
                processed_comments,
                comments_with_slang,
                total_words,
                total_slang
            )

            # Display results to user
            print("\nAnalysis Complete!")
            print(f"Gen Z Score: {gen_z_score}/100")
            print(f"Comments Analyzed: {processed_comments}")
            print(f"Comments With Slang: {comments_with_slang}")
            print(f"Total Words: {total_words}")
            print(f"Total Slang Words: {total_slang}")

        except Exception as e:
            print(f"Error analyzing subreddit: {e}")

    def save_results(self, subreddit_name, score, total_comments,
                     comments_with_slang, total_words, total_slang):
        """
        Saves analysis results to a CSV file.

        Parameters contain all statistics to save.
        Creates a timestamped file name to avoid overwriting.

        File format:
        subreddit_analysis_YYYYMMDD_HHMMSS.csv
        """
        # Create timestamp for unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{subreddit_name}_analysis_{timestamp}.csv"

        # Prepare data for CSV
        # Creating a dictionary that will become a single row in our CSV
        data = {
            'Subreddit': subreddit_name,
            'Gen_Z_Score': score,
            'Total_Comments': total_comments,
            'Comments_With_Slang': comments_with_slang,
            'Total_Words': total_words,
            'Total_Slang_Words': total_slang,
            'Analysis_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Create DataFrame with our data (pandas handles CSV creation)
        df = pd.DataFrame([data])
        # Save to CSV file (index=False means don't save row numbers)
        df.to_csv(filename, index=False)
        print(f"\nResults saved to {filename}")


def main():
    """
    Main function - program starts here.
    Gets user input and runs the analysis.
    """
    # Create analyzer object
    analyzer = RedditCommentAnalyzer()

    # Get subreddit name from user (strip removes whitespace)
    subreddit_name = input("Enter subreddit name to analyze (without r/): ").strip()

    # Get number of comments to analyze, with error handling
    try:
        # The 'or 1000' means use 1000 if no input given
        comment_limit = int(input("Enter number of comments to analyze: ") or 1000)
    except ValueError:
        # If input isn't a valid number, use default
        comment_limit = 1000

    # Run the analysis
    analyzer.analyze_subreddit_comments(subreddit_name, comment_limit)


# This checks if the script is being run directly (not imported)
if __name__ == "__main__":
    main()