import requests
from bs4 import BeautifulSoup


class WebScraper:
    """Web sayfalarının içeriğini temiz metne dönüştürür."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch(self, url: str) -> str:
        """URL'deki sayfayı indirip temiz metin olarak döndürür."""

        if not url or not url.strip():
            return ""

        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64)"
                    )
                }
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Gereksiz HTML elemanlarını kaldır.
            for element in soup([
                "script",
                "style",
                "noscript",
                "nav",
                "footer"
            ]):
                element.decompose()

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            return text

        except requests.RequestException as error:
            print(f"Sayfa indirme hatası: {error}")
            return ""

        except Exception as error:
            print(f"Scraper hatası: {error}")
            return ""

