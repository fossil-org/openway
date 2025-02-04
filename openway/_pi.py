ACCESS_DENIED = 0
ACCESS_GRANTED = 1
INCORRECT_PASSWORD = 2

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
        comment = False
        for lnn, ln in enumerate(c.split("\n"), start=1):
            ln = ln.strip().split("//", 2)[0]
            if ln.startswith("/*"):
                comment = True
                continue
            if "*/" in ln:
                comment = False
                ln = ln.split("*/", 2)[1]
            if not ln or comment:
                continue
            try:
                rel, status = [i.strip() for i in ln.split(":", 2)]
                if status.lower().split(" ")[0] == "kr":
                    self.rules[rel] = status.split(" ", 2)
                    self.rules[rel][0] = self.rules[rel][0].lower()
                    try:
                        self.rules[rel][1] = self.rules[rel][1].strip("\"'")
                    except IndexError:
                        raise SyntaxError(f"a string must be provided along with {status.split(" ")[0]}. example: '{rel}: {status.split(" ")[0]} \"enter text here\"'")
                elif status.lower() not in ["n", "r", "ar", "kr"]:
                    raise SyntaxError(f"unknown rule '{status}'")
                else:
                    self.rules[rel] = status
            except ValueError:
                raise SyntaxError(f"invalid .openway file syntax on line {lnn}: '{ln}'")
        from os import listdir
        from . import INIT
        l = [i for i in [INIT if i2 == "init" else i2 for i2 in listdir(self.pkg_path)] if i not in list(self.rules.keys()) + [".openway"]]
        if l:
            raise SyntaxError(f"missing rules for release{'s' if len(l) != 1 else ''}: {', '.join([INIT if i == "init" else i for i in l])}.\nhint: use `rm {self.path}` and run this program again to reset the .openway file.")
    def check_legality(self, rel, *, key = None, admin = False):
        self.parse()
        from . import INIT
        status = self.rules[INIT if rel == "init" else rel]
        obj = None
        if isinstance(status, list):
            status, obj = status
        status = status.lower()
        if status == "kr" and str(key) != str(obj):
            return INCORRECT_PASSWORD
        return ACCESS_DENIED if (status == "ar") or (status == "r" and not admin) else ACCESS_GRANTED