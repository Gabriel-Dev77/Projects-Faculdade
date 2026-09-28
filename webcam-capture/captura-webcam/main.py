import sys
from datetime import datetime
from pathlib import Path
import cv2


def abrir_camera(indice: int = 0) -> cv2.VideoCapture:
    """Abre a câmera usando o backend mais adequado ao sistema."""
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(indice, cv2.CAP_DSHOW)  # abre mais rápido no Windows
    else:
        cap = cv2.VideoCapture(indice)

    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir a câmera {indice}.")

    # Resolução desejada (a câmera pode ajustar para a mais próxima suportada)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap


def main() -> None:
    pasta_saida = Path("capturas")
    pasta_saida.mkdir(exist_ok=True)

    cap = abrir_camera(0)
    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Câmera aberta em {largura}x{altura}")
    print("Teclas: [s] salvar foto | [q] ou [ESC] sair")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Falha ao ler o frame.")
                break

            # Espelha a imagem para parecer um espelho (opcional)
            frame = cv2.flip(frame, 1)

            # Exibe uma cópia com instruções, sem "sujar" a foto salva
            exibicao = frame.copy()
            cv2.putText(exibicao, "s: salvar | q: sair", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Webcam", exibicao)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("s"):
                nome = datetime.now().strftime("foto_%Y%m%d_%H%M%S.png")
                caminho = pasta_saida / nome
                cv2.imwrite(str(caminho), frame)
                print(f"Foto salva em {caminho}")
            elif tecla in (ord("q"), 27):  # 27 = ESC
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()