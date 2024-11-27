from rest_framework.serializers import ModelSerializer


def model_serializer_factory(model, fields='__all__', depth=1):
    cls_name = f"{model.__name__}Serializer"
    return type(
        cls_name,
        (ModelSerializer,),
        {"Meta": type("Meta", (), {"model": model, "fields": fields, "depth": depth})},
    )