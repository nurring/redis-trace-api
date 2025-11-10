# Redis Proxy API

FastAPI 기반의 Redis 프록시 API 서버입니다.

## 기능

- `/status` - Redis에서 키를 조회하고 블록 데이터를 반환
- `/putsample` - 타임스탬프를 추가하여 Redis에 데이터 저장

## 요구사항

- Python 3.11+
- Redis 서버

## 설치

### 로컬 환경

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### Docker

```bash
docker build -t redis-proxy .
```

## 환경변수 설정

`.env.example` 파일을 `.env`로 복사하고 환경변수를 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:

```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password_here
```

**참고**: Redis 서버에 비밀번호가 설정되지 않은 경우 `REDIS_PASSWORD`는 생략하거나 비워둘 수 있습니다.

## 실행

### 로컬 실행

```bash
python main.py
```

서버는 `http://localhost:8000`에서 실행됩니다.

### Docker 실행

```bash
docker run -p 8000:8000 --env-file .env redis-proxy
```

## API 엔드포인트

### POST /status

Redis에서 키를 조회하고 블록 데이터를 가져옵니다.

**Request Body:**
```json
{
  "key": "your-key"
}
```

**Response:**
```json
{
  "block": "block_id",
  ...
}
```

### POST /putsample

타임스탬프를 추가하여 Redis에 데이터를 저장합니다.

**Request Body:**
```json
{
  "key": "your-key",
  "value": "{\"data\": \"value\"}"
}
```

**Response:**
```json
{
  "message": "Set your-key = {\"data\":\"value\",\"timestamp\":1234567890}"
}
```

## API 문서

서버 실행 후 다음 주소에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
