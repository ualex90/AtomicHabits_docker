from rest_framework import serializers


class FillingNotOutTwoFieldsValidator:
    """ Валидатор проверят, что одновременно не заполнены 2 поля """

    def __init__(self, first_field, second_field, message=None):
        self.message = message
        self.first_field = first_field
        self.second_field = second_field

    def __call__(self, value):
        if value.get(self.first_field) and value.get(self.second_field):
            if not self.message:
                self.message = f'Недопустимо одновременно указывать "{self.first_field}" и "{self.second_field}"'
            raise serializers.ValidationError(self.message)


class FieldsIsNoneValidator:
    """ Валидатор проверят, что указанные поля не заполнены """

    def __init__(self, *args, message=None):
        self.message = message
        self.fields = args

    def __call__(self, value):
        for field in self.fields:
            if value.get(field):
                if not self.message:
                    self.message = f'Запрещено заполнять поле "{field}""'
                raise serializers.ValidationError(self.message)
