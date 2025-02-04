class Version:
    def __init__(self, major, minor, patch):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)
    def to_string(self):
        return f"v{self.major}.{self.minor}.{self.patch}"
    def __str__(self):
        return self.to_string()
    @classmethod
    def from_string(cls, s):
        if isinstance(s, int) or isinstance(s, str) and s.isnumeric():
            return cls(s, 0, 0)
        elif isinstance(s, float) or isinstance(s, str) and s.replace(".", "").isnumeric():
            return cls(int(float(s)), int(str(s)[str(s).index(".") + 1:]), 0)
        elif isinstance(s, str):
            s = s.removeprefix("v")
            try:
                mj, mn, pt = s.split(".")
            except ValueError:
                raise SyntaxError(f'legal formats for version number: major, "major", major.minor, "major.minor", "major.minor.patch"')
            return cls(int(l[0]), int(l[1]), int(l[2]))