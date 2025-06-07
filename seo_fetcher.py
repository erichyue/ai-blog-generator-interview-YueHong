# seo_fetcher.py

import random

def fetch_seo_metrics(keyword: str) -> dict:
    """
    Mock version: return random SEO metrics for any given keyword.
    """
    search_volume = random.randint(500, 20000)
    keyword_difficulty = round(random.uniform(10, 80), 2)
    avg_cpc = round(random.uniform(0.5, 3.0), 2)

    return {
        "search_volume": search_volume,
        "keyword_difficulty": keyword_difficulty,
        "avg_cpc": avg_cpc
    }
