1.TRexGames 크롤링 ai <br>
2.빌드<br>
-MCP기반<br>
-python --v : 3.13.3<br>
-ai: claude <br>
-docker<br>
3.크롤링 사이트: steam <br>
4.전체 아키텍처 흐름 <br>
[1] Python MCP 서버 (크롤링 + 전송)<br>
       ↓ (HTTP POST, 비동기)<br>
[2] Java Spring Boot REST API (수신 + 변환 + 저장)<br>
       ↓ (JPA)<br>
[3] Docker 내부 PostgreSQL 컨테이너 (데이터 저장소)<br><br>

개발 끝남
