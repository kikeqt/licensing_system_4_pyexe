# Licensing system for Py2Exe
Licensing system for python scripts that are packaged in windows executables, based on public cryptography.  Includes simplified AES and RSA encryption module

The purpose is to create a system of restrictions that prevents unauthorized use for internal systems.  In addition to offering a simple way to encrypt information particularly that stored in the code or that which needs to be safeguarded.

Examples of use in each file .py

## Pre-requisitos
```
pip install pycryptodome
```

## Instalación
Descarge el código fuente de este proyecto en el directorio raíz del proyecto python que se desea restringir.

O clone el proyecto con git
```
git clone https://github.com/kikeqt/licensing_system_4_pyexe.git
```

## Funcionamiento
1. ***signer.py*** genera una firma electronica del equipo.  Si no se han generado ***private.pem*** y ***public.pem*** generará automaticamente una vez que se defina la contraseña para proteger la clave privada, por ejemplo ***example_4_signer_gui.py***.
2. ***license\_verifier.py*** verifica la firma

En el proceso se crean 3 archivos ***private.pem***, ***public.pem*** y ***\<hostname\>.lic***.

***private.pem*** contiene la clave privada y cifrada con AES en modo OCB.

***public.pem*** contiene la clave pública.

***\<hostname\>.lic*** contiene datos del equipo firmado digitalmente, con la clave privada

**Observaciones:**
* Si desea cambiar los nomres de los archivos, estos estan definidos en ***license_verifier.py***, líneas_ `22`, `24` y `46`.

* Si en lugar de abrir las llaves públicas y privadas desde un archivo, prefiere almacenarlas en el código, encontrará marcado donde debe hacer el cambio, ***license_verifier.py*** \[`42`\] y ***signer.py*** \[`35`,`36`\].

## Uso sugerido
1. Deberá ejecutar en el equipo que se va a autorizar ***signer.py*** o ***example_4_signer_gui.py***, lo que generará el archivo de licencia correspondiente ***\<hostname\>.lic***.
    * En ***signer.py***, usted deberá cambiar la contraseña de la clave privada, en línea `98`, _se suguiere en su lugar implementar un método de entrada, por ejemplo:_

´´´
print('Type the password')
password =input()
´´´

    * O en ***example_4_signer_gui.py*** usted debera introducirla en el campo indicado.

2. Dejar en el directorio del ejecutable que se desea proteger los archivos ***public.pem*** y ***license_verifier.py***.  Puede omitir a ***public.pem*** si se introdujo en la variable de indicada para ***license_verifier.py***