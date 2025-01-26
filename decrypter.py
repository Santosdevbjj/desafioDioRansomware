import os
import pyaes

def decrypt_file(encrypted_file, key):
    try:
        # Abrir o arquivo criptografado para leitura em modo binário
        with open(encrypted_file, "rb") as file:
            file_data = file.read()
        
        # Criar o objeto AES com a chave fornecida
        aes = pyaes.AESModeOfOperationCTR(key)

        # Descriptografar os dados
        decrypted_data = aes.decrypt(file_data)

        # Remover o arquivo criptografado
        os.remove(encrypted_file)

        # Restaurar o arquivo original
        original_file = encrypted_file.replace(".encrypted", "")
        with open(original_file, "wb") as new_file:
            new_file.write(decrypted_data)

        print(f"Arquivo '{encrypted_file}' descriptografado com sucesso como '{original_file}'.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{encrypted_file}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # Nome do arquivo criptografado e chave de descriptografia
    encrypted_file = "teste.txt.encrypted"
    key = b"chave_segura_16b"  # A chave deve ter 16 bytes

    # Validar tamanho da chave
    if len(key) != 16:
        print("Erro: A chave deve ter exatamente 16 bytes.")
    else:
        decrypt_file(encrypted_file, key)
