# Update Filter Script

## ������� �����

1. ����������� �����������:
   ```bash
   git clone https://github.com/ilyals/glinet.git
   ```

2. ��������� � ����� ����������� � ���������� �����������:
   ```bash
   cd glinet
   pip install -r requirements.txt
   ```

3. �������� ���� .gitpassword ��� �������� ����� ������������ � ������ ��� Git (��� ����������� ENV):
   ```bash
   echo 'GIT_USERNAME=your_username' > .gitpassword
   echo 'GIT_PASSWORD=your_password' >> .gitpassword
   ```

4. ��������� ������:
   ```bash
   python3 makelist.py
   ```

## ��������
������ ������������� ��������� ���� � IP-�������� � ��������, ��������� ��� � ����������� � ����������� ���������.
## ����������
- Python 3.x
- ������������� �����������: requests
