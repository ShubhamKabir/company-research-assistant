from services.crawler import crawl_website

text = crawl_website("https://www.microsoft.com")

print("Characters:", len(text))
print()
print(text[:2000])