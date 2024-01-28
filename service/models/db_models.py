from tortoise.models import Model as TModel
from tortoise import fields


class Manufacturer(TModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    class Meta:
        table = "manufacturers"

    class PydanticMeta:
        exclude = ("id", "models")

    def __str__(self):
        return f"Manufacturer(id={self.id},name={self.name})"


class Category(TModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    class Meta:
        table = "categories"

    class PydanticMeta:
        exclude = ("id", "parts",)

    def __str__(self):
        return f"Category(id={self.id},name={self.name})"


class Model(TModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    manufacturer = fields.ForeignKeyField('models.Manufacturer', related_name="models")

    class Meta:
        table = "models"

    class PydanticMeta:
        exclude = ("parts",)

    def __str__(self):
        return f"Model(id={self.id},name={self.name},manufacturer={self.manufacturer})"


class Part(TModel):
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=50)
    spec = fields.CharField(max_length=200)
    models = fields.ManyToManyField('models.Model', through='parts_models', related_name="parts",
                                    forward_key="model_id", backward_key="part_id")
    categories = fields.ManyToManyField('models.Category', through='parts_categories', related_name="parts",
                                        forward_key="category_id", backward_key="part_id")

    class Meta:
        table = "parts"

    class PydanticMeta:
        exclude = ("models", "categories",)

    def __str__(self):
        return (f"Part(id={self.id},number={self.number},spec={self.spec},"
                f"models={self.models},categories={self.categories})")

