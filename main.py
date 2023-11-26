from typing import Annotated
from creategif import CreateAsciiArt

from fastapi import FastAPI, File, Request, status

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# origins = [
#     "http://localhost/*",
#     "http://localhost:8000/*",
#     "https://web-ascii-arter-kbfh8ecjtpnc.deno.dev",
#     "https://web-ascii-arter.deno.dev",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.post("/files/")
async def create_files(files: Annotated[bytes, File()]):
    # ↓画像を加工して、base64文字列に保存
    output = CreateAsciiArt().create_ascii_art_from_binary(files)
    return {"base64": output}
