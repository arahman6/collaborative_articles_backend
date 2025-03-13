from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core.core_schema import CoreSchema, str_schema

class PyObjectId(ObjectId):
    """Custom Pydantic type for MongoDB ObjectId."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type[ObjectId], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Returns Pydantic core schema, treating ObjectId as a string."""
        return str_schema()

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetCoreSchemaHandler
    ) -> JsonSchemaValue:
        """Ensures OpenAPI schema recognizes ObjectId as a string."""
        return {"type": "string"}

    @classmethod
    def validate(cls, v):
        """Validates if the given value is a valid ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_validators__(cls):
        """Yields the validator function for Pydantic."""
        yield cls.validate
