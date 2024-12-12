import socket
from typing import Union

class NetworkUtils:
    """
    Classe utilitária para operações relacionadas à rede.
    """

    @staticmethod
    def get_local_ip() -> Union[str, None]:
        """
        Obtém o endereço IP local da máquina.

        Retorna:
            str: O endereço IP local.
            None: Se não for possível determinar o endereço IP.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                # Conecta a um endereço remoto para determinar o IP local
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
            except (OSError, socket.error) as e:
                # Log adequado (caso necessário, utilizando biblioteca de logging)
                print(f"Erro ao obter IP local: {e}")
                return None

# Exemplo de uso
if __name__ == "__main__":
    ip_address = NetworkUtils.get_local_ip()
    if ip_address:
        print(f"Endereço IP Local: {ip_address}")
    else:
        print("Não foi possível determinar o endereço IP local.")