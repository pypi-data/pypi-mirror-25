import click


@click.command()
def main():
    """
    This script will update your apt-key, apt-configuration, update apt, and install
    all required package in the list.
    """
    setup()
    print(get_disks())


if __name__ == "__main__":
    main()
