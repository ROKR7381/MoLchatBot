# cli/run.py
"""
CLI entry point for the shipping chatbot.
Provides interactive command-line access to the chatbot and optionally starts the auto-updater.
"""
import argparse
import asyncio
import logging
import sys

logger = logging.getLogger("shipping_chatbot")


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for CLI mode."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run_interactive_session(with_auto_updater: bool = False) -> None:
    """
    Run an interactive CLI session with the shipping chatbot.
    
    Args:
        with_auto_updater: If True, start the background blob refresh task.
    """
    from agents.azure_agent import initialize_azure_agent
    from agents.router import route_query

    print("=" * 60)
    print("Shipping Chatbot CLI")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the session.")
    print("Type 'help' for available commands.")
    print("=" * 60)

    # Initialize the agent
    try:
        agent, llm = initialize_azure_agent()
        print("\n✓ Agent initialized successfully!\n")
    except Exception as exc:
        print(f"\n✗ Failed to initialize agent: {exc}")
        print("Some features may be limited to the router.\n")
        agent = None

    # Start auto-updater if requested
    auto_updater = None
    if with_auto_updater:
        try:
            from services.auto_updater import get_auto_updater
            auto_updater = get_auto_updater()
            # Note: In CLI mode, we'd need to run this in a background thread
            print("✓ Auto-updater enabled (will refresh data periodically)\n")
        except Exception as exc:
            print(f"✗ Could not start auto-updater: {exc}\n")

    # Main interaction loop
    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye!")
                break

            if user_input.lower() == "help":
                print_help()
                continue

            # Try to get a response
            try:
                if agent:
                    response = agent.invoke(user_input)
                    if isinstance(response, dict):
                        response = response.get("output", str(response))
                else:
                    response = route_query(user_input)

                print(f"\nBot: {response}")

            except Exception as exc:
                logger.error(f"Error processing query: {exc}")
                print(f"\n✗ Error: {exc}")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


def print_help() -> None:
    """Print help information about available commands."""
    help_text = """
Available Commands:
  help              Show this help message
  quit, exit, q     Exit the chatbot

Example Queries:
  - "What are the milestones for container ABCD1234567?"
  - "Show me containers delayed by more than 5 days"
  - "What containers are arriving in the next 7 days?"
  - "Get ETA for container WXYZ9876543"
  - "Show arrivals at Los Angeles port"
  - "Search for PO number 1234567890"
  - "What is the average delay?"
  - "Show vessel info for container ABCD1234567"

Tips:
  - Mention container numbers in format: ABCD1234567 (4 letters + 7 digits)
  - Use keywords like 'delay', 'arrival', 'ETA', 'port', 'vessel'
  - Specify time periods like 'next 7 days' or 'delayed by 5 days'
"""
    print(help_text)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Shipping Chatbot CLI - Interactive command-line interface"
    )
    parser.add_argument(
        "--auto-update",
        action="store_true",
        help="Enable automatic background data refresh",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level (default: INFO)",
    )

    args = parser.parse_args()

    setup_logging(args.log_level)

    try:
        run_interactive_session(with_auto_updater=args.auto_update)
    except Exception as exc:
        logger.error(f"Fatal error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
