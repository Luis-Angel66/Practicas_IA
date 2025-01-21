import os  # Librería para realizar operaciones con el sistema de archivos
import tkinter as tk  # Librería para crear interfaces gráficas de usuario
from tkinter import ttk, filedialog, messagebox, simpledialog  # Widgets y cuadros de diálogo adicionales
from cryptography.hazmat.primitives.asymmetric import dh, rsa  # Algoritmos de criptografía asimétrica
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15  # Esquema de relleno para firmas RSA
from cryptography.hazmat.primitives import serialization, hashes  # Funciones para serialización y hashes criptográficos
from cryptography.hazmat.primitives.kdf.hkdf import HKDF  # Función de derivación de claves (KDF)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Cifrado simétrico
from cryptography.hazmat.backends import default_backend  # Backend criptográfico
import secrets  # Generación de números aleatorios seguros

# Crear un directorio donde se almacenarán los archivos generados por el programa
PROJECT_DIR = "project_files"
os.makedirs(PROJECT_DIR, exist_ok=True)  # Si el directorio no existe, lo crea

# **Funciones Auxiliares**

def save_to_file(data, filename):
    """
    Guarda datos binarios en un archivo dentro del directorio del proyecto.
    """
    with open(os.path.join(PROJECT_DIR, filename), 'wb') as f:
        f.write(data)

def load_from_file(filename):
    """
    Carga datos binarios desde un archivo dentro del directorio del proyecto.
    """
    with open(os.path.join(PROJECT_DIR, filename), 'rb') as f:
        return f.read()

# **Funciones para Manejo de Relleno en AES**
from cryptography.hazmat.primitives import padding  # Importación específica para PKCS7

def pad_data(data):
    """
    Aplica relleno PKCS7 a los datos para que sean múltiplos del tamaño del bloque del algoritmo AES.
    """
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    return padder.update(data) + padder.finalize()

def unpad_data(data):
    """
    Elimina el relleno PKCS7 de los datos descifrados.
    """
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()

# **Clase Principal de la Aplicación Gráfica**

class CryptographyApp:
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica, configurando las pestañas y sus funcionalidades.
        """
        self.root = root
        self.root.title("Criptografía Híbrida - Proyecto")  # Título de la ventana principal
        self.root.geometry("800x600")  # Dimensiones iniciales de la ventana

        # Configuración de las pestañas
        self.tab_control = ttk.Notebook(root)

        # Crear tres pestañas principales
        self.dh_tab = ttk.Frame(self.tab_control)  # Pestaña para generación de claves DH
        self.cipher_tab = ttk.Frame(self.tab_control)  # Pestaña para cifrado y descifrado
        self.signature_tab = ttk.Frame(self.tab_control)  # Pestaña para firma y verificación

        # Añadir las pestañas al control de pestañas
        self.tab_control.add(self.dh_tab, text="Claves DH")
        self.tab_control.add(self.cipher_tab, text="Cifrar/Descifrar")
        self.tab_control.add(self.signature_tab, text="Firmar/Verificar")
        self.tab_control.pack(expand=1, fill="both")

        # Configurar las funcionalidades de cada pestaña
        self.setup_dh_tab()
        self.setup_cipher_tab()
        self.setup_signature_tab()

    def setup_dh_tab(self):
        """
        Configura la pestaña para la generación de claves y parámetros Diffie-Hellman (DH).
        """
        label = tk.Label(self.dh_tab, text="Generar Claves DH", font=("Arial", 16))
        label.pack(pady=10)

        # Botones para las distintas funcionalidades DH
        generate_params_btn = tk.Button(self.dh_tab, text="Generar Parámetros DH", command=self.generate_dh_parameters)
        generate_params_btn.pack(pady=10)

        generate_keys_btn = tk.Button(self.dh_tab, text="Generar Claves DH", command=self.generate_dh_keys)
        generate_keys_btn.pack(pady=10)

        calculate_shared_btn = tk.Button(self.dh_tab, text="Calcular Clave Compartida", command=self.calculate_shared_key)
        calculate_shared_btn.pack(pady=10)

        # Etiqueta para mostrar el estado de las operaciones
        self.dh_status = tk.Label(self.dh_tab, text="", fg="green")
        self.dh_status.pack(pady=5)

    def setup_cipher_tab(self):
        """
        Configura la pestaña para cifrar y descifrar archivos.
        """
        label = tk.Label(self.cipher_tab, text="Cifrar/Descifrar Archivos", font=("Arial", 16))
        label.pack(pady=10)

        # Botón para cifrar un archivo
        encrypt_btn = tk.Button(self.cipher_tab, text="Cifrar Archivo", command=self.encrypt_file)
        encrypt_btn.pack(pady=10)

        # Botón para descifrar un archivo
        decrypt_btn = tk.Button(self.cipher_tab, text="Descifrar Archivo", command=self.decrypt_file)
        decrypt_btn.pack(pady=10)

        # Etiqueta para mostrar el estado de las operaciones
        self.cipher_status = tk.Label(self.cipher_tab, text="", fg="green")
        self.cipher_status.pack(pady=5)

    def setup_signature_tab(self):
        """
        Configura la pestaña para la firma y verificación de archivos.
        """
        label = tk.Label(self.signature_tab, text="Firmar y Verificar Archivos", font=("Arial", 16))
        label.pack(pady=10)

        # **Sección para firmar archivos**
        sign_file_frame = tk.Frame(self.signature_tab)
        sign_file_frame.pack(pady=10)

        tk.Label(sign_file_frame, text="Archivo a firmar:").grid(row=0, column=0, padx=5, pady=5)
        self.sign_file_path = tk.Entry(sign_file_frame, width=50)
        self.sign_file_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(sign_file_frame, text="Seleccionar", command=self.select_sign_file).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(sign_file_frame, text="Clave privada RSA:").grid(row=1, column=0, padx=5, pady=5)
        self.sign_private_key_path = tk.Entry(sign_file_frame, width=50)
        self.sign_private_key_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(sign_file_frame, text="Seleccionar", command=self.select_sign_private_key).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(sign_file_frame, text="Firmar Archivo", command=self.sign_file).grid(row=2, column=1, pady=10)

        # **Sección para verificar firmas**
        verify_file_frame = tk.Frame(self.signature_tab)
        verify_file_frame.pack(pady=10)

        tk.Label(verify_file_frame, text="Archivo a verificar:").grid(row=0, column=0, padx=5, pady=5)
        self.verify_file_path = tk.Entry(verify_file_frame, width=50)
        self.verify_file_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(verify_file_frame, text="Seleccionar", command=self.select_verify_file).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(verify_file_frame, text="Archivo de firma:").grid(row=1, column=0, padx=5, pady=5)
        self.verify_signature_path = tk.Entry(verify_file_frame, width=50)
        self.verify_signature_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(verify_file_frame, text="Seleccionar", command=self.select_verify_signature).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(verify_file_frame, text="Clave pública RSA:").grid(row=2, column=0, padx=5, pady=5)
        self.verify_public_key_path = tk.Entry(verify_file_frame, width=50)
        self.verify_public_key_path.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(verify_file_frame, text="Seleccionar", command=self.select_verify_public_key).grid(row=2, column=2, padx=5, pady=5)

        tk.Button(verify_file_frame, text="Verificar Firma", command=self.verify_signature).grid(row=3, column=1, pady=10)

        self.signature_status = tk.Label(self.signature_tab, text="", fg="green")
        self.signature_status.pack(pady=5)

    def select_sign_file(self):
        """
        Permite al usuario seleccionar un archivo para firmar.
        """
        path = filedialog.askopenfilename(title="Seleccionar archivo para firmar")
        if path:
            self.sign_file_path.delete(0, tk.END)
            self.sign_file_path.insert(0, path)

    def select_sign_private_key(self):
        """
        Permite al usuario seleccionar una clave privada para firmar un archivo.
        """
        path = filedialog.askopenfilename(title="Seleccionar clave privada RSA para firmar")
        if path:
            self.sign_private_key_path.delete(0, tk.END)
            self.sign_private_key_path.insert(0, path)

    def select_verify_file(self):
        """
        Permite al usuario seleccionar un archivo para verificar.
        """
        path = filedialog.askopenfilename(title="Seleccionar archivo para verificar")
        if path:
            self.verify_file_path.delete(0, tk.END)
            self.verify_file_path.insert(0, path)

    def select_verify_signature(self):
        """
        Permite al usuario seleccionar un archivo de firma.
        """
        path = filedialog.askopenfilename(title="Seleccionar archivo de firma (signature.dat)")
        if path:
            self.verify_signature_path.delete(0, tk.END)
            self.verify_signature_path.insert(0, path)

    def select_verify_public_key(self):
        """
        Permite al usuario seleccionar una clave pública para verificar una firma.
        """
        path = filedialog.askopenfilename(title="Seleccionar clave pública RSA (RSA_pub.pem)")
        if path:
            self.verify_public_key_path.delete(0, tk.END)
            self.verify_public_key_path.insert(0, path)

    def generate_dh_parameters(self):
        """
        Genera y guarda parámetros Diffie-Hellman (DH) en un archivo.
        """
        try:
            parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
            param_bytes = parameters.parameter_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.ParameterFormat.PKCS3
            )
            save_to_file(param_bytes, "DH_parameters.pem")
            self.dh_status.config(text="Parámetros DH generados y guardados como 'DH_parameters.pem'.")
        except Exception as e:
            self.dh_status.config(text=f"Error al generar parámetros: {str(e)}", fg="red")

    def generate_dh_keys(self):
        """
        Genera claves públicas y privadas DH a partir de parámetros seleccionados por el usuario.
        """
        param_path = filedialog.askopenfilename(title="Seleccionar parámetros DH (DH_parameters.pem)")
        if not param_path:
            self.dh_status.config(text="No se seleccionaron parámetros DH.", fg="red")
            return

        try:
            with open(param_path, "rb") as f:
                parameters = serialization.load_pem_parameters(f.read(), backend=default_backend())

            private_key = parameters.generate_private_key()
            public_key = private_key.public_key()

            # Pedir identificador para las claves
            key_name = simpledialog.askstring("Nombre de Claves", "Ingrese un identificador para las claves (e.g., 'usuario1'):")
            if not key_name:
                self.dh_status.config(text="Operación cancelada. No se generaron claves.", fg="red")
                return

            # Guardar claves
            private_filename = f"DH_priv_{key_name}.pem"
            public_filename = f"DH_pub_{key_name}.pem"
            private_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            save_to_file(private_bytes, private_filename)
            save_to_file(public_bytes, public_filename)

            self.dh_status.config(text=f"Claves DH generadas y guardadas como '{private_filename}' y '{public_filename}'.")
        except Exception as e:
            self.dh_status.config(text=f"Error al generar claves: {str(e)}", fg="red")

    def calculate_shared_key(self):
        """
        Calcula una clave compartida utilizando Diffie-Hellman.
        """
        try:
            # Selección de la clave privada propia
            private_key_path = filedialog.askopenfilename(title="Seleccionar clave privada propia (DH_priv_X.pem)")
            if not private_key_path:
                self.dh_status.config(text="No se seleccionó una clave privada.", fg="red")
                return

            # Selección de la clave pública de la otra parte
            public_key_path = filedialog.askopenfilename(title="Seleccionar clave pública de la otra parte (DH_pub_X.pem)")
            if not public_key_path:
                self.dh_status.config(text="No se seleccionó una clave pública.", fg="red")
                return

            private_key = serialization.load_pem_private_key(load_from_file(private_key_path), password=None)
            peer_public_key = serialization.load_pem_public_key(load_from_file(public_key_path))

            # Cálculo de la clave compartida
            shared_key = private_key.exchange(peer_public_key)

            # Derivar clave AES a partir de la clave compartida
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,  # AES 256 bits
                salt=None,
                info=b'DH shared key',
                backend=default_backend()
            ).derive(shared_key)

            save_to_file(derived_key, "shared_key.bin")
            self.dh_status.config(text="Clave compartida generada y guardada correctamente.")

        except Exception as e:
            self.dh_status.config(text=f"Error al calcular la clave compartida: {str(e)}", fg="red")

    def encrypt_file(self):
        """
        Cifra un archivo utilizando AES con una clave compartida.
        """
        file_path = filedialog.askopenfilename(title="Seleccionar archivo a cifrar")
        if not file_path:
            return

        shared_key_path = filedialog.askopenfilename(title="Seleccionar clave compartida (shared_key.bin)")
        if not shared_key_path:
            messagebox.showerror("Error", "No se seleccionó una clave compartida.")
            return

        try:
            shared_key = load_from_file(shared_key_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la clave compartida seleccionada.")
            return

        # Archivo cifrado
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        plaintext_padded = pad_data(plaintext)

        iv = secrets.token_bytes(16)
        cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()

        # Guarda archivo cifrado y vector (IV)
        save_to_file(ciphertext, "archivo_cifrado.dat")
        save_to_file(iv, "iv.dat")

        self.cipher_status.config(text="Archivo cifrado y guardado como 'archivo_cifrado.dat'.")

    def decrypt_file(self):
        """
        Descifra un archivo previamente cifrado utilizando AES con una clave compartida.
        """
        file_path = filedialog.askopenfilename(title="Seleccionar archivo a descifrar")
        if not file_path:
            return

        shared_key_path = filedialog.askopenfilename(title="Seleccionar clave compartida (shared_key.bin)")
        if not shared_key_path:
            messagebox.showerror("Error", "No se seleccionó una clave compartida.")
            return

        try:
            shared_key = load_from_file(shared_key_path)
            iv = load_from_file("iv.dat")  # Se carga el IV necesario para el descifrado
        except FileNotFoundError:
            messagebox.showerror("Error", "Faltan archivos necesarios para descifrar.")
            return

        # Leer el archivo cifrado
        with open(file_path, 'rb') as f:
            ciphertext = f.read()

        # Configurar el objeto de descifrado con la clave compartida y el IV
        cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Eliminar el relleno del texto plano
        plaintext = unpad_data(plaintext_padded)

        # Guardar el archivo descifrado
        save_to_file(plaintext, "archivo_descifrado.txt")
        self.cipher_status.config(text="Archivo descifrado y guardado como 'archivo_descifrado.txt'.")

    def sign_file(self):
        """
        Firma un archivo utilizando una clave privada RSA.
        """
        file_path = self.sign_file_path.get()
        private_key_path = self.sign_private_key_path.get()

        if not file_path or not private_key_path:
            messagebox.showerror("Error", "Debe seleccionar un archivo y una clave privada para firmar.")
            return

        try:
            private_key = serialization.load_pem_private_key(load_from_file(private_key_path), password=None)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la clave privada RSA seleccionada.")
            return

        # Leer los datos del archivo
        with open(file_path, 'rb') as f:
            data = f.read()

        # Generar la firma digital
        signature = private_key.sign(
            data,
            PKCS1v15(),
            hashes.SHA256()
        )

        # Guardar la firma en un archivo
        save_to_file(signature, "firma.dat")
        self.signature_status.config(text="Firma digital generada y guardada como 'firma.dat'.")

    def verify_signature(self):
        """
        Verifica la firma digital de un archivo utilizando una clave pública RSA.
        """
        file_path = self.verify_file_path.get()
        signature_path = self.verify_signature_path.get()
        public_key_path = self.verify_public_key_path.get()

        if not file_path or not signature_path or not public_key_path:
            messagebox.showerror("Error", "Debe seleccionar el archivo, la firma y la clave pública para verificar.")
            return

        try:
            public_key = serialization.load_pem_public_key(load_from_file(public_key_path))
            signature = load_from_file(signature_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "Faltan archivos necesarios para verificar la firma.")
            return

        # Leer los datos del archivo
        with open(file_path, 'rb') as f:
            data = f.read()

        try:
            # Verificar la firma digital
            public_key.verify(
                signature,
                data,
                PKCS1v15(),
                hashes.SHA256()
            )
            self.signature_status.config(text="Firma verificada exitosamente.")
        except Exception as e:
            self.signature_status.config(text="La firma no es válida.", fg="red")


# Ejecutar la aplicación gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptographyApp(root)
    root.mainloop()