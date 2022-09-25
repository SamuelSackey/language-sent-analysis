import tweepy
import pandas as pd
import os

api_key = 'kkBWYP1Vh3qwIUQZtnDcwZpSi'
api_key_secret = 'LA2BILmgo8Jn2BiKsRCFa7muUyPqjE6aStNL96iT4E6dMlZOhn'
access_token = 'REx5dnpzS1ZiVGJrMG11SE5vTFo6MTpjaQ'
access_secret = 'e777iEEupUDprYJ3FjkbMdVH4do9r6J1ZPu3L85CBqbjOyqvvS'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALmDhAEAAAAAo00TTYY5BIu%2FcnSpPmpHGzlk7Ro%3Dw6fjC6W57HeVqQkthB5royMsaHfAkBBx9FoZNZmjUVvux8YSpK'


client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# programming languages
languages = ["C", "Go", "Java", "C#", "F#", "Haskell", "Python", "Ruby"]

# year ranges
years = [("2015", "2016"), ("2016", "2017"), ("2017", "2018"),
         ("2018", "2019"), ("2019", "2020"), ("2020", "2021"), ("2021", "2022")]

for language in languages:
    # Create directory
    path = os.path.join(os.getcwd(), language)
    os.makedirs(path, exist_ok=False)

    for year in years:
        # format query
        query = f'{language} language OR python programming lang:en'

        # format correct time and date
        start = f'{year[0]}-06-01T00:00:00.000Z'

        end = f'{year[1]}-05-01T00:00:00.000Z'

        frames = []

        for tweets in tweepy.Paginator(
            client.search_all_tweets,
            query=query,
            tweet_fields=['id', 'text'],
            start_time=start,
            end_time=end,
            max_results=500
        ).flatten(limit=2000):

            frames.append({
                "id": tweets.id,
                "year": year[1],
                "language": language,
                "text": tweets.text
            })

        #  log
        print(language + "-" + year[1] + " | count: ", {len(frames)})

        # Create data frame
        tweets_df = pd.DataFrame(frames)
        print(tweets_df.head())

        # dimensions
        print("Shape: ", tweets_df.shape)

        # Save to CSV
        tweets_df.to_csv(f'{language}/{language}_{year[1]}.csv',
                         encoding='utf-8', index=False)
