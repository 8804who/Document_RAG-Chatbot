from fastapi import APIRouter, Depends, File, UploadFile, responses
from util.dependencies import get_current_user
from util.document import (
    save_user_document_to_file,
    insert_document_to_vector_store,
    get_user_documents_from_vector_store,
)
import uuid

documents_router = APIRouter()


@documents_router.post("/user")
async def upload_user_document(
    current_user: dict = Depends(get_current_user),
    document: UploadFile = File(...),
) -> dict:
    user_id = current_user.get("sub")
    document_id = str(uuid.uuid4())
    document_content = document.file.read().decode("utf-8")
    save_user_document_to_file(user_id, document_id, document_content)
    insert_document_to_vector_store(user_id, document_id, document.filename)
    return responses.JSONResponse(
        content={"message": "Document uploaded successfully"}, status_code=200
    )


@documents_router.get("/user")
async def get_user_documents(
    current_user: dict = Depends(get_current_user),
) -> dict:
    user_id = current_user.get("sub")
    documents = get_user_documents_from_vector_store(user_id)
    return responses.JSONResponse(content={"documents": documents}, status_code=200)
