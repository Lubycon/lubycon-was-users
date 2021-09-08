
import os
import requests
import warnings

import uvicorn

from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Lubycon-WAS-users", description="루비콘 사용자들 정보를 조회할 수 있는 백엔드 서비스입니다")

url = "https://raw.githubusercontent.com/ssaru/Lubycon-users/"
token = os.environ.get("GITHUB_TOKEN", "")


class Response(BaseModel):
    users_info: str


@app.get("/users_info/{tag}/")
async def get_users_info(tag: str = "v0.1.0") -> Response:
    """
    특정 버전(tag)의 사용자 정보를 반환한다.

    - **tag**: [Lubycon-users](https://github.com/ssaru/Lubycon-users)의 특정 tag버전(ex. v0.1.0)
    """
    uri = "".join([url, tag, "/users.json?token=", token])
    req = requests.get(uri)
    
    if req.ok:
        users_info = req.text
        response = Response(users_info=users_info)
        return response
    else:
        raise HTTPException(status_code=400, detail=f"Failed to get user information. See response message-> {req.text}")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    uvicorn.run(app, host="0.0.0.0", port=8000)
