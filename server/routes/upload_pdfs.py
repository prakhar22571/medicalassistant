from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from typing import List
from modules.load_vectorstore import load_vectorstore
from modules.pdf_handlers import save_uploaded_files
from fastapi.responses import JSONResponse
from logger import logger


router=APIRouter()


def process_uploaded_files(file_paths: list[str]):
    try:
        load_vectorstore(file_paths)
        logger.info("Document added to vectorstore")
    except Exception:
        logger.exception("Error while processing uploaded PDFs")

@router.post("/upload_pdfs/")
async def upload_pdfs(background_tasks: BackgroundTasks, files:List[UploadFile] = File(...)):
    try:
        logger.info("Recieved uploaded files")
        file_paths = save_uploaded_files(files)
        background_tasks.add_task(process_uploaded_files, file_paths)
        logger.info("Document processing scheduled for vectorstore update")
        return {"messages":"Files received and processing started"}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500,content={"error":str(e)})