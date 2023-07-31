from rest_framework.permissions import BasePermission
from botocore.exceptions import NoCredentialsError
from botocore.session import Session


class ValidCognitoTokenPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            # Obtén el token de la solicitud
            print(f"ValidCognito_request: {request}")
            token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]
            print(f"ValidCognito_token: {token}")
            # Verifica la validez del token utilizando el servicio de Cognito
            session = Session()
            session._credentials = (
                None  # Evita el uso de las credenciales predeterminadas
            )
            session.set_credentials(token=token)
            session.get_credentials().get_frozen_credentials()
            return True  # El token es válido
        except NoCredentialsError:
            return False  # El token es inválido o no se proporcionó
