import subprocess
import shutil
import os
import zipfile

# Funkcje z danymi autoryzacji (credentials)

def getCredentials(location):
		# Zwraca dane autoryzacji do konkretnej lokalizacji (bazy danych lub serwera)
		if location == "old":
				return {
						"db_username": "old_db_username",
						"db_password": "old_db_password",
						"db_name": "old_db_name",
						"url": "old_url",
						"ip": "old_ip",
						"port": "old_port"
				}
		elif location == "new":
				return {
						"db_username": "new_db_username",
						"db_password": "new_db_password",
						"db_name": "new_db_name",
						"url": "new_url",
						"ip": "new_ip",
						"port": "new_port"
				}
		else:
				return {}

# Funkcje do backupu i przywracania bazy danych

def backupDatabase(credentials, output_file):
		# Wykonuje backup bazy danych
		command = f"mysqldump -u {credentials['db_username']} -p{credentials['db_password']} {credentials['db_name']} > {output_file}"
		print(f"subprocess.call({command}, shell=True)")
		# subprocess.call(command, shell=True)

def restoreDatabase(credentials, input_file):
		# Przywraca bazę danych z pliku SQL
		command = f"mysql -u {credentials['db_username']} -p{credentials['db_password']} {credentials['db_name']} < {input_file}"
		print(f"subprocess.call({command}, shell=True)")
		# subprocess.call(command, shell=True)

# Funkcje kopiujące i archiwizujące pliki

def copyAndZipFiles(source_directory, target_directory, protocol):
		# Kopiuje pliki (lokalnie lub przez SSH) i tworzy archiwum ZIP
		if protocol == "local":
				shutil.copytree(source_directory, target_directory)
		elif protocol == "ssh":
				ssh_credentials = getCredentials("new")  # Dane do SSH
				ssh_command = f"scp -r {source_directory} {ssh_credentials['ip']}:{target_directory}"
				subprocess.call(ssh_command, shell=True)

		# Tworzenie archiwum ZIP
		print(f"shutil.make_archive({target_directory}, 'zip', {target_directory})")
		shutil.make_archive(target_directory, 'zip', target_directory)
		# Usuwa katalog ze skopiowanymi plikami (bez archiwum)
		print(f"shutil.rmtree({target_directory})")
		shutil.rmtree(target_directory)

# Funkcja zmieniająca domenę w WordPress

def changeWordPressDomain(credentials, new_domain):
		# Edytuje wpis w tabeli wp_options w bazie danych WordPress, aby zmienić domenę
		db_credentials = credentials
		command = (
				f"mysql -u {db_credentials['db_username']} -p{db_credentials['db_password']} {db_credentials['db_name']} "
				f"-e \"UPDATE wp_options SET option_value = '{new_domain}' WHERE option_name = 'siteurl' OR option_name = 'home'\""
		)
		print(f"subprocess.call({command}, shell=True)")
		# subprocess.call(command, shell=True)

# Menu interaktywne

if __name__ == "__main__":
		while True:
				print("\nWybierz opcję:")
				print("1. Backup bazy danych")
				print("2. Przywracanie bazy danych na nowym serwerze")
				print("3. Kopiowanie i archiwizacja plików (lokalnie)")
				print("4. Zmiana domeny w WordPress")
				print("0. Wyjście")
				choice = input("Wprowadź numer opcji: ")

				if choice == '0':
						break
				elif choice == '1':
						old_credentials = getCredentials("old")
						backupDatabase(old_credentials, 'backup.sql')
						print("Backup zakończony pomyślnie")
				elif choice == '2':
						new_credentials = getCredentials("new")
						# restoreDatabase(new_credentials, 'backup.sql')
						print("Przywracanie zakończone pomyślnie")
				elif choice == '3':
						source_directory = '/ścieżka/do/katalogu/źródłowego'
						target_directory = '/ścieżka/do/katalogu/docelowego'
						protocol = 'local'
						# copyAndZipFiles(source_directory, target_directory, protocol)
						print("Kopiowanie i archiwizacja zakończone pomyślnie")
				elif choice == '4':
						new_credentials = getCredentials("new")
						new_domain = new_credentials['url']
						# print(f"changeWordPressDomain(new_credentials, new_domain)")
						changeWordPressDomain(new_credentials, new_domain)
						print("Zmiana domeny zakończona pomyślnie")
