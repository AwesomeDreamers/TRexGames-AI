from confluent_kafka import Producer
import json

conf = {
    'bootstrap.servers': 'localhost:9092'  # 도커 kafka:9093 / 로컬 localhost:9092
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'메시지 전송 실패: {err}')
    else:
        print(f'메시지 전송 성공: {msg.value().decode()} → 토픽: {msg.topic()}')

message = {'message': 'hello kafka!'}
producer.produce('steam-games', value=json.dumps(message), callback=delivery_report)

producer.flush()


