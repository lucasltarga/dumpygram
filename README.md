# Dumpygram

Python script based on Instaloader library used to download comments from Instagram posts.

## Features
- Delay between requests to avoid Instagram block.
    - From 1.5s to 4s between comments;
    - From 1.5 to 3s between replies;
    - From 12s to 25s between posts;
    - From 15s to 30s between tries (if error).
- Preview post details while downloading comments.
    - Caption (first 100 characters);
    - Likes count.
- Support for automatic comments extraction from multiple posts.
- Export comments to CSV file.
    - CSV file contains post shortcode, comment ID, reply flag, parent ID (if it is a reply), comment date, username, comment text and likes. 


## Requisites
- Python 3+
- Instaloader
- dotenv
- pandas

## Installation (Linux)
First of all, you need to [install Python](https://wiki.python.org/moin/BeginnersGuide/Download).

Download the dumpygram code or clone this repository using the following command:
```
git clone https://github.com/lucasltarga/dumpygram.git
```

Navigate to the downloaded dumpygram folder before running the next commands.

### Using virtual environments
Virtual environments are important to avoid version conflicts between different projects and respective installed libraries.

**1. Create a virtual environment**
```
python -m venv venv
```

**2. Activate the virtual environment before installing the dependencies**
```
source ./venv/bin/activate
```

### Installing the dependencies
**1. Run this command to install the dependencies**
```
pip install instaloader dotenv pandas
```

## How to use
**1. Copy and paste the following text in a .env file created in the dumpygram folder**

```
ACCOUNT = "USERNAME"
PASSWORD = "PASSWORD"

POSTS = "ID_1, ID_2"
```

Replace USERNAME and PASSWORD with actual credentials that will be used to scrape data. It is considerably harder to scrape Instagram data without logging in.

Replace POSTS list with desired Instagram posts shortcodes separated with commas. You can locate the shortcodes in the posts URL as follows: www.instagram.com/p/SHORTCODE/

**2. Run the script**

If you have installed the dependencies using a virtual environment, make sure the venv is active before running the script.

```
python main.py
```

**3. Wait for the proccess to finish**

The script will show details from the post and comments being downloaded. For each post, a CSV will be saved after completing the download.