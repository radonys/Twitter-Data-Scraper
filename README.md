# Twitter-Data-Scraper

Twitter Data Scraper using Python, Selenium and Google BigQuery

### Required Modules

- Selenium
- Pandas
- datetime
- google-cloud-bigquery
- pyarrow

### Other Requirements

- Firefox Browser (can be changed as per convenience)
- geckodriver (needed for Firefox webdriver, changes as per desired web browser)
- Enabled BigQuery API in GCP with **JSON key file** (follow steps [here](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries))

### How to run

1. Clone the repository.
2. Place the JSON key file in the repository.
3. Modify the filepaths for *geckodriver* and *JSON file* in the [Twitter_Data_Stream.py](https://github.com/radonys/Twitter-Data-Scraper/blob/main/Twitter_Data_Stream.py) or [Twitter_Data_Stream.ipynb](https://github.com/radonys/Twitter-Data-Scraper/blob/main/Twitter_Data_Stream.ipynb).
4. Change the **table_id** as per your configuration in the BiqQuery Console.
5. Open Terminal or Command-Line Interface with the repository as the current directory.
6. Execute ```pip install -r requirements.txt```.
7. After this, run ```python3 Twitter_Data_Stream.py```.

The code can be executed using Jupyter Notebook [Twitter_Data_Stream.ipynb](https://github.com/radonys/Twitter-Data-Scraper/blob/main/Twitter_Data_Stream.ipynb).

### Main Code Components

##### Scrape Tweet IDS

Input: Twitter User Handle (String)
Output: (Twitter ID (String), DateTime (String))

Description: 
- Initiate a Webdriver instance (Firefox here)
- Store unique ID,DateTime pairs in ids (Set)
- Load Twitter User page and added wait time for page load
- Finds all the "a" tags in the current browser with the status_format (String)
- Extracts datetime from the "time" tag
- The function collects the tweets for the current date.
- If date doesn't match with today's date, the flag becomes False and loop breaks.
- Else, the loop continues with page scrolling.

- Stale Element and Missing Tag errors are handled using try/except.

##### Scrape Tweet Data

Input: Twitter User Handle (String), Tweet ID (String)
Output: Tweet Data (Dictionary)

Description: 
- Initiate a Webdriver instance (Firefox here)
- Store unique hashtags, urls, mentions (Set)
- Load Twitter User page and added wait time for page load
- Finds all the "a" tags in the current browser with the twitter shortening format (String)
- Extracts data from the "span" tag with specific characters to determine hashtags and mentions. 

- Stale Element and Missing Tag errors are handled using try/except.

##### Driver Code

This code block calls the above described functions for each Twitter user in the *twitter_users* list and stores the data in a Pandas DataFrame *data*. This dataframe is pushed in the Google BigQuery using the BigQuery Python client.

### Major Considerations

- Considering the data streaming part, the collection of tweets everytime can be performed based on one of the two parameters: last tweet id collected or the date of execution.
- In this code, we collect data based on the current date of the system and hence there might be repetitions in the data table. This thing can be easily handled by removing duplicates using the tweet_id.
- Approach with last tweet id wasn't working properly (still working it out) and hence not incorporated in this submission considering the time-sensitivity of the assignment submission.
- The nature of data collection using Selenium can sometimes lead to dirty data and requiring data transformation.
- In this submission, I am using the batch upload method to update the BigQuery table since streaming isn't part of the free-tier GCP.

### Running Code as a constant data collector

- Since I am using batch upload mechanism, the Python code [Twitter_Data_Stream.py](https://github.com/radonys/Twitter-Data-Scraper/blob/main/Twitter_Data_Stream.py) can be used with **cronjob** or **Task Scheduler** scheduled to run as per the desired rate of execution.


