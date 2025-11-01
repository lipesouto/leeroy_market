"""
Integração com SeAT API
Sistema de comunicação com a API do SeAT para obter dados corporativos
"""

import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class SeATAPIError(Exception):
    """Exceção customizada para erros da API SeAT"""
    pass


class SeATAPI:
    """
    Cliente para comunicação com a API do SeAT
    
    Documentação da API: https://eveseat.github.io/docs/developer_guides/api/
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'SEAT_API_URL', None)
        self.token = getattr(settings, 'SEAT_API_TOKEN', None)
        self.corporation_id = getattr(settings, 'SEAT_CORPORATION_ID', None)
        
        if not all([self.base_url, self.token]):
            logger.warning("SeAT API não configurada. Configure SEAT_API_URL e SEAT_API_TOKEN.")
        
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Timeout padrão para requisições
        self.timeout = 10
        
        # Cache TTL (Time To Live) em segundos
        self.cache_ttl = 300  # 5 minutos
    
    def _make_request(self, method, endpoint, **kwargs):
        """
        Faz requisição à API do SeAT com tratamento de erros
        
        Args:
            method: Método HTTP (GET, POST, etc)
            endpoint: Endpoint da API (ex: '/corporation/123/wallet')
            **kwargs: Argumentos adicionais para requests
        
        Returns:
            dict: Resposta JSON da API
        
        Raises:
            SeATAPIError: Se houver erro na requisição
        """
        if not self.base_url or not self.token:
            raise SeATAPIError("SeAT API não configurada")
        
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao acessar SeAT API: {url}")
            raise SeATAPIError("Timeout ao conectar com SeAT")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Erro de conexão com SeAT API: {url}")
            raise SeATAPIError("Não foi possível conectar ao SeAT")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP da SeAT API: {e.response.status_code} - {url}")
            raise SeATAPIError(f"Erro HTTP: {e.response.status_code}")
        
        except Exception as e:
            logger.error(f"Erro inesperado ao acessar SeAT API: {str(e)}")
            raise SeATAPIError(f"Erro inesperado: {str(e)}")
    
    def _get_cached(self, cache_key, fetch_function, *args, **kwargs):
        """
        Busca dado do cache ou executa função se não estiver em cache
        
        Args:
            cache_key: Chave do cache
            fetch_function: Função para buscar dados se não estiver em cache
            *args, **kwargs: Argumentos para fetch_function
        
        Returns:
            Dados do cache ou resultado de fetch_function
        """
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.debug(f"Cache hit: {cache_key}")
            return cached_data
        
        logger.debug(f"Cache miss: {cache_key}")
        data = fetch_function(*args, **kwargs)
        cache.set(cache_key, data, self.cache_ttl)
        return data
    
    # ========== CORPORATION ENDPOINTS ==========
    
    def get_corporation_wallet(self, corporation_id=None):
        """
        Busca saldo da wallet da corporação
        
        Args:
            corporation_id: ID da corporação (usa default se não especificado)
        
        Returns:
            list: Lista de divisões da wallet com saldos
            
        Exemplo:
            [{"division": 1, "balance": 1234567.89}]
        """
        corp_id = corporation_id or self.corporation_id
        if not corp_id:
            raise SeATAPIError("Corporation ID não configurado")
        
        cache_key = f"seat_corp_{corp_id}_wallet"
        
        def fetch():
            endpoint = f"/corporation/{corp_id}/wallet"
            response = self._make_request('GET', endpoint)
            return response.get('data', [])
        
        return self._get_cached(cache_key, fetch)
    
    def get_corporation_assets(self, corporation_id=None):
        """
        Busca assets da corporação
        
        Returns:
            list: Lista de assets
        """
        corp_id = corporation_id or self.corporation_id
        if not corp_id:
            raise SeATAPIError("Corporation ID não configurado")
        
        cache_key = f"seat_corp_{corp_id}_assets"
        
        def fetch():
            endpoint = f"/corporation/{corp_id}/assets"
            response = self._make_request('GET', endpoint)
            return response.get('data', [])
        
        return self._get_cached(cache_key, fetch)
    
    def get_corporation_members(self, corporation_id=None):
        """
        Busca membros da corporação
        
        Returns:
            list: Lista de membros
        """
        corp_id = corporation_id or self.corporation_id
        if not corp_id:
            raise SeATAPIError("Corporation ID não configurado")
        
        cache_key = f"seat_corp_{corp_id}_members"
        
        def fetch():
            endpoint = f"/corporation/{corp_id}/members"
            response = self._make_request('GET', endpoint)
            return response.get('data', [])
        
        return self._get_cached(cache_key, fetch)
    
    def get_corporation_structures(self, corporation_id=None):
        """
        Busca estruturas da corporação
        
        Returns:
            list: Lista de estruturas
        """
        corp_id = corporation_id or self.corporation_id
        if not corp_id:
            raise SeATAPIError("Corporation ID não configurado")
        
        cache_key = f"seat_corp_{corp_id}_structures"
        
        def fetch():
            endpoint = f"/corporation/{corp_id}/structures"
            response = self._make_request('GET', endpoint)
            return response.get('data', [])
        
        return self._get_cached(cache_key, fetch)
    
    # ========== CHARACTER ENDPOINTS ==========
    
    def get_character_wallet(self, character_id):
        """
        Busca saldo da wallet de um personagem
        
        Args:
            character_id: ID do personagem
        
        Returns:
            dict: Dados da wallet
        """
        cache_key = f"seat_char_{character_id}_wallet"
        
        def fetch():
            endpoint = f"/character/{character_id}/wallet"
            response = self._make_request('GET', endpoint)
            return response.get('data', {})
        
        return self._get_cached(cache_key, fetch)
    
    def get_character_skills(self, character_id):
        """
        Busca skills de um personagem
        
        Args:
            character_id: ID do personagem
        
        Returns:
            list: Lista de skills
        """
        cache_key = f"seat_char_{character_id}_skills"
        
        def fetch():
            endpoint = f"/character/{character_id}/skills"
            response = self._make_request('GET', endpoint)
            return response.get('data', [])
        
        return self._get_cached(cache_key, fetch)
    
    # ========== UTILITY METHODS ==========
    
    def is_configured(self):
        """
        Verifica se a API está configurada
        
        Returns:
            bool: True se configurada, False caso contrário
        """
        return all([self.base_url, self.token, self.corporation_id])
    
    def test_connection(self):
        """
        Testa conexão com a API do SeAT
        
        Returns:
            tuple: (bool: sucesso, str: mensagem)
        """
        if not self.is_configured():
            return False, "SeAT API não configurada"
        
        try:
            # Tenta buscar dados da corporação
            self.get_corporation_wallet()
            return True, "Conexão com SeAT OK"
        except SeATAPIError as e:
            return False, str(e)
    
    def clear_cache(self, corporation_id=None):
        """
        Limpa cache de dados do SeAT
        
        Args:
            corporation_id: ID da corporação (limpa apenas dela se especificado)
        """
        corp_id = corporation_id or self.corporation_id
        
        if corp_id:
            cache_keys = [
                f"seat_corp_{corp_id}_wallet",
                f"seat_corp_{corp_id}_assets",
                f"seat_corp_{corp_id}_members",
                f"seat_corp_{corp_id}_structures",
            ]
            for key in cache_keys:
                cache.delete(key)
            logger.info(f"Cache do SeAT limpo para corporação {corp_id}")
        else:
            logger.warning("Corporation ID não especificado para limpar cache")


# Instância global do cliente SeAT
seat_api = SeATAPI()


# ========== HELPER FUNCTIONS ==========

def get_corporation_summary():
    """
    Busca sumário dos dados corporativos
    
    Returns:
        dict: Dicionário com wallet, assets, membros
    """
    if not seat_api.is_configured():
        return {
            'configured': False,
            'error': 'SeAT não configurado'
        }
    
    try:
        wallet = seat_api.get_corporation_wallet()
        members = seat_api.get_corporation_members()
        
        # Calcular saldo total da wallet
        total_balance = sum(w.get('balance', 0) for w in wallet)
        
        return {
            'configured': True,
            'wallet': {
                'divisions': wallet,
                'total_balance': total_balance
            },
            'members': {
                'count': len(members),
                'list': members
            }
        }
    except SeATAPIError as e:
        logger.error(f"Erro ao buscar sumário corporativo: {str(e)}")
        return {
            'configured': True,
            'error': str(e)
        }


def format_isk(value):
    """
    Formata valor ISK com separadores
    
    Args:
        value: Valor numérico
    
    Returns:
        str: Valor formatado (ex: "1,234,567.89 ISK")
    """
    try:
        return f"{value:,.2f} ISK"
    except (ValueError, TypeError):
        return "0.00 ISK"

