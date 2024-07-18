from django.shortcuts import render

# Create your views here.
import base64
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

url_base = 'https://gateway.apiserpro.serpro.gov.br'
consumer_key = 'LeFh2XRQz6apNStquQLN5e84K10a'
consumer_secret = 'IWxAzfBc4xcKZxjDlrEMHnDZoVga'

def pegar_token():
    url_token = f'{url_base}/token'
    credenciais = f"{consumer_key}:{consumer_secret}"
    codificar = base64.b64encode(credenciais.encode('utf-8')).decode('utf-8')
    headers = {
        "Authorization": f"Basic {codificar}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    dado = {"grant_type": "client_credentials"}
    response = requests.post(url_token, headers=headers, data=dado)
    if response.status_code == 200:
        response_dado = response.json()
        return response_dado.get("access_token")
    else:
        return None

def consultar_divida(numero_inscricao, servico, token):
    url = f"{url_base}/consulta-divida-ativa-df/api/v1/{servico}/{numero_inscricao}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code in [401, 403]:
        token = pegar_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
            response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

class ConsultaDividaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        numero_inscricao = data.get('numero_inscricao')
        servico = data.get('servico')
        token = pegar_token()
        if not token:
            return Response({"error": "Failed to retrieve token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        resultado = consultar_divida(numero_inscricao, servico, token)
        return Response(resultado)
