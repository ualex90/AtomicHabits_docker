from rest_framework import serializers


class TimeToCompleteValidator:
    """ Проверка, что время выполнения не превышает максимальное время """

    def __init__(self, field, max_time=120):
        self.field = field
        self.max_time = max_time

    def __call__(self, value):
        if time_to_complete := value.get(self.field):
            if time_to_complete > self.max_time:
                raise serializers.ValidationError(f"Время выполнения задания не "
                                                  f"должно превышать {self.max_time} секунд")


class RelatedHabitOnlyNiceValidator:
    """ Проверка, что в связанных привычках указана только приятная привычка """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if habit_id := value.get(self.field):
            if not habit_id.is_nice:
                raise serializers.ValidationError(f'В поле "{self.field}" должна быть указана полезная привычка')
