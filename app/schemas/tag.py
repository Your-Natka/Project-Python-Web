from pydantic import BaseModel, constr, field_validator


class TagBase(BaseModel):
    name: constr(max_length=50)  # type: ignore # обмеження довжини рядка

    model_config = {
        "populate_by_name": True
    }


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: int
