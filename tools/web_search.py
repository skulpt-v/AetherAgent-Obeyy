from duckduckgo_search import DDGS


class WebSearch:
    """AetherAgent için web arama aracı."""

    def __init__(self):
        """Web arama sistemini başlatır."""
        self.search_engine = DDGS()

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Web'de arama yapar ve sonuçları döndürür."""

        if not query or not query.strip():
            return []

        results = []

        try:
            search_results = self.search_engine.text(
                query,
                max_results=limit
            )

            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })

        except Exception as error:
            print(f"Web arama hatası: {error}")

        return results
