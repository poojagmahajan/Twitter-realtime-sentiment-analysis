# Twitter_Sentiment_Analysis

## Introduction
Sentiment analysis on twitter data related to certain topic using specific keywords.
You can give any keywords or hashtags as input to get data for analysis.

## Requirements
- python >3.5
- Any Editor(I used pycharm)

## Installation
- Pandas `pip install pandas`
- numpy  `pip install numpy`
- Tweepy `pip install tweepy`
- Textblob `pip install TextBlob`
- argparser `pip install argparse`
- csv  `pip install csv`
- re  `pip install re`
- matplotlib `pip install matplotlib`


## How to use

Run code file `Sentiment_Analysis.py`

Bellow is __help__ of code
```
usage: Sentiment_Analysis.py [-h] -H HASHTAG_LIST -s SINCE_DATE -u UNTIL_DATE
                             [-g GEOCODE] [-l LANGUAGE] -f FILE -c COUNT

optional arguments:
  -h, --help            show this help message and exit
  -H HASHTAG_LIST, --hashtag_list HASHTAG_LIST
                        comma seperated list of hashtags to analyse
  -s SINCE_DATE, --since_date SINCE_DATE
                        since date
  -u UNTIL_DATE, --until_date UNTIL_DATE
                        until date
  -g GEOCODE, --geocode GEOCODE
                        geographical code of india
  -l LANGUAGE, --language LANGUAGE
                        language of tweets
  -f FILE, --file FILE  filename to store tweets
  -c COUNT, --count COUNT
                        number of tweets required

```

Sample __input__ should be like :
```
-f data.csv -H "Sushant Singh Rajput,#JusticeforSushantSingRajput" -s 2020-08-23 -u 2020-08-29 -c 100

```

Sample __output__ should be like this :


![output_piechart](https://github.com/poojagmahajan/Twitter_Sentiment_Analysis/blob/master/output_piechart.png)


## Files description
Bellow is information about file that directory contains :

- __code__ file is `Sentiment_Analysis.py`
- __Sample Data__ collected in`data.csv`
- All your __twitter credentials__ should be define in file `twitter_credentials.py`


## Contributing to project
To contribute to <project_name>, follow these steps:

- Fork this repository.
- Create a branch: `git checkout -b <branch_name>`.
- Make your changes and commit them: `git commit -m '<commit_message>'`
- Push to the original branch: `git push origin <project_name>/<location>`
- Create the pull request.

Please fork and give credits if you use my code. :smile:

Alternatively see the GitHub documentation on [creating a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)

 
## Contact
If you want to contact me you can reach me at __(mahajanpoojag@gmail.com)__.


## License 
This project uses the following license:
[Apache License 2.0](https://github.com/poojagmahajan/Twitter_Sentiment_Analysis/blob/master/LICENSE.txt)


