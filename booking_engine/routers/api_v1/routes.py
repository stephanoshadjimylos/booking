import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

from booking_engine.routers.api_v1.models import ClassGetAvailability
from booking_engine.utility.reservation_calculator import get_room_availability


app = FastAPI()
app.mount("/imgs", StaticFiles(directory="booking_engine/photos"), name="images")
templates = Jinja2Templates(directory="booking_engine/routers/api_v1/templates")


def initiate_app():
    uvicorn.run(
        "booking_engine.routers.api_v1.routes:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


@app.get("/")
def home(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("landing_page.html", context)


@app.post("/get_availability")
async def get_availability(payload: ClassGetAvailability, request: Request):
    try:
        availability = get_room_availability(
            check_in=payload.check_in,
            nights=payload.nights,
            adults=payload.adults,
            children=payload.children,
            infants=payload.infants,
        )
        if not availability:
            return templates.TemplateResponse(
                "no_results_found.html", {"request": request}
            )
        # Render the HTML template with the availability data
        return templates.TemplateResponse(
            "availability.html", {"request": request, "rooms": availability}
        )
    except Exception as e:
        logging.error(f"Get availability endpoint failed. Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error. Exception: {e}",
        )
