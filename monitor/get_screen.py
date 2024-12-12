import cv2
import os
import time

# Configuração da pasta para salvar as imagens
IMAGE_DIR = "../shared_folder/"  # Alterar para o diretório compartilhado
os.makedirs(IMAGE_DIR, exist_ok=True)

# Função para verificar a condição (exemplo: tempo decorrido ou algum evento específico)
def check_condition():
    # Exemplo: capturar imagem a cada 10 segundos
    return int(time.time()) % 10 == 0

# Função para capturar e salvar a imagem
def capture_image(frame):
    try:
        # Inicializa a captura da câmera
        # cap = cv2.VideoCapture(camera_index)
        # if not cap.isOpened():
        #     print("Erro ao acessar a câmera.")
        #     return
        #
        # Lê um frame da câmera
        # ret, frame = cap.read()
        # if not ret:
        #     print("Erro ao capturar o frame.")
        #     return

        # Nomeia a imagem com base no timestamp
        timestamp = int(time.time())
        image_name = f"image_{timestamp}.jpg"
        image_path = os.path.join(IMAGE_DIR, image_name)

        # Salva a imagem
        cv2.imwrite(image_path, frame)
        print(f"Imagem salva em: {image_path}")

        # Libera a câmera
        # cap.release()
    except Exception as e:
        print(f"Erro ao capturar imagem: {e}")

# Loop principal
# if __name__ == "__main__":
#     print(f"Diretório para salvar imagens: {IMAGE_DIR}")
#     print("Aguardando condição para capturar imagem...")
#
#     while True:
#         if check_condition():
#             capture_image()
#             time.sleep(1)  # Evita múltiplas capturas desnecessárias
