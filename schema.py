import pydantic
from errors import HttpError
from typing import Optional, Union, Type


class BaseAdv(pydantic.BaseModel):
    header: str
    description: str

    @pydantic.field_validator('description')
    @classmethod
    def description_correct(cls, v):
        if len(v) < 1:
            raise ValueError('incorrect description')
        return v


class CreateAdvertisement(BaseAdv):
    pass


class UpdateAdvertisement(BaseAdv):
    header: Optional[str] = None
    description: Optional[str] = None


def validate_json(
    json_data: dict,
    schema_cls: Type[Union[CreateAdvertisement, UpdateAdvertisement]]
):
    try:
        schema_object = schema_cls(**json_data)
        return schema_object.dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)




