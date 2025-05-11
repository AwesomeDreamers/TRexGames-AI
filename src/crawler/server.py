from mcp.server.fastmcp import FastMCP
import httpx
from bs4 import BeautifulSoup

mcp = FastMCP("WebCrawler")

@mcp.tool()
async def crawl_steam(keyword: str) -> str:
    """Steam에서 게임 검색 후 첫 번째 결과의 정보 반환"""
    query = keyword.replace(" ", "+")
    url = f"https://store.steampowered.com/search/?term={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        first_game = soup.select_one("a.search_result_row")
        if not first_game:
            return f"'{keyword}'에 대한 결과를 찾을 수 없습니다."

        title = first_game.select_one("span.title")
        price = first_game.select_one("div.search_price")
        link = first_game.get("href")

        title_text = title.text.strip() if title else "제목 없음"
        price_text = price.text.strip() if price else "가격 정보 없음"

        return f"[{title_text}]({link}) - {price_text}"


@mcp.tool()
def say_hello(name: str) -> str:
    return f"안녕하세요, {name}님!"

if __name__ == "__main__":
    mcp.run()
