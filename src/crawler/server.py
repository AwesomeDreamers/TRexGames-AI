from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import httpx
import asyncio

mcp = FastMCP("WebCrawler")

STEAM_HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

STEAM_COOKIES = {
    "birthtime": "568022401",
    "lastagecheckage": "1-January-1988",
    "mature_content": "1"
}


async def fetch_detail(client, title, url):
    try:
        resp = await client.get(url, headers=STEAM_HEADERS, cookies=STEAM_COOKIES)
        soup = BeautifulSoup(resp.text, "html.parser")

        # 설명
        desc_tag = soup.select_one("div.game_description_snippet")
        description = desc_tag.text.strip() if desc_tag else "설명 없음"

        # 가격
        price_tag = soup.select_one(".discount_final_price") or soup.select_one(".game_purchase_price.price")
        price = price_tag.text.strip() if price_tag else "가격 정보 없음"

        # 발매일
        release_tag = soup.select_one(".date")
        release_date = release_tag.text.strip() if release_tag else "발매일 정보 없음"

        # 카테고리 (두번째 a태그 가져옴)
        category_tag = soup.select("div.blockbg a")
        category = category_tag[1].text.strip() if len(category_tag) >= 2 else "카테고리 없음"

        # 대표 이미지 URL (스팀 클라우드)
        image_tag = soup.select_one("div#gameHeaderImageCtn img")
        image_url = image_tag["src"].strip() if image_tag and image_tag.has_attr("src") else "이미지 없음"

        return {
            "title": title,
            "url": url,
            "description": description,
            "price": price,
            "release_date": release_date,
            "category": category,
            "image": image_url
        }
    except Exception as e:
        return {
            "title": title,
            "url": url,
            "error": str(e)
        }


@mcp.tool()
async def get_top_100_games_async() -> list[dict]:
    """스팀 인기 게임 100개 (성인인증-> 쿠키 헤더 적용으로 우회해서 진입)"""
    games = []
    base_url = "https://store.steampowered.com/search/?filter=topsellers&page="

    async with httpx.AsyncClient(timeout=20.0) as client:
        tasks = []

        for page in range(1, 5):
            url = f"{base_url}{page}"
            resp = await client.get(url, headers=STEAM_HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")
            game_elements = soup.select("a.search_result_row")

            for game in game_elements:
                title = game.select_one("span.title").text.strip()
                game_url = game["href"].split("?")[0]
                tasks.append(fetch_detail(client, title, game_url))

        results = await asyncio.gather(*tasks)

    return results


@mcp.tool()
def say_hello(name: str) -> str:
    # 테스트용
    return f"안녕하세요, {name}님!"


if __name__ == "__main__":
    mcp.run()
