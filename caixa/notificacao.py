from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class Notificador(ABC):
    @abstractmethod
    def notificar(self, mensagem: str) -> None: ...


class NotificadorArquivo(Notificador):
    """Grava cada evento numa linha: [data e hora] mensagem."""

    def __init__(self, caminho: str = "eventos_caixa.log") -> None:
        self._caminho = Path(caminho)

    def notificar(self, mensagem: str) -> None:
        momento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with self._caminho.open("a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{momento}] {mensagem}\n")

    def ler_eventos(self) -> list[str]:
        if not self._caminho.exists():
            return []
        return self._caminho.read_text(encoding="utf-8").splitlines()

class NotificadorConsole(Notificador):
    """Segunda implementação, para demonstrar que várias podem ser registradas."""

    def notificar(self, mensagem: str) -> None:
        print(f"  [evento] {mensagem}")