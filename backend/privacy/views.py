from core.views import BaseModelViewSet as AbstractBaseModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from .models import (
    Purpose,
    PersonalData,
    DataSubject,
    DataRecipient,
    DataContractor,
    DataTransfer,
    Processing,
)


class BaseModelViewSet(AbstractBaseModelViewSet):
    serializers_module = "privacy.serializers"


class PurposeViewSet(BaseModelViewSet):
    """
    API endpoint that allows purposes to be viewed or edited.
    """

    model = Purpose


class PersonalDataViewSet(BaseModelViewSet):
    """
    API endpoint that allows personal data to be viewed or edited.
    """

    model = PersonalData

    @action(detail=False, name="Get deletion policy choices")
    def deletion_policy(self, request):
        return Response(dict(PersonalData.DELETION_POLICY_CHOICES))


class DataSubjectViewSet(BaseModelViewSet):
    """
    API endpoint that allows data subjects to be viewed or edited.
    """

    model = DataSubject


class DataRecipientViewSet(BaseModelViewSet):
    """
    API endpoint that allows data recipients to be viewed or edited.
    """

    model = DataRecipient


class DataContractorViewSet(BaseModelViewSet):
    """
    API endpoint that allows data contractors to be viewed or edited.
    """

    model = DataContractor


class DataTransferViewSet(BaseModelViewSet):
    """
    API endpoint that allows data transfers to be viewed or edited.
    """

    model = DataTransfer


class ProcessingViewSet(BaseModelViewSet):
    """
    API endpoint that allows processing activities to be viewed or edited.
    """

    model = Processing
