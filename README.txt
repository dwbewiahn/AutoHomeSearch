# AutoHomeSearch

AutoHomeSearch is a Python script that searches for apartments for rent in a specific region on the OLX website and alerts the user if a new apartment that meets certain criteria has been posted. 

## How it works

The script uses the requests and json libraries to scrape data from the OLX website. The data is filtered based on a set of predefined search filters such as category, city, price range, and number of rooms. If a new apartment is found that meets the search criteria, the script uses the winsound library to play an alert sound and prints the details of the apartment to the console.

The search is set to run every 5 minutes by default, but this can be adjusted as needed.

## Requirements

- Python 3.x
- requests
- json
- winsound
- schedule

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/dwbewiahn/AutoHomeSearch.git
   ```

2. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

3. Update the search filters in the `search_filters` dictionary to match your preferences. 

4. Run the script:

   ```
   python home_searcher.py
   ```

## Note

- The script is currently set up to only search for apartments in a specific region on the OLX website. You can update the `search_filters` dictionary to search for apartments in different regions by changing the city ID.

- The `pushover_notifier.py` file is not included in this repository. If you want to receive push notifications when a new apartment is found, you will need to create your own `pushover_notifier.py` file and replace the `TODO` comment in the `is_new_apartment()` function with the appropriate function call.