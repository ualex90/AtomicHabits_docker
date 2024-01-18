from rest_framework import serializers

from app_habits.models import Habit
from validators.general_validators import FillingNotOutTwoFieldsValidator
from app_habits.validators.habit import (
    TimeToCompleteValidator,
    RelatedHabitOnlyNiceValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitNiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        exclude = ('start_time', 'periodicity', 'related_habit', 'reward')
        read_only_fields = ('owner', 'is_nice')
        validators = [
            # Проверяем что время выполнения не превышает 120 секунд
            TimeToCompleteValidator('time_to_complete'),
        ]


class HabitGoodCreateSerializer(serializers.ModelSerializer):
    # Для полезной привычки, поле start_time является обязательным
    start_time = serializers.TimeField()

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('owner', 'is_nice')
        validators = [
            # Проверяем что одновременно не указаны связанная привычка и вознаграждение
            FillingNotOutTwoFieldsValidator('related_habit', 'reward'),
            # Проверяем что время выполнения не превышает 120 секунд
            TimeToCompleteValidator('time_to_complete'),
            # Проверяем что в связанных привычках, привычка с признаком приятной
            RelatedHabitOnlyNiceValidator('related_habit'),
        ]


class HabitGoodUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('owner', 'is_nice')
        validators = [
            # Проверяем что одновременно не указаны связанная привычка и вознаграждение
            FillingNotOutTwoFieldsValidator('related_habit', 'reward'),
            # Проверяем что время выполнения не превышает 120 секунд
            TimeToCompleteValidator('time_to_complete'),
            # Проверяем что в связанных привычках, привычка с признаком приятной
            RelatedHabitOnlyNiceValidator('related_habit'),
        ]

    def update(self, instance, validated_data):
        """
        При обновлении обеспечивается наличия значения
        только в одном из полей related_habit или reward.
        Сохраняется то поле, которое ввел пользователь при обновлении
        """

        if validated_data.get("related_habit") and instance.reward:
            # Сброс поля reward в None если пользователь ввел related_habit
            validated_data['reward'] = None
        elif validated_data.get("reward") and instance.related_habit:
            # Сброс поля related_habit в None если пользователь ввел reward
            validated_data['related_habit'] = None
        instance = super().update(instance, validated_data)
        return instance


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice')


class HabitListAllSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()

    @staticmethod
    def get_owner_email(instance):
        owner_email = instance.owner.email
        return owner_email

    class Meta:
        model = Habit
        fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
