"""Command-line interface for the forgebase chat application."""

import asyncio

import click

from forgebase.infrastructure import config, logging_config


@click.group()
def main() -> None:
    """Forgebase CLI."""


@main.command()
@click.option("--debug", is_flag=True, help="Enable debug logging.")
def chat(debug: bool) -> None:
    """Starts an interactive chat session."""
    logging_config.setup_logging(debug)
    chat_service = config.get_chat_service()

    async def run() -> None:
        """Runs the async chat loop."""
        print("Starting chat session. Type /exit to end, /reset to clear.")
        while True:
            try:
                user_input = await asyncio.to_thread(lambda: input("User> "))
                if user_input.lower() == "/exit":
                    break
                if user_input.lower() == "/reset":
                    await chat_service.reset_chat()
                    print("Conversation reset.")
                    continue

                print("Agent> ", end="")
                async for chunk in chat_service.send_message_stream(user_input):
                    print(chunk, end="", flush=True)
                print()
            except (KeyboardInterrupt, EOFError):
                break
        print("\nExiting chat session.")

    asyncio.run(run())


if __name__ == "__main__":
    main()
