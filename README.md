# Update Filter Script

## Быстрый старт

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/ilyals/glinet.git
   ```

2. Перейдите в папку репозитория и установите зависимости:
   ```bash
   cd glinet
   pip install -r requirements.txt
   ```

3. Создайте файл .gitpassword для хранения имени пользователя и пароля для Git (или используйте ENV):
   ```bash
   echo 'GIT_USERNAME=your_username' > .gitpassword
   echo 'GIT_PASSWORD=your_password' >> .gitpassword
   ```

4. Запустите скрипт:
   ```bash
   python3 makelist.py
   ```

## Описание
Скрипт автоматически обновляет файл с IP-адресами и доменами, добавляет его в репозиторий и отслеживает изменения.
## Требования
- Python 3.x
- Установленные зависимости: requests
