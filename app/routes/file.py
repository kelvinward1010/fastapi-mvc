from fastapi import APIRouter, UploadFile, HTTPException, status, Response
from fastapi.responses import JSONResponse
from bson import ObjectId
from ..db import init_db
from ..schemas import entity

db = init_db.files_collection

router = APIRouter(
    prefix="/file",
    tags=["Files"],
)

@router.post("/upload-file")
async def upload_file(file: UploadFile):
    try:
        # Read data from the uploaded file
        image_data = await file.read()

        # Save the data to MongoDB
        result = db.insert_one({"filename": file.filename, "data": image_data})
        id = str(result.inserted_id)
        return JSONResponse(content={
            "status": 200,
            "message": "success",
            "url": f'https://fastapi-mvc.onrender.com/file/{id}'
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.get("/{id}")
async def get_photo(id: str):
    try:
        
        find_file = db.find_one({"_id": ObjectId(id)})
        if not find_file:
            return Response(content="File not found", status_code=404)

        return Response(content=find_file["data"], media_type="image/jpeg") #application/octet-stream
    except Exception as e:
        return Response(content=str(e), status_code=500)