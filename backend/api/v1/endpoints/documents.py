from fastapi import APIRouter, Depends, File, UploadFile, responses
from util.dependencies import get_current_user
from util.document import save_user_document, insert_document
import uuid

documents_router = APIRouter()


@documents_router.post("/user")
async def upload_user_document(
    current_user: dict = Depends(get_current_user),
    document: UploadFile = File(...),
) -> dict:
    user_id = current_user.get("sub")
    document_id = str(uuid.uuid4())
    document_content = document.file.read()
    save_user_document(user_id, document_id, document_content)
    insert_document(user_id, document_id)
    return responses.JSONResponse(
        content={"message": "Document uploaded successfully"}, status_code=200
    )
