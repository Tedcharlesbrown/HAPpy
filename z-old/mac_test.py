import sys
print(sys.executable)
if sys.version_info[0] == 3:
    print("FOO")
else:
    print("BAR")