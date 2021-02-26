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


