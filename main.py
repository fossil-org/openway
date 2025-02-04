from openway import Package, AdminPackage, INIT

mypackage = Package("mypackage", 1, key="Password123")

print(mypackage.get_fc("main.py"))