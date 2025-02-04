class PackageInitializer:
    def __init__(self, path):
        self.path = path
        self.pkg_path = path.parent
        self.rules = {}
    def apply_default_rules(self):
        from os import listdir
        with self.path.open("w") as file:
            from . import INIT
            file.write("\n".join(list(sorted([f"{INIT if i == "init" else i}: nR" for i in listdir(self.pkg_path) if i != ".openway"]))))
    def parse(self):
        with self.path.open() as file:
            c = file.read()
        for lnn, ln in enumerate(c.split("\n"), start=1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                rel, status = [i.strip() for i in ln.split(":", 2)]
                status = status.lower()
                if status not in ["nr", "r", "ar"]:
                    raise SyntaxError(f"unknown rule '{status}'")
                self.rules[rel] = status
            except ValueError:
                raise SyntaxError(f"invalid .openway file syntax on line {lnn}: '{ln}'")
        from os import listdir
        from . import INIT
        l = [i for i in [INIT if i2 == "init" else i2 for i2 in listdir(self.pkg_path)] if i not in list(self.rules.keys()) + [".openway"]]
        if l:
            raise SyntaxError(f"missing rules for release{'s' if len(l) != 1 else ''}: {', '.join([INIT if i == "init" else i for i in l])}.\nhint: use `rm {self.path}` and run this program again to reset the .openway file.")
    def check_legality(self, rel, *, admin = False):
        self.parse()
        from . import INIT
        status = self.rules[INIT if rel == "init" else rel]
        return not ((status == "ar") or (status == "r" and not admin))