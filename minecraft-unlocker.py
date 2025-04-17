import os
import platform
import ctypes
import shutil
import subprocess
import locale

actual_directory = os.path.dirname(os.path.abspath(__file__))

archive_name = "Windows.ApplicationModel.Store.dll"
original_dll = os.path.join(os.environ['SystemRoot'], 'System32', archive_name)
original_dll_sys_wow64 = os.path.join(os.environ['SystemRoot'], 'SysWOW64', archive_name)

operational_system = platform.architecture()[0]

crack_dll = os.path.join(actual_directory, operational_system, "System32", archive_name)
crack_dll_sys_wow_64 = os.path.join(actual_directory, operational_system, "SysWOW64", archive_name)


def get_system_language():
    language, _ = locale.getlocale()
    return language


def take_ownership(path):
    subprocess.call(f'takeown /f "{path}"', shell=True)
    system_language = get_system_language()

    if system_language == 'pt_BR':  # Português
        subprocess.call(f'icacls "{path}" /grant "Administradores":F', shell=True)
    else:  # Para outros idiomas, como o inglês
        subprocess.call(f'icacls "{path}" /grant "Administrators":F', shell=True)


def is_admin():
    # Verifica se o script esta sendo executado como administrador
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def sub_dll(dll_path: str, crack_dll_path: str):
    try:
        take_ownership(dll_path)
        os.remove(dll_path)
        shutil.copy2(crack_dll_path, dll_path)
    except PermissionError as e:
        print("Não foi possivel substituir a dll, erro de permissão.", e)


def crack_64():
    if (is_admin()):
        print("Substituindo a dll do sys32...")
        sub_dll(original_dll, crack_dll)
        print("Substituindo a dll do sysWOW64...")
        sub_dll(original_dll_sys_wow64, crack_dll_sys_wow_64)

    else:
        print("Execute como administrador")


def crack_32():
    print(operational_system, "identificado...")
    if os.path.exists(original_dll): print(f'Arquivo {archive_name} encontrado.')
    if os.path.exists(crack_dll): print(f'Arquivo {crack_dll} encontrado.')

    if (is_admin()):
        print("Substituindo a dll do sys32...")
        sub_dll(original_dll, crack_dll)

    else:
        print("Execute como administrador")


if operational_system == "64bit": crack_64()
if operational_system == "32bit": crack_32()
