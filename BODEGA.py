import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sqlite3

class FormularioProductos:
    def __init__(self):
        self.conexion = sqlite3.connect("C:/Users/PC20-A06-SC/Desktop/nnn/formulario_tinda/productos.db")

        self.ventana = tk.Tk()
        self.ventana.title("Formulario de Productos")

        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.presentacion_var = tk.StringVar()
        self.fecha_vencimiento_var = tk.StringVar()
        self.laboratorio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()

        self.crear_widgets()
        self.ventana.mainloop()

    def crear_widgets(self):
        ttk.Label(self.ventana, text="Código del Producto:").grid(column=0, row=0, padx=10, pady=10)
        self.codigo_entry = ttk.Entry(self.ventana, textvariable=self.codigo_var)
        self.codigo_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.ventana, text="Nombre del Producto:").grid(column=0, row=1, padx=10, pady=10)
        ttk.Entry(self.ventana, textvariable=self.nombre_var).grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(self.ventana, text="Presentación:").grid(column=0, row=2, padx=10, pady=10)
        ttk.Entry(self.ventana, textvariable=self.presentacion_var).grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(self.ventana, text="Fecha de Vencimiento:").grid(column=0, row=3, padx=10, pady=10)
        ttk.Entry(self.ventana, textvariable=self.fecha_vencimiento_var).grid(column=1, row=3, padx=10, pady=10)

        ttk.Label(self.ventana, text="Laboratorio:").grid(column=0, row=4, padx=10, pady=10)
        ttk.Entry(self.ventana, textvariable=self.laboratorio_var).grid(column=1, row=4, padx=10, pady=10)

        ttk.Label(self.ventana, text="Cantidad en Bodega:").grid(column=0, row=5, padx=10, pady=10)
        ttk.Entry(self.ventana, textvariable=self.cantidad_var).grid(column=1, row=5, padx=10, pady=10)

        # Frame para centrar los botones
        button_frame = tk.Frame(self.ventana)
        button_frame.grid(column=1, row=6, padx=10, pady=10)

        self.boton_guardar = ttk.Button(button_frame, text="Guardar", command=self.guardar)
        self.boton_guardar.pack(side="left", padx=5)

        ttk.Button(button_frame, text="Buscar", command=self.buscar).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Mostrar Registros", command=self.mostrar_todos).pack(side="left", padx=5)

    def mostrar_todos(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM PRODUCTOS")
            productos = cursor.fetchall()

            if not productos:
                mb.showinfo("Información", "No hay productos en la base de datos.")
                return

            # Crear una nueva ventana para mostrar los productos
            ventana_productos = tk.Toplevel(self.ventana)
            ventana_productos.title("Lista de Productos")

            tree = ttk.Treeview(ventana_productos, columns=("Código", "Nombre", "Presentación", "Fecha de Vencimiento", "Laboratorio", "Cantidad"), show='headings')
            tree.heading("Código", text="Código")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Presentación", text="Presentación")
            tree.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
            tree.heading("Laboratorio", text="Laboratorio")
            tree.heading("Cantidad", text="Cantidad")

            for producto in productos:
                tree.insert("", tk.END, values=producto)

            tree.pack(expand=True, fill='both')

            # Añadir un botón para cerrar la ventana de productos
            ttk.Button(ventana_productos, text="Cerrar", command=ventana_productos.destroy).pack(pady=10)

        except sqlite3.OperationalError as e:
            mb.showerror("Error", f"Error al recuperar los datos: {e}")

    def guardar(self):
        codigo = self.codigo_var.get()
        nombre = self.nombre_var.get()
        presentacion = self.presentacion_var.get()
        fecha_vencimiento = self.fecha_vencimiento_var.get()
        laboratorio = self.laboratorio_var.get()
        cantidad = self.cantidad_var.get()

        if not codigo or not nombre or not presentacion or not fecha_vencimiento or not laboratorio or not cantidad:
            mb.showwarning("Advertencia", "Por favor complete todos los campos.")
            return

        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM PRODUCTOS WHERE CODIGO_PRODUCTO=?", (codigo,))
            producto = cursor.fetchone()

            if producto:
                mb.showwarning("Advertencia", "El código de producto ya existe en la base de datos.")
            else:
                cursor.execute("INSERT INTO PRODUCTOS (CODIGO_PRODUCTO, NOMBRE_PRODUCTO, PRESENTACION, FECHA_VENCIMIENTO, LABORATORIO, CANTIDAD_EN_BODEGA) VALUES (?, ?, ?, ?, ?, ?)",
                               (codigo, nombre, presentacion, fecha_vencimiento, laboratorio, cantidad))
                self.conexion.commit()

                mb.showinfo("Información", "Datos guardados exitosamente.")
                self.limpiar_campos()
        except sqlite3.OperationalError as e:
            mb.showerror("Error", f"Error al guardar los datos: {e}")

    def buscar(self):
        self.boton_guardar.config(state=tk.DISABLED)  # Desactivar el botón "Guardar"
        
        codigo = self.codigo_var.get()
        if not codigo:
            mb.showwarning("Advertencia", "Por favor ingrese el código del producto.")
            self.boton_guardar.config(state=tk.NORMAL)  # Reactivar el botón "Guardar"
            return

        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM PRODUCTOS WHERE CODIGO_PRODUCTO=?", (codigo,))
            producto = cursor.fetchone()

            if producto:
                self.nombre_var.set(producto[1])
                self.presentacion_var.set(producto[2])
                self.fecha_vencimiento_var.set(producto[3])
                self.laboratorio_var.set(producto[4])
                self.cantidad_var.set(producto[5])
                mb.showinfo("Información", "Producto encontrado.")
                
                # Bloquear el campo de código
                self.codigo_entry.config(state=tk.DISABLED)
            else:
                mb.showwarning("Advertencia", "No se encontró ningún producto con ese código.")
                self.limpiar_campos()
        except sqlite3.OperationalError as e:
            mb.showerror("Error", f"Error al buscar los datos: {e}")
        finally:
            self.boton_guardar.config(state=tk.NORMAL)  # Reactivar el botón "Guardar"

    def eliminar(self):
        codigo = self.codigo_var.get()
        
        if not codigo:
            mb.showwarning("Advertencia", "Por favor ingrese el código del producto a eliminar.")
            return

        respuesta = mb.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar este producto?")
        if respuesta:
            try:
                cursor = self.conexion.cursor()
                cursor.execute("DELETE FROM PRODUCTOS WHERE CODIGO_PRODUCTO=?", (codigo,))
                if cursor.rowcount > 0:
                    self.conexion.commit()
                    mb.showinfo("Información", "Producto eliminado exitosamente.")
                    self.limpiar_campos()
                else:
                    mb.showwarning("Advertencia", "No se encontró ningún producto con ese código.")
            except sqlite3.OperationalError as e:
                mb.showerror("Error", f"Error al eliminar los datos: {e}")

    def limpiar_campos(self):
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.presentacion_var.set("")
        self.fecha_vencimiento_var.set("")
        self.laboratorio_var.set("")
        self.cantidad_var.set("")
        self.codigo_entry.config(state=tk.NORMAL)  # Habilitar el campo de código

    def __del__(self):
        self.conexion.close()

# Inicializar la aplicación
if __name__ == "__main__":
    FormularioProductos()

