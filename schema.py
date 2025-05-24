import pydantic
from errors import HttpError
from typing import Optional, Union, Type


class BaseAdv(pydantic.BaseModel):
    id: int
    header: str
    description: str
    user_id: int

    @pydantic.field_validator('description')
    @classmethod
    def description_correct(cls, v):
        if len(v) < 1:
            raise ValueError('incorrect description')
        return v


class CreateAdvertisement(BaseAdv):
    pass


class UpdateAdvertisement():
    header: str or None
    description: str or None


    @pydantic.field_validator('description')
    @classmethod
    def description_correct(cls, v):
        if len(v) < 1:
            raise ValueError('incorrect description')
        return v


def validate_json(
    json_data: dict,
    schema_cls: type[CreateAdvertisement] or type[UpdateAdvertisement]
):
    try:
        schema_object = schema_cls(**json_data)
        return schema_object.dict(exclude_unset=False) # статьи не уникальны по названию
    except pydantic.ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)




