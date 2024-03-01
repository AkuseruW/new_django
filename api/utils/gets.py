from django.db.models import Q

from api.models import Conversation, Match

def get_match(p1, p2):
    match = Match.objects.filter(
        Q(profile1=p1, profile2=p2) | Q(profile1=p2, profile2=p1)
    )

    if match.exists():
        return match.first()

    return None


def get_conversation_between(p1, p2):
    conversation = Conversation.objects.filter(participants=p1).filter(
        participants=p2
    )
    if conversation.exists():
        return conversation.first()
    else:
        return None