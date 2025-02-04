"""
openway init <name> - initializes a package
        github - opens the openway github page
        list - lists all packages in the current directory
        help - shows this message
"""

def main():
    from sys import argv
    from os import mkdir, getcwd
    from os.path import join
    from pathlib import Path
    import webbrowser

    try:
        if argv[1] == "init":
            path = Path(getcwd(), argv[2])
            path.mkdir()
            (path / "init").mkdir()
            from ._pi import PackageInitializer
            PackageInitializer((path / ".openway")).apply_default_rules()
        elif argv[1] == "list":
            from . import Package
            print(f"packages in {getcwd()}:\n- {'\n- '.join(Package.get_pl())}")
        elif argv[1] == "github":
            webbrowser.open(f"https://github.com/fossil-org/openway")
        elif argv[1] == "help":
            print(__doc__)
    except IndexError:
        print("not enough arguments. run openway help for more info.")

main()