import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

# Pages worth trying
PAGES = [
    "",
    "/about",
    "/about-us",
    "/products",
    "/services",
    "/solutions",
    "/company",
    "/contact",
]

# Pages that indicate blocking / maintenance
BLOCKED_PHRASES = [
    "thank you for your patience",
    "currently experiencing high demand",
    "health beacon",
    "access denied",
    "just a moment",
    "cloudflare",
    "checking your browser",
    "enable javascript",
    "request blocked",
]


def get_page_text(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True,
        )

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Detect blocked pages
        lower = text.lower()

        if any(phrase in lower for phrase in BLOCKED_PHRASES):
            print(f"Blocked page detected: {url}")
            return ""

        lines = []

        for line in text.splitlines():
            line = line.strip()

            if len(line) < 3:
                continue

            lines.append(line)

        return "\n".join(lines)

    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return ""


def crawl_website(base_url):

    all_text = ""
    visited = set()
    successful_pages = 0

    for page in PAGES:

        url = urljoin(base_url, page)

        if url in visited:
            continue

        visited.add(url)

        print(f"Crawling: {url}")

        text = get_page_text(url)

        if text:
            successful_pages += 1
            all_text += "\n\n" + text

    # Remove duplicate lines
    unique = []
    seen = set()

    for line in all_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line in seen:
            continue

        seen.add(line)
        unique.append(line)

    final_text = "\n".join(unique)

    print(f"Pages crawled: {successful_pages}")
    print(f"Characters extracted: {len(final_text)}")

    return {
        "full_text": final_text,
        "ai_text": final_text[:8000],
        "total_chars": len(final_text),
        "pages_crawled": successful_pages,
    }