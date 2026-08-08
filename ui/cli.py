from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.text import Text


class CLI:
    """Obeyy için Rich tabanlı terminal arayüzü."""

    def __init__(self):
        self.console = Console()

    def show_banner(self):
        """Başlangıç ekranını gösterir."""

        self.console.print(
            Panel(
                Text(
                    "O B E Y Y\n"
                    "Intelligent AI Assistant",
                    justify="center"
                ),
                title="🤖 Obeyy",
                border_style="cyan"
            )
        )

    def show_message(self, message: str):
        """Obeyy'nin cevabını gösterir."""

        self.console.print(
            Panel(
                Markdown(message),
                title="🤖 Obeyy",
                border_style="green"
            )
        )

    def get_input(self) -> str:
        """Kullanıcıdan mesaj alır."""

        return Prompt.ask(
            "[bold cyan]Sen[/bold cyan]"
        ).strip()

    def show_error(self, error: str):
        """Hata mesajını gösterir."""

        self.console.print(
            Panel(
                str(error),
                title="⚠ Hata",
                border_style="red"
            )
        )

    def show_goodbye(self):
        """Kapanış mesajını gösterir."""

        self.console.print(
            "\n[bold cyan]Obeyy kapatılıyor... 👋[/bold cyan]"
        )