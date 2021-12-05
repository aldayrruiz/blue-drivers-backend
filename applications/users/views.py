import logging

from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from applications.tenant.models import Tenant
from applications.users.models import RecoverPassword, RecoverPasswordStatus
from applications.users.serializers.create import RegistrationSerializer, FakeRegistrationSerializer
from applications.users.serializers.simple import SimpleUserSerializer
from applications.users.serializers.special import UpdateUserSerializer, SingleUserSerializer, \
    PartialUpdateUserSerializer, CreateRecoverPasswordSerializer, ConfirmRecoverPasswordSerializer, \
    RecoverPasswordSerializer
from applications.users.services.creator import create_fake_admin
from applications.users.services.queryset import get_user_queryset
from shared.permissions import IsAdmin, IsNotDisabled
from utils.api.query import query_bool
from utils.codegen import generate_password
from utils.email.users import send_create_recover_password, send_confirmed_recovered_password

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    """
    This entire endpoint class and its methods (endpoints) are only available if requester is admin.
    """

    def list(self, request):
        """
        It returns all users.
        """
        requester = self.request.user
        even_disabled = query_bool(self.request, 'evenDisabled')
        logger.info('List users request received. [evenDisabled: {}]'.format(even_disabled))
        queryset = get_user_queryset(requester.tenant, even_disabled=even_disabled)
        serializer = SimpleUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        It returns the user given an id.
        """
        requester = self.request.user
        logger.info('Retrieve user request received.')
        queryset = get_user_queryset(requester.tenant, even_disabled=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = SingleUserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        It disables an user.
        If requester tries to delete himself, server respond with 403 ERROR.
        """
        logger.info('Destroy user request received.')
        requester = self.request.user
        queryset = get_user_queryset(requester.tenant, even_disabled=True)
        user = get_object_or_404(queryset, pk=pk)
        if requester == user:
            logger.warning("User couldn't delete himself.")
            return Response(status=HTTP_403_FORBIDDEN)
        user.delete()
        logger.info('User was disabled.')
        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """
        It update the data of a user.
        """
        logger.info('Update user request received.')
        requester = self.request.user
        queryset = get_user_queryset(requester.tenant, even_disabled=True)

        user = get_object_or_404(queryset, pk=pk)
        serializer = UpdateUserSerializer(user, self.request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User was updated successfully.')
            return Response(serializer.data)
        log_error_serializing(serializer)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        It is used just for disable and enable users. Just admins can do this.
        """
        logger.info('Partial update user request received.')
        requester = self.request.user
        queryset = get_user_queryset(requester.tenant, even_disabled=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = PartialUpdateUserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('User was partial updated successfully.')
            return Response(serializer.data)
        log_error_serializing(serializer)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_recover_password(self, request):
        serializer = CreateRecoverPasswordSerializer(data=self.request.data)
        if not serializer.is_valid():
            log_error_serializing(serializer)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        recover_password = serializer.save()
        send_create_recover_password(recover_password.owner, recover_password.code)
        serialized = RecoverPasswordSerializer(recover_password)
        return Response(serialized.data)

    @action(detail=True, methods=['put'])
    def confirm_recover_password(self, request, pk=None):
        serializer = ConfirmRecoverPasswordSerializer(data=self.request.data)
        queryset = RecoverPassword.objects.all()
        recover_password = get_object_or_404(queryset, pk=pk)

        if not serializer.is_valid():
            log_error_serializing(serializer)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        code_not_match = recover_password.code.upper() != serializer.validated_data['code'].upper()
        already_completed = recover_password.status == RecoverPasswordStatus.COMPLETED

        if code_not_match or already_completed:
            return Response(status=HTTP_400_BAD_REQUEST)

        recover_password.status = RecoverPasswordStatus.COMPLETED
        owner = recover_password.owner
        new_password = generate_password()
        owner.set_password(new_password)

        owner.save()
        recover_password.save()

        send_confirmed_recovered_password(recover_password.owner, new_password)
        return Response()

    # Create method is located in /register endpoint
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update']:
            permission_classes = [permissions.IsAuthenticated, IsNotDisabled]
        elif self.action in ['create', 'destroy', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class RegistrationViewSet(viewsets.ViewSet):

    def create(self, request):
        logger.info('Register user request received.')
        requester = self.request.user
        serializer = RegistrationSerializer(data=self.request.data)

        if not serializer.is_valid():
            log_error_serializing(serializer)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = serializer.save(tenant=requester.tenant)
        logger.info('User registered successfully: {}'.format(user.fullname))
        return Response(serializer.data)

    @action(detail=False, methods=['post'], name='Fake')
    def create_fake(self, request):
        logger.info('Register a fake user received.')
        tenant, created = Tenant.objects.get_or_create(name='Fake')
        # If you forgot to create Fake Tenant -> Create fake admin to not crash.
        if created:
            create_fake_admin(tenant.id)
        serializer = FakeRegistrationSerializer(data=self.request.data)

        if not serializer.is_valid():
            log_error_serializing(serializer)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        user = serializer.save(tenant=tenant)
        logger.info('Fake user registered successfully: {}'.format(user.fullname))

        # Set all vehicles from tenant to new user.
        vehicles = tenant.vehicles.all()
        user.allowed_vehicles.set(vehicles)

        return Response(serializer.data)

    def get_permissions(self):
        if self.name == 'Fake':
            return [permission() for permission in []]
        else:
            # Only admin can register users.
            return [permission() for permission in [permissions.IsAuthenticated, IsAdmin]]


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        logger.info('Login user request received.')
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.is_disabled:
            logger.info('User is disabled -> Cannot login')
            return Response({'errors': 'Usuario deshabilitado, contactar con el administrador'}, HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=user)
        if created:
            logger.debug('Token was created.')
        if token.key:
            logger.info('Login was successfully.')
        else:
            logger.warning('Login of user {} failed.', user.fullname)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'fullname': user.fullname,
            'role': user.role,
            'tenant': user.tenant.id
        })


def log_error_serializing(serializer):
    logger.error("User couldn't be serialized with {} because of {}."
                 .format(serializer.__class__.__name__, serializer.errors))
