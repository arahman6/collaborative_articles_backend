from mangum import Mangum
from app.main import app

class CustomMangum(Mangum):
    def __call__(self, event, context):
        print("Event")
        print(event)

        print("Context")
        print(context)
        # Ensure requestContext exists and has http key
        if "requestContext" in event and "http" in event["requestContext"]:
            if "sourceIp" not in event["requestContext"]["http"]:
                event["requestContext"]["http"]["sourceIp"] = "0.0.0.0"
        return super().__call__(event, context)
    

lambda_handler = CustomMangum(app)

