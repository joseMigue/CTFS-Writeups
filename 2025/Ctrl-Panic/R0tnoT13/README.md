El sistema mantiene un estado interno de 128 bits S, derivado de AES. Para verificar integridad de hardware, el firmware registra valores de la forma:
S ⊕ ROTR(S, k)
para distintos valores de rotación k.
Por un error de logging, se filtran varios de estos valores, junto con:
los k correspondientes
dos bits conocidos del estado (no los vi pero use 1 y 0 porque parece que es lo más normal)
un ciphertext cifrado usando el estado
El objetivo es reconstruir S y recuperar el mensaje cifrado.

<img width="482" height="263" alt="imagen1" src="https://github.com/user-attachments/assets/7c7cd9fd-a717-4430-a7ef-36e9d1d9d899" />

El script solveRot.py se encarga de reconstruir el estado interno secreto S de 128 bits usando la información filtrada por los logs del sistema. Cada log tiene la forma S ⊕ ROTR(S, k), donde ROTR es una rotación de bits hacia la derecha. La idea clave es que estas ecuaciones son lineales a nivel de bits, así que pueden modelarse como restricciones lógicas. El script usa Z3 para crear un vector de 128 bits que representa S y agrega una ecuación por cada par (k, valor_filtrado) conocido. Además, incorpora los bits ancla del estado (los bits conocidos que da el challenge) para romper simetrías y asegurar una solución única. Una vez que el solver encuentra un modelo consistente, el script reconstruye S completo y lo imprime en hexadecimal.

<img width="545" height="45" alt="imagen2" src="https://github.com/user-attachments/assets/66f81e3e-f9d5-4061-8a84-ded1f5e0248f" />

Luego el script crypt.py toma el estado interno S ya recuperado y lo usa para descifrar el ciphertext provisto por el challenge. En este caso, el cifrado es simple: el estado actúa directamente como keystream, por lo que descifrar consiste en hacer un XOR entre el ciphertext y los bytes de S. El script convierte el estado hexadecimal en bytes, hace el XOR byte a byte con el ciphertext y muestra el resultado.

<img width="522" height="68" alt="imagen3" src="https://github.com/user-attachments/assets/d919b91d-f2df-460d-850e-10de6ff3009f" />
