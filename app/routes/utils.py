from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/chart/{chart_id}")
async def get_chart_image(chart_id: str):
    chart_path = f"app/static/images/{chart_id}.png"
    if os.path.exists(chart_path):
        return FileResponse(chart_path)
    else:
        raise HTTPException(status_code=404, detail="图表未找到")