import requests

class BotCuspidorAPI:
    def __init__(self, base_url = "http://backend-java:7010/cuspidor-bot/api"):
        self.base_url = base_url
        
    async def criar_usuario(self, name:str, user_id_telegram: str) -> bool:
        url = f"{self.base_url}/user/create"
        payload = {
            "name": f"Usuario {name}",
            "id_telegram": user_id_telegram
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 201:
                return True 
            else:
                print(f"Falha ao criar usuário: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
        return False

    async def tornar_premium(self, user_id: str):
        url = f"{self.base_url}/user/become-premium/{user_id}"
        try:
            response = requests.post(url, timeout=5)
            return response.status_code
        except requests.RequestException as e:
            print(f"Erro ao consultar API: {e}")
        # propaga exceção para ser tratada por quem chamou
        raise e