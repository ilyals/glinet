import requests
import os
import subprocess
import re
import socket
from datetime import datetime
from ipaddress import ip_network, ip_address
import shutil

# Настройки репозитория
repo_url = "https://github.com/ilyals/glinet.git"
repo_dir = os.path.join(os.getcwd(), "glinet")
list_file = "listrepo.txt"
output_file = "filterfromvpn.txt"
script_name = "makelist.py"  # Название самого скрипта
readme_file = "README.md"

# Абсолютный путь к самому скрипту
current_script_path = os.path.abspath(__file__)

# Клонирование или обновление репозитория
if os.path.isdir(repo_dir):
    os.chdir(repo_dir)
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    subprocess.run(["git", "clone", repo_url, repo_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir(repo_dir)

# Добавление самого скрипта в репозиторий, если он ещё не существует там
if not os.path.isfile(script_name):
    shutil.copy(current_script_path, os.path.join(repo_dir, script_name))
    subprocess.run(["git", "add", script_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Добавление самого скрипта в репозиторий, если он ещё не существует там
script_path = os.path.join(os.getcwd(), script_name)
if not os.path.isfile(script_name):
    shutil.copy(os.path.join("..", script_name), script_path)
    subprocess.run(["git", "add", script_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Создание README.md с инструкцией по развертыванию, если он отсутствует
if not os.path.isfile(readme_file):
    with open(readme_file, "w") as f:
        f.write("# Update Filter Script\n\n")
        f.write("## Быстрый старт\n\n")
        f.write("1. Склонируйте репозиторий:\n")
        f.write("   ```bash\n")
        f.write(f"   git clone {repo_url}\n")
        f.write("   ```\n\n")
        f.write("2. Перейдите в папку репозитория и запустите скрипт:\n")
        f.write("   ```bash\n")
        f.write(f"   cd {repo_dir}\n")
        f.write(f"   python3 {script_name}\n")
        f.write("   ```\n\n")
        f.write("## Описание\n")
        f.write("Скрипт автоматически обновляет файл с IP-адресами и доменами, добавляет его в репозиторий и отслеживает изменения.\n")
        f.write("## Требования\n- Python 3.x\n- Установленные зависимости: requests\n")
    subprocess.run(["git", "add", readme_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Проверка наличия файла listrepo.txt
if not os.path.isfile(list_file):
    print(f"Файл {list_file} не найден в репозитории.")
    exit(1)

# Чтение списка URL-адресов из файла listrepo.txt
with open(list_file, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# Регулярные выражения для IP-адресов и доменов
ip_pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$")
domain_pattern = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

unique_ips = set()
domains = set()

# Сбор всех уникальных IP-адресов и доменов
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        for line in data.splitlines():
            line = line.strip()
            if ip_pattern.match(line):
                unique_ips.add(line)
            elif domain_pattern.match(line):
                domains.add(line)

# Преобразование уникальных IP и подсетей в объекты ip_network для проверки вхождений
networks = {ip_network(ip, strict=False) for ip in unique_ips}

# Проверка доменов на соответствие IP-адресам и подсетям из списка
filtered_domains = set()
for domain in domains:
    try:
        domain_ip = ip_address(socket.gethostbyname(domain))
        if not any(domain_ip in net for net in networks):
            filtered_domains.add(domain)
    except (socket.gaierror, ValueError):
        pass  # Пропуск доменов, которые не разрешаются или неправильные IP

# Сортировка IP-адресов по сетям
sorted_ips = sorted(networks, key=lambda net: (net.network_address, net.prefixlen))
sorted_domains = sorted(filtered_domains)

# Чтение предыдущего содержимого файла для сравнения
previous_ips, previous_domains = set(), set()
if os.path.isfile(output_file):
    with open(output_file, "r") as f:
        for line in f:
            line = line.strip()
            if ip_pattern.match(line):
                previous_ips.add(line)
            elif domain_pattern.match(line):
                previous_domains.add(line)

# Подсчет изменений
added_ips = set(map(str, sorted_ips)) - previous_ips
removed_ips = previous_ips - set(map(str, sorted_ips))
added_domains = set(sorted_domains) - previous_domains
removed_domains = previous_domains - set(sorted_domains)

# Запись итогового результата
with open(output_file, "w") as f:
    f.write("\n".join(map(str, sorted_ips)) + "\n" + "\n".join(sorted_domains))

# Формирование коммит-сообщения
date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_message = (f"[{date_now}] Обработаны источники: {', '.join(urls)}\n"
                  f"Добавлено IP: {len(added_ips)}, Удалено IP: {len(removed_ips)}\n"
                  f"Добавлено доменов: {len(added_domains)}, Удалено доменов: {len(removed_domains)}\n"
                  f"Общее количество: IP ({len(sorted_ips)}) / Domains ({len(sorted_domains)})")

# Вывод статистики изменений для пользователя
print("Статистика изменений:")
print(f"Добавлено IP: {len(added_ips)}, Удалено IP: {len(removed_ips)}")
print(f"Добавлено доменов: {len(added_domains)}, Удалено доменов: {len(removed_domains)}")
print(f"Общее количество IP: {len(sorted_ips)}")
print(f"Общее количество доменов: {len(sorted_domains)}")

# Добавление, коммит и пуш изменений
subprocess.run(["git", "add", output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["git", "commit", "-m", commit_message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["git", "push", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
