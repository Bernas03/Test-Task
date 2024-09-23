import os
import shutil
import time
import hashlib
import logging
import argparse

# Função para calcular o hash MD5 de um arquivo / #Function to calculate the MD5 hash of a file
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Função para sincronizar as pastas / #Function to synchronize the folders
def sync_folders(source, replica, log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    # Verificar todos os arquivos na pasta de origem / #Check all files in the source folder
    for dirpath, dirnames, filenames in os.walk(source):
        relative_path = os.path.relpath(dirpath, source)
        replica_dir = os.path.join(replica, relative_path)
        
        # Se a pasta não existir na réplica, criá-la / #If the folder does not exist in the replica, create it
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            logging.info(f'Folder created: {replica_dir}')
            print(f'Folder created: {replica_dir}')

        # Verificar cada arquivo / #Check each file
        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            replica_file = os.path.join(replica_dir, filename)

            # Se o arquivo não existir ou for diferente, copiá-lo / #If the file does not exist or is different, copy it
            if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f'File copied: {source_file} -> {replica_file}')
                print(f'File copied: {source_file} -> {replica_file}')

    # Verificar e remover arquivos que existem na réplica, mas não na origem / #Check and remove files that exist in the replica, but not in the source
    for dirpath, dirnames, filenames in os.walk(replica):
        relative_path = os.path.relpath(dirpath, replica)
        source_dir = os.path.join(source, relative_path)

        # Remover arquivos extras / #Remove extra files
        for filename in filenames:
            replica_file = os.path.join(dirpath, filename)
            source_file = os.path.join(source_dir, filename)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f'File removed: {replica_file}')
                print(f'File removed: {replica_file}')

# Função principal para configurar argumentos e chamar a sincronização periodicamente / #Main function to set up arguments and call synchronization periodically
def main():
    parser = argparse.ArgumentParser(description="One-way folder sync.")
    parser.add_argument('source', type=str, help='Path to source folder')
    parser.add_argument('replica', type=str, help='Path to replica folder')
    parser.add_argument('interval', type=int, help='Sync interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')
    args = parser.parse_args()

    # Verificar se a pasta de origem existe / #Check if the source folder exists
    if not os.path.exists(args.source):
        print(f'Error: The source folder "{args.source}" does not exist.')
        return

    # Verificar se a pasta de réplica existe, caso contrário, criar / #Check if the replica folder exists, otherwise create
    if not os.path.exists(args.replica):
        os.makedirs(args.replica)
        print(f'Created replica folder: {args.replica}')
    
    # Verificar se o arquivo de log existe, caso contrário, criá-lo / #Check if the log file exists, otherwise create
    if not os.path.exists(args.log_file):
        open(args.log_file, 'w').close()  # Cria o arquivo vazio / #Create the empty file
        print(f'Log file created: {args.log_file}')

    # Sincronização periódica / #Periodic synchronization
    while True:
        sync_folders(args.source, args.replica, args.log_file)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
