# FiveStar Property Scrapy Scraper

<a href="https://codeclimate.com/github/Firiyuu/scrapy-fivestarproperties/maintainability"><img src="https://api.codeclimate.com/v1/badges/bc9c6e930ec3c029ac3f/maintainability" /></a>

Scraping a javascript-based website using scrapy and a lil' bit of selenium, saved to mongodb.

It saves:

```bash
- Property Name
- Url
- Details
- Bedroom/Bathroom/Sleeps
- Description
- Image urls
- Images (Saved at images folder )
```

## Use

Use this command to download all urls within the website that we need, since this website needs to be navigated in order to get the urls because of JS. So we need to get inside each image container get the url

```bash
cd hotelschecker
scrapy crawl hotels
```

All the urls that was saved to the db will then be used by the next spider

```bash
cd hotelschecker
scrapy crawl sites
```
