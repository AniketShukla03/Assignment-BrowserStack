import os
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

articles = [
    "https://elpais.com/opinion/2025-07-17/el-roto-nuevo-master.html",
    "https://elpais.com/opinion/2025-07-17/flavita-banana-proteccion-flotante.html",
    "https://elpais.com/opinion/2025-07-16/riki-blanco-bulos.html",
    "https://elpais.com/opinion/2025-07-17/peridis-pp-a-hombros-de-vox.html",
    "https://elpais.com/opinion/2025-07-16/jose-angel-antelo-por-sciammarella.html"
]

def download_image(url, path):
    try:
        response = requests.get(url)
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f" Failed to download image: {e}")
        return False

def main():
    print("\n Starting El País scraper...\n")
    translated_titles = []

    for i, url in enumerate(articles, 1):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('title').text.strip().replace(" | Opinión | EL PAÍS", "")
            translated_title = GoogleTranslator(source='auto', target='en').translate(title)
            translated_titles.append(translated_title)

            img_tag = soup.find('meta', property='og:image')
            image_url = img_tag['content'] if img_tag else None

            author_info = "Author info not found"
            author_tag = soup.find('span', class_='a_aut_n')
            if author_tag:
                author_info = author_tag.text.strip()

            print(f" Article {i}: {url}")
            print(f" Title (Spanish): {title}")
            print(f" Title (English): {translated_title}")
            print(f" Author Info: {author_info}")

            if image_url:
                image_path = f"images/article_{i}.jpg"
                if download_image(image_url, image_path):
                    print(f" Image saved to: {image_path}")
            print()

        except Exception as e:
            print(f" Error processing article {url}: {e}")

    # Word repetition analysis
    print(" Analyzing repeated words in translated titles...")
    word_counts = {}
    for title in translated_titles:
        for word in title.lower().split():
            word_counts[word] = word_counts.get(word, 0) + 1

    repeated = {k: v for k, v in word_counts.items() if v > 2}
    if repeated:
        print(" Repeated words (more than twice):", repeated)
    else:
        print(" No words repeated more than twice.")

# Make it callable
if __name__ == "__main__":
    main()

