import ctypes, sys, os, shutil, configparser, time

settings = configparser.ConfigParser()
settings.read('install_1S.ini', encoding='utf-8')
OneS_files = settings['MAIN']['files_1S']
ver = settings['MAIN']['ver']
core_path = OneS_files
dest_path = os.path.join('C:' + os.sep, 'Windows', 'Temp', ver)
program_path = os.path.join('C:' + os.sep, 'Program Files (x86)', '1cv8', ver)

def install_1s():
    shutil.copytree(core_path, dest_path)
    print('Копирование временных файлов завершено')
    os.system(r'msiexec -i "' + dest_path + os.sep + '1CEnterprise 8.msi' + '"-quiet TRANSFORMS=adminstallrelogon.mst;1049.mst DESIGNERALLCLIENTS=1 THICKCLIENT=1 THINCLIENTFILE=1 THINCLIENT=1 WEBSERVEREXT=0 SERVER=0 CONFREPOSSERVER=0 CONVERTER77=0 SERVERCLIENT=0 LANGUAGES=RU')
    print('Установка 1С завершена')
    if os.path.exists(program_path + os.sep + 'bin'):
        os.rename(program_path + os.sep + 'bin' + os.sep + 'techsys.dll', program_path + os.sep + 'bin' + os.sep + 'techsys_100.dll')
        print('Переименование завершено')
        shutil.copy(dest_path + os.sep + 'techsys.dll', program_path + os.sep + 'bin')
        print('Копирование завершено')
        time.sleep(5)
        shutil.rmtree(dest_path)
        print('Удаление временных файлов завершено')
        print('Установка завершена, закройте окно')

def uninstall_1s():
    os.mkdir(dest_path)
    shutil.copy(core_path + os.sep + '1CEnterprise 8.msi', dest_path)
    print('Копирование временных файлов завершено')
    os.system(r'msiexec -uninstall "' + dest_path + os.sep + '1CEnterprise 8.msi' + '"-quiet')
    print('Удаление 1С завершено')
    time.sleep(5)
    if os.path.exists(program_path + os.sep + 'bin'):
        shutil.rmtree(program_path)
        print('Директория 1С удалена')
    time.sleep(5)
    shutil.rmtree(dest_path)
    print('Удаление временных файлов завершено')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



if is_admin():
    pass
    # Code of your program here
    if os.path.exists(program_path + os.sep + 'bin'):
        uninstall_1s()
    else:
        install_1s()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
