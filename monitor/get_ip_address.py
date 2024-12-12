import socket

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Conecta a um endereço remoto para determinar o IP local
            s.connect(("8.8.8.8", 80))  # Usa o Google DNS como referência
            return s.getsockname()[0]
        except Exception as e:
            return f"Erro ao obter IP: {e}"

ip_address = get_local_ip()
print(f"Endereço IP Local: {ip_address}")