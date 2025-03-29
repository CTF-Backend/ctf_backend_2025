from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from asgiref.sync import sync_to_async

from staff.models import Notification
from staff.serializers import NotificationSerializer

from contestant.models import Team
from contestant.serializers import TeamSerializer


class NotificationConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permissions = (permissions.IsAuthenticated,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Notification)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=NotificationSerializer(instance).data, action=action.value)


class TeamConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Team.objects.all().order_by("-score")  # Sorted leaderboard
    serializer_class = TeamSerializer
    permissions = (permissions.IsAuthenticated,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    async def receive_json(self, content, **kwargs):
        action = content.get("action")
        if action == "list":
            await self.send_team_list()

    async def send_team_list(self):
        teams = await sync_to_async(list)(self.get_queryset())
        serialized_data = TeamSerializer(teams, many=True).data
        await self.send_json({"teams": serialized_data})

    @model_observer(Team)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_team_list()

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=TeamSerializer(instance).data, action=action.value)
