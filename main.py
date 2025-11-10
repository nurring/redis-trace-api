from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD', None),
    decode_responses=True
)

class StatusRequest(BaseModel):
    key: str

class PutSampleRequest(BaseModel):
    key: str
    value: str

@app.post("/status")
async def status(request: StatusRequest):
    try:
        # First Redis lookup
        first_result = redis_client.get(request.key)

        if first_result is None:
            return {"error": "Key not found", "key": request.key}

        first_data = json.loads(first_result)

        # Extract block_id from first result
        if "block" not in first_data:
            raise HTTPException(status_code=500, detail="Block ID not found in first lookup")

        block_id = first_data["block"]

        # Second Redis lookup with block:block_id key
        second_key = f"{request.key}:block:{block_id}"
        second_result = redis_client.get(second_key)

        if second_result is None:
            raise HTTPException(status_code=404, detail=f"Block data not found for key: {second_key}")

        final_data = json.loads(second_result)

        # Add block_id to the final response
        final_data["block"] = block_id

        return final_data

    except redis.RedisError:
        raise HTTPException(status_code=500, detail="Redis connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/putsample")
async def put_sample(request: PutSampleRequest):
    try:
        import time
        current_timestamp = int(time.time())

        # Parse JSON value and add timestamp
        value_data = json.loads(request.value)
        value_data["timestamp"] = current_timestamp
        final_value = json.dumps(value_data)

        redis_client.set(request.key, final_value)
        return {"message": f"Set {request.key} = {final_value}"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in value")
    except redis.RedisError:
        raise HTTPException(status_code=500, detail="Redis connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)