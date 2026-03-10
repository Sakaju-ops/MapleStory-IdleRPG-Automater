#!/usr/bin/env python3
"""
MapleStory Idle Bot - Main Entry Point
"""

import argparse
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def run_gui():
    """Launch the graphical user interface."""
    try:
        from gui.launcher import BotLauncher
        app = BotLauncher()
        app.run()

    except ImportError as e:
        print(f"Error: GUI dependencies not installed: {e}")
        print("Install with: pip install customtkinter pillow")
        sys.exit(1)


def run_cli(args):
    """Run in CLI mode."""
    from core.adb_controller import ADBController
    from core.logger import setup_logger
    from config import ConfigManager
    from games.maple_story_idle import MapleStoryIdleBot

    config_manager = ConfigManager(args.config)
    config = config_manager.load()

    logger = setup_logger("maple_bot", "info")

    adb = ADBController(host="127.0.0.1", port=5555, logger=logger)

    if not adb.connect():
        logger.error("Failed to connect to BlueStacks")
        sys.exit(1)

    bot_config = config.get("bot-option", {})
    bot_config["templates_dir"] = str(Path(__file__).parent / "templates" / "maple_story_idle")

    bot = MapleStoryIdleBot(adb, bot_config, logger)

    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    finally:
        bot.stop()
        adb.disconnect()


def main():
    parser = argparse.ArgumentParser(description="MapleStory Idle Bot")

    parser.add_argument("--cli", action="store_true")
    parser.add_argument("--config", default="config/settings.yaml")

    args = parser.parse_args()

    if args.cli:
        run_cli(args)
    else:
        run_gui()


if __name__ == "__main__":
    main()
