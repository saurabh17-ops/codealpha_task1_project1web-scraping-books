import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import time


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"


def get_category(product_url):

    try:
        response = requests.get(product_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Find the breadcrumb navigation
        breadcrumb = soup.select("ul.breadcrumb li")

        # The category is the third breadcrumb item
        if len(breadcrumb) >= 3:
            category = breadcrumb[2].get_text(strip=True)
            return category

        return "Unknown"

    except requests.RequestException as e:
        print(f"Category error: {e}")
        return "Unknown"

def scrape_books():

    books_data = []

    for page in range(1, 51):

        url = BASE_URL.format(page)

        print(f"Scraping page {page}: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

        except requests.RequestException as e:
            print(f"Error while scraping page {page}: {e}")
            continue

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        books = soup.find_all(
            "article",
            class_="product_pod"
        )

        for book in books:

            title = book.h3.a["title"]

            price = book.find(
                "p",
                class_="price_color"
            ).text.strip()

            availability = book.find(
                "p",
                class_="instock availability"
            ).text.strip()

            rating_class = book.find(
                "p",
                class_="star-rating"
            )["class"]

            rating = rating_class[1]

            product_url = urljoin(url, book.h3.a["href"])

            print(f"  Getting category: {title}")

            category = get_category(product_url)

            books_data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "category": category,
                "availability": availability,
                "product_url": product_url
            })

            time.sleep(0.1)

        time.sleep(0.5)

    return books_data


def clean_data(data):

    df = pd.DataFrame(data)

    # Clean price
    df["price"] = (
        df["price"]
        .str.replace("£", "", regex=False)
        .str.replace("Â", "", regex=False)
        .str.strip()
        .astype(float)
    )

    # Convert rating words to numbers
    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["rating"].map(rating_mapping)

    # Clean availability
   df["availability"] = (
    df["availability"]
    .str.replace("\n", "", regex=False)
    .str.strip()
)

df["category"] = df["category"].replace(
    ["Default", "Add a comment"],
    "Unknown"
)

df = df.drop_duplicates()

    return df


if __name__ == "__main__":

    print("Starting web scraping...\n")

    data = scrape_books()

    print(f"\nTotal books scraped: {len(data)}")

    df = clean_data(data)

    df.to_csv(
        "data/books.csv",
        index=False
    )

    print("\nData cleaning completed.")

    print("\nFirst 5 records:")
    print(df.head())

    print("\nDataset information:")
    df.info()

    print("\nDataset saved successfully:")
    print("data/books.csv")