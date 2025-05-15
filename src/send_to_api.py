import asyncio
import requests
from crawler import get_top_100_games_async  # 기존 크롤링 함수 재사용

async def send_games_to_api():
    print("크롤링 시작...")
    games = await get_top_100_games_async()

    api_url = "http://localhost:8090/api/steam/games"
    success = 0

    for game in games:
        try:
            res = requests.post(api_url, json=game)
            if res.status_code == 200:
                print(f"{game['title']} 저장됨")
                success += 1
            else:
                print(f"{game['title']} 실패: {res.status_code}")
        except Exception as e:
            print(f"예외: {game['title']} → {e}")

    print(f"총 {success}/{len(games)} 개 저장 완료")

# 실행
if __name__ == "__main__":
    asyncio.run(send_games_to_api())
