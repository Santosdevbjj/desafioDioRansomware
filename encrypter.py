import os
import pyaes

def encrypt_file(file_name, key):
    try:
        # Abrir o arquivo para leitura em modo binário
        with open(file_name, "rb") as file:
            file_data = file.read()
        
        # Remover o arquivo original
        os.remove(file_name)

        # Criar o objeto AES com a chave fornecida
        aes = pyaes.AESModeOfOperationCTR(key)

        # Criptografar os dados
        crypto_data = aes.encrypt(file_data)

        # Salvar o arquivo criptografado com nova extensão
        encrypted_file = f"{file_name}.encrypted"
        with open(encrypted_file, "wb") as new_file:
            new_file.write(crypto_data)

        print(f"Arquivo '{file_name}' criptografado com sucesso como '{encrypted_file}'.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_name}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # Nome do arquivo e chave de criptografia
    file_name = "teste.txt"
    key = b"chave_segura_16b"  # A chave deve ter 16 bytes

    # Validar tamanho da chave
    if len(key) != 16:
        print("Erro: A chave deve ter exatamente 16 bytes.")
    else:
        encrypt_file(file_name, key)
