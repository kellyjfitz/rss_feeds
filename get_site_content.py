from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pystache as PS 

# Create a new instance of the Edge driver
service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)

def get_view():
    articles = []
    links_to_process = []

    # Go to the website
    driver.get("https://view.com.au/news/national/")

    # Find all <section> elements on the page
    sections = driver.find_elements(By.TAG_NAME, 'section')

    for section in sections:
        # Find all <article> elements within this <section>
        articles_in_section = section.find_elements(By.TAG_NAME, 'article')

        for article in articles_in_section:
            # Find all <a> elements within this <article>
            links = article.find_elements(By.TAG_NAME, 'a')

            # Print out the URLs of all the links
            for link in links:
                url = link.get_attribute('href')
                if url and url.startswith('https://view.com.au/news/national/') and url != 'https://view.com.au/news/national/':
                    print(url)
                    links_to_process.append(url)

    for link in links_to_process:
        get_article(link, articles)                

    with open ("template.mustache", "r") as file:
        template = file.read()

    rendered = PS.render(template, {"items": articles})

    with open ("rss_test.xml", "w") as file:
        file.write(rendered)


def get_article(url, articles):

    # Go to the website
    driver.get(url)  # replace with your URL

    # Get the title
    title = driver.find_element(By.XPATH, '//meta[@property="og:title"]')
    headline = title.get_attribute('content')

    # Get the meta description tag
    meta_description = driver.find_element(By.XPATH, '//meta[@name="description"]')
    description = meta_description.get_attribute('content')

    # Get the image url
    meta_image = driver.find_element(By.XPATH, '//meta[@property="og:image"]')
    image = meta_image.get_attribute('content')

    # Get the pub date
    meta_date = driver.find_element(By.XPATH, '//meta[@property="article:published_time"]')
    pub_date = meta_date.get_attribute('content')

    item = {"headline": headline, "description": description, "image": image, "pub_date": pub_date, "url": url}

    articles.append(item)

    #for later getting the data
    # # Find the <h1> element on the page
    # h1 = driver.find_element(By.TAG_NAME, 'h1')

    # headline = h1.text
    # # Print out the text of the <h1> element
    # print("headline: ", headline)

    # # Find the <div> element with the class 'pt-2 md:pt-4'
    # div = driver.find_element(By.CSS_SELECTOR, 'div.pt-2.md\\:pt-4')

    # # Find all <p> elements within this <div>
    # pars = div.find_elements(By.TAG_NAME, 'p')

    # # Print out the text of all the <p> elements
    # for par in pars:
    #     print(par.text)

get_view()