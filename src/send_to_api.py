import asyncio
from confluent_kafka import Producer
import json
from crawler import get_top_100_games_async  # 크롤링 함수
import time

# Kafka 설정
conf = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"전송 실패: {err}")
    else:
        print(f"전송 성공: {msg.value().decode()} → 토픽: {msg.topic()}")

async def send_games_to_kafka():
    print("----크롤링 시작----")
    games = await get_top_100_games_async()

    success = 0

    for game in games:
        try:
            # JSON 직렬화
            producer.produce(
                topic='steam-games',
                value=json.dumps(game),
                callback=delivery_report
            )
            success += 1
        except Exception as e:
            print(f"예외 발생: {game.get('title', '[no title]')} → {e}")

    # 모든 메시지가 전송될 때까지 대기
    producer.flush()
    print(f"카프카로 전송 완료: {success}/{len(games)}개")

async def batch_loop(interval_seconds=86400):
    """배치 24시간 마다 실행 """
    while True:
        await send_games_to_kafka()
        await asyncio.sleep(interval_seconds)

# 실행
if __name__ == "__main__":
    asyncio.run(batch_loop(interval_seconds=86400))
