# Web Scraping and Book Price Analysis

## Project Overview

This project demonstrates an end-to-end data analysis workflow using web scraping.

The project collects book information from the Books to Scrape website, cleans the scraped data, performs exploratory data analysis, and creates visualizations to identify patterns in book prices, ratings, and categories.

## Objectives

- Scrape book data from multiple pages
- Collect book title, price, rating, category, availability, and product URL
- Clean and transform the scraped data
- Perform exploratory data analysis using Pandas
- Create visualizations using Matplotlib
- Identify relationships between book price and rating
- Analyze average prices across book categories

## Dataset

The dataset contains information for 1,000 books scraped across 50 pages.

### Columns

| Column | Description |
|---|---|
| title | Title of the book |
| price | Book price in pounds |
| rating | Book rating from 1 to 5 |
| category | Book category |
| availability | Availability status |
| product_url | URL of the individual book |

## Tools and Technologies

- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- Jupyter Notebook
- VS Code

## Project Structure

```text
web-scraping-books/
│
├── data/
│   └── books.csv
│
├── src/
│   └── scraper.py
│
├── notebooks/
│   └── analysis.ipynb
│
├── README.md
├── requirements.txt
└── .gitignore

