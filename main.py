from modules.managers.ca_core import CaCore


def main():
    """
    Entry point of the application.
    Initializes and runs the core application.
    """
    core = CaCore()
    core.run()


if __name__ == "__main__":
    main()