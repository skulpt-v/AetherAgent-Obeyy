from memory import Database
from core.agent import AetherAgent
from tools.calculator import Calculator
from ui.cli import CLI


def main():
    """Obeyy uygulamasını başlatır."""

    cli = CLI()
    cli.show_banner()

    database = Database()

    try:
        agent = AetherAgent(database)

        calculator = Calculator()

        agent.register_tool(
            "calculator",
            calculator.calculate
        )

        latest_conversation = database.get_latest_conversation()

        if latest_conversation:
            conversation_id = latest_conversation["id"]

            cli.console.print(
                f"[dim]Mevcut konuşmaya devam ediliyor. "
                f"ID: {conversation_id}[/dim]"
            )

        else:
            conversation_id = database.create_conversation(
                title="Obeyy Sohbeti"
            )

            cli.console.print(
                f"[dim]Yeni konuşma oluşturuldu. "
                f"ID: {conversation_id}[/dim]"
            )

        cli.console.print(
            "[bold green]Obeyy hazır.[/bold green]"
        )

        cli.console.print(
            "[dim]Çıkmak için 'exit' veya 'quit' yazabilirsin.[/dim]\n"
        )

        while True:
            user_message = cli.get_input()

            if not user_message:
                continue

            if user_message.lower() in ("exit", "quit"):
                cli.show_goodbye()
                break

            try:
                response = agent.chat(
                    conversation_id=conversation_id,
                    user_message=user_message
                )

                cli.show_message(response)

            except Exception as error:
                cli.show_error(error)

    finally:
        database.close()


if __name__ == "__main__":
    main()