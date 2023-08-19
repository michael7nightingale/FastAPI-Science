from .models import History
from ..users.models import User


async def delete_history(user: User):
    for h in await History.filter(user__id=user.id):
        await h.delete()
