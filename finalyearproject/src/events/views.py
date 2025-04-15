from rest_framework import viewsets
from .models import Due, Event
from .serializers import DueSerializer, EventSerializer
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def upcoming_events(self, request):
        """
        Returns a list of upcoming events.
        """
        upcoming_events = Event.objects.filter(event_date__gte=now().date())
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

class DueViewSet(viewsets.ModelViewSet):
    queryset = Due.objects.all()
    serializer_class = DueSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['post'])
    def copy_expired_members(self, request):
        """
        Copies members whose membership has expired to the Due table.
        """
        from .models import Members  # Import Members model here to avoid circular imports

        expired_members = Members.objects.filter(membership_end_date__lt=now().date())

        copied_count = 0
        for member in expired_members:
            if not Due.objects.filter(member_id=member.member_id).exists():
                Due.objects.create(
                    member_id=member.member_id,
                    name=member.name,
                    email=member.email,
                    phone_number=member.phone_number,
                    address=member.address,
                    date_of_birth=member.date_of_birth,
                    membership_start_date=member.membership_start_date,
                    membership_end_date=member.membership_end_date,
                    membership_type_id=member.membership_type.membership_type_id
                )
                copied_count += 1

        return Response({"message": f"{copied_count} members copied to Due table."})

    @action(detail=True, methods=['delete'])
    def delete_member_and_due(self, request, pk=None):
        """
        Deletes a member and their due record based on member ID.
        """
        try:
            member_id = int(pk)
            Due.objects.filter(member_id=member_id).delete()
            from .models import Members
            Members.objects.filter(member_id=member_id).delete()
            return Response({"message": "Member and their due record deleted successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
