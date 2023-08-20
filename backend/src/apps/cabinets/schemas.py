from pydantic import BaseModel


class DownloadFile(BaseModel):
    filename: str
    extension: str
