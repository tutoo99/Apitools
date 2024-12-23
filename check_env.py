import sys
import platform

print(f"Python 版本: {platform.python_version()}")
print(f"Python 路径: {sys.executable}")
print("\n系统路径:")
for path in sys.path:
    print(path) 