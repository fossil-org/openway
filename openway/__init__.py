class Package:
    def __init__(self, name: str, version: str | None = None, *, admin = False):
        self.name = name
        self.__admin = admin
        from ._version import Version
        self.version = Version.from_string(version or "v1.0.0")
        from pathlib import Path
        from os import getcwd
        self.path = Path(getcwd()) / name
        self.rel_path = self.path / ("init" if (p := self.version.to_string()) == "v1.0.0" else p)
        if not self.path.exists():
            raise FileNotFoundError(f"release {name} does not exist in {getcwd()}")
        elif not self.rel_path.exists() or self.name == ".openway":
            raise FileNotFoundError(f"release {name}/{self.version} does not exist. did you mean: {", ".join(self.get_rl()[:-1])} or {self.get_rl()[-1]}?")
        from ._pi import PackageInitializer
        self.pi = PackageInitializer(self.path / ".openway")
        if not self.pi.path.exists():
            self.pi.apply_default_rules()
        else:
            with self.pi.path.open() as file:
                if not file.read().strip():
                    self.pi.apply_default_rules()
        if not self.pi.check_legality(self.version.to_string(), admin=self.__admin):
            raise PermissionError(f"no access to release {name}/{self.version}, please contact the developers of {name} for access.")
    def get_f(self, filename: str):
        return (self.rel_path / filename).open("r+")
    def get_fc(self, filename: str):
        with self.get_f(filename) as file:
            c = file.read()
        return c
    def write_fc(self, filename: str):
        with self.get_f(filename) as file:
            file.write(c)
    def get_fp(self, filename: str):
        return self.rel_path / filename
    def get_r(self):
        return str(self.rel_path)
    def get_p(self):
        return str(self.path)
    def get_pl(self):
        from os import listdir, getcwd
        from os.path import exists, join
        return [i for i in listdir(getcwd()) if exists(join(getcwd(), i, ".openway"))]
    def get_fl(self):
        from os import listdir
        return listdir(self.rel_path)
    def get_rl(self):
        from os import listdir
        return list(sorted(["v1.0.0" if i == "init" else i for i in listdir(self.path) if i != ".openway"]))
    def different_version(self, version: str):
        return self.__class__(self.name, version)
    def advance_version(self, major_or_minor_or_patch: str, amount: int = 1):
        l = major_or_minor_or_patch.split(",")
        from ._version import Version
        return self.different_version(Version(
            self.version.major + (amount if "major" in l else 0),
            self.version.minor + (amount if "minor" in l else 0),
            self.version.patch + (amount if "patch" in l else 0)
        ).to_string())