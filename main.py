from openway import Package

mypackage = Package("mypackage", 1, key="Password123")

exec(mypackage.get_fc("main.py"))