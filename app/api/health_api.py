from fastapi import APIRouter

router = APIRouter()

@router.get("") #The `@router` decorator in FastAPI is used to include external routers, or a set of routes, into the main application. Mainly used for seperation of concerns to group related api routes together and can be used in the main file
def health_check():
    return {"status": "healthy"}