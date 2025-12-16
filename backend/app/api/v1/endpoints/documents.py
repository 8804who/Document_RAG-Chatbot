import uuid

from fastapi import APIRouter, Depends, File, Path, UploadFile
from fastapi.responses import JSONResponse

from app.util.dependencies import get_current_user
from app.util.document import (
    delete_document_from_vector_store,
    get_user_documents_from_vector_store,
    insert_document_to_vector_store,
    save_user_document_to_file,
)
from app.util.logger import logger

documents_router = APIRouter()


@documents_router.post("/user")
async def upload_user_document(
    current_user: dict = Depends(get_current_user),
    document: UploadFile = File(...),
) -> JSONResponse:
    logger.info(f"Uploading user document: {document.filename}")
    user_id = current_user.get("sub")
    document_id = str(uuid.uuid4())
    document_content = document.file.read().decode("utf-8")
    save_user_document_to_file(user_id, document_id, document_content)
    insert_document_to_vector_store(user_id, document_id, document.filename)
    return JSONResponse(
        content={"message": "Document uploaded successfully"}, status_code=200
    )


@documents_router.get("/user")
async def get_user_documents(
    current_user: dict = Depends(get_current_user),
) -> JSONResponse:
    logger.info("Getting user documents")
    user_id = current_user.get("sub")
    documents = get_user_documents_from_vector_store(user_id)
    return JSONResponse(content={"documents": documents}, status_code=200)


@documents_router.delete("/{document_id}")
async def delete_user_document(
    current_user: dict = Depends(get_current_user),
    document_id: str = Path(...),
) -> JSONResponse:
    logger.info(f"Deleting user document: {document_id}")
    delete_document_from_vector_store(document_id)
    return JSONResponse(
        content={"message": "Document deleted successfully"}, status_code=200
    )
