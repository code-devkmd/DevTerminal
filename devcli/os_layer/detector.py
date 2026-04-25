import platform

OS_TYPE = platform.system().lower()

IS_WINDOWS = OS_TYPE == "windows"
IS_LINUX = OS_TYPE == "linux"
IS_MAC = OS_TYPE == "darwin"