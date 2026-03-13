<a name="readme-top"></a>

<br />
<div align="center">

  <h3 align="center">Meta Spy</h3>

  <p align="center">
    Meta Spy is a versatile Python-based tool designed to scrape various data from Instagram profiles and Facebook  profiles, pages and search results. Whether you need basic information or want to delve deep into a user's activity, Facebook Spy has you covered. 
    <br />
    <br />
</div>



## Info

If you're using a Facebook account with a custom ID in the URL (e.g., https://www.facebook.com/zuck), Facebook Spy will work smoothly. However, for accounts with default IDs in the URL, certain scrapers may not function as expected. These include scrapers for work and education, contact data, visited places, family members, recent places, reviews, and likes. Rest assured, we're actively working to resolve this issue

<!-- ABOUT THE PROJECT -->
## About The Project

The project, known as "Meta Spy," is a powerful and versatile tool designed to gather information from Facebook profiles, pages and search results. 

The project is under constant development to improve its functionality and address any issues that may arise.



## Key Features
- Login - Perform a secure two-step verification process to log in to Facebook account with enhanced security settings or log in to Facebook account using the default login method.
- Scrape details like: friend list, images, recent places, videos, reels, reviews, posts, likes, groups, events etc.
- Local web application - User is able to run a loval web application to browse scraped data, create notes for specified Person object and easly search details in web.
- Create a graphical representation of connections between different Facebook profiles based on their friendships.
- Initiate a friend crawler for a specified Facebook account. Gether data about friends and contunue the process for subsequent users in the queue.
- Save scraped data for a specified Facebook user to PDF file for documentation and anylysis.
- Running scrapers in parallel to speed up the data collection process
- Save all scraped data to JSON files and database 

### Built With

- Python
  - Typer 
  - FastAPI
  - Selenium
- SQLite 
- HTML / CSS / Bootstrap5

<!-- GETTING STARTED -->
## Getting Started


### Installation

1. Clone git repository
```bash
git clone https://github.com/DEENUU1/meta-spy.git
```

2. Create dotenv file and add required data
```bash
cp .env_example .env
```

3. Install all requirements
```bash
pip install -r requirements.txt
```

4. Change directory to metaspy to run commands
```bash
cd metaspy
```

### Tests

To run pytests use this command
```bash
pytest
```


## Examples
This is just a few examples of how you can use this tool. For more comments check <a href="https://deenuu1.github.io/facebook-spy/commands/>">Documentation</a>

#### Version

```bash
python main.py version
```

<img src="assets/newversion.png" alt="Logo" >


#### Login

```bash
python main.py login-2-step
```

OR

```bash
python main.py login
```

  <img src="assets/new/login.png" alt="Logo" >


#### Search
```bash
python main.py fb-search <"Search Query"> <results> <option_1> <option_2> ... 

Options:
--post # Search for posts based on given query
--results # Number of results 
--people # Search for people based on given query
--group # Search for group based on given query
--place # Search for place based on given query
--event # Search for event based on given query
--page # Search for page based on given query
```

<img src="https://github.com/DEENUU1/facebook-spy/blob/main/assets/v1_2/search.gif?raw=true" alt="Logo" >


#### Scrape Facebook account/page
```bash
python main.py fb-account <facebook_id> <option_1> <option_2> ...

Options:
--work # Scrape work and education information from the given facebook account
--contact # Scrape contact data from the given facebook account
--location # Scrape location data from the given facebook account
--family # Scrape family members data from the given facebook account
--name # Scrape full name from the given facebook account
--friends # Scrape friends list from the given facebook account 🛑 Page not support
--images # Scrape images from the given facebook account 
--recent # Scrape recent places from the given facebook account 🛑 Page not support
--reels # Scrape urls for reels from the given facebook account
--reviews # Scrape reviews from the given facebook account
--videos # Scrape urls for videos from the given facebook account
--da # Download all videos from the given facebook account
--dn # Download only new videos from the given facebook account
--posts # Scrape all posts from the given facebook account
--details # Scrape details of posts from the given facebook account
--likes # Scrape likes from the given facebook account
--groups # Scrape groups from the given facebook account
--events # Scrape events from the given facebook account
```

#### Scrape Instagram account
```bash
python  main.py insta-account <id> <option_1> <option_2> ...

Options:
--images
--stats
```

#### Friend crawler
This command works similarly to the command that scrapes data about a given user's friends list. The difference, however, is that after scraping and creating Friend objects, it also creates objects for the CrawlerQueue model and after successfully scraping friends for one user, it proceeds to scraping the list of friends for the next user in the queue.
```bash
python main.py friend-crawler <facebook_id>
```

<img src="assets/new/crawler1.png" alt="Logo" >
<img src="assets/crawlerfriendscheama.png.png" alt="Logo" >


#### Graph
Graph of connections between Person objects based on ther friends.

```bash
python main.py graph
```

<img src="assets/graph.png" alt="Logo" >

<!-- LICENSE -->
## License

See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DEENUU1/facebook-spy.svg?style=for-the-badge
[contributors-url]: https://github.com/DEENUU1/facebook-spy/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DEENUU1/facebook-spy.svg?style=for-the-badge
[forks-url]: https://github.com/DEENUU1/facebook-spy/network/members
[stars-shield]: https://img.shields.io/github/stars/DEENUU1/facebook-spy.svg?style=for-the-badge
[stars-url]: https://github.com/DEENUU1/facebook-spy/stargazers
[issues-shield]: https://img.shields.io/github/issues/DEENUU1/facebook-spy.svg?style=for-the-badge
[issues-url]: https://github.com/DEENUU1/facebook-spy/issues
[license-shield]: https://img.shields.io/github/license/DEENUU1/facebook-spy.svg?style=for-the-badge
[license-url]: https://github.com/DEENUU1/facebook-spy/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/kacper-wlodarczyk
[basic]: https://github.com/DEENUU1/facebook-spy/blob/main/assets/v1_2/basic.gif?raw=true
[full]: https://github.com/DEENUU1/facebook-spy/blob/main/assets/v1_2/full.gif?raw=true
[search]: https://github.com/DEENUU1/facebook-spy/blob/main/assets/v1_2/search.gif?raw=true
