import tkinter as tk

from src.gui import WhitespaceNormalizerApp, logger


def main():
    """Creates and runs the application."""
    logger.info("Starting WhitespaceNormalizer application")
    try:
        root = tk.Tk()
        app = WhitespaceNormalizerApp(root)
        logger.info("Entering main application loop")
        root.mainloop()
    except Exception as e:
        logger.critical(f"Application crashed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
