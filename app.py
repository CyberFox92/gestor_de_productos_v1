from tkinter import ttk
from tkinter import *
import tkinter as tk
import sqlite3
from PIL import ImageTk, Image
import os

class VentanaPrincipal:
    """Funcion principal del programa, carga la ventana principal, el cuadro de registro de productos,
    la tabla de productos y los botones de accion"""

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap("recursos/icon.ico")

        #Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un producto nuevo", font=("Calibri", 16, "bold"))
        frame.grid(row=0, column=1, columnspan=4, pady=20)

        #Logo de cabecera
        nombre_logo ="Logo_py"
        logo = self.get_imagen(self.ventana, nombre_logo, 140  )
        logo.grid(row=0, column=0)

        #Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=("Calibri", 13))
        self.etiqueta_nombre.grid(row=1, column=0)

        #Entry Nombre
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio=Label(frame, text="Precio: ", font=("Calibri", 13))
        self.etiqueta_precio.grid(row=2, column=0)

        #Entry Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ", font=("Calibri", 13))
        self.etiqueta_categoria.grid(row=1, column=2)

        #Entry Categoria
        self.categoria = Entry(frame)
        self.categoria.grid(row=1, column=3)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=("Calibri", 13))
        self.etiqueta_stock.grid(row=2, column=2)

        # Entry Stock
        self.stock = Entry(frame)
        self.stock.grid(row=2, column=3)

        # Label detalle
        self.etiqueta_stock = Label(frame, text="Puedes agregar detalles al producto desde la ventana Editar.", font=("Calibri", 13))
        self.etiqueta_stock.grid(row=3, columnspan=4)

        #Boton Aniadir Producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto)
        self.boton_aniadir.grid(row=4, columnspan=4, sticky=W+E)

        #Radiokbuttons, filtra stock
        self.filtro = tk.IntVar()
        self.filtro.set(0)
        self.boton_stock_completo = tk.Radiobutton(self.ventana, text="Todos los articulos",
                                                   variable = self.filtro, value=0, command=self.aplicar_filtro)
        self.boton_stock_completo.grid(row=4, column=0)

        self.boton_solo_stock = tk.Radiobutton(self.ventana, text="Articulos con stock",
                                               variable = self.filtro, value=1, command=self.aplicar_filtro)
        self.boton_solo_stock.grid(row=4, column=1)

        self.boton_sin_stock = tk.Radiobutton(self.ventana, text="Articulos sin stock",
                                              variable = self.filtro, value=2, command=self.aplicar_filtro)
        self.boton_sin_stock.grid(row=4, column=2)

        # Botones de detalles editar y eliminar
        self.boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto)
        self.boton_eliminar.grid(row=6, column=0, columnspan=1, sticky=W+E, ipadx=100)
        self.boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto)
        self.boton_editar.grid(row=6, column=1, columnspan=1, sticky=W+E,ipadx=100)
        self.boton_detalles = ttk.Button(text="DETALLES", command=self.mostrar_detalles)
        self.boton_detalles.grid(row=6, column=2, columnspan=1, sticky=W+E, ipadx=100)

        #Mensaje para el usuario
        self.mensaje = Label(text="", font=("Calibri", 12), fg="red")
        self.mensaje.grid(row=3, column=0, columnspan=4, sticky=W + E)

        #Tabla Productos

        #Estilo para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=("Calibri", 12))
        style.configure("mystyle.Treeview.Heading",
                        font=("Calibri", 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky":"nswe"})])

        #Estructura de tabla
        self.tabla = ttk.Treeview(height=17, columns=("nombre", "precio", "categoria", "stock"), style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=4)
        self.tabla.heading("#0", text="", anchor=CENTER)
        self.tabla.column("#0", width=0, stretch=NO)
        self.tabla.heading("nombre", text="Nombre", anchor=CENTER)
        self.tabla.heading("precio", text="Precio", anchor=CENTER)
        self.tabla.heading("categoria", text="Categoria", anchor=CENTER)
        self.tabla.heading("stock", text="Stock", anchor=CENTER)

        self.get_productos()

    def aplicar_filtro(self):
        """Funcion que filtra que RadioButton esta selexxionado y pasa el valor a la funcion correspondiente"""

        if self.filtro.get() == 0:
            self.get_productos()
        elif self.filtro.get() == 1:
            self.get_con_stock()
        elif self.filtro.get() == 2:
            self.get_sin_stock()


    def db_consulta(self, consulta, parametros = ()):
        """Funcion principal para las consultas a la bd. Recibe la consulta y los parametros de la misma"""

        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        """Funcion que sirve para consultar la tabla productos de la BD, recuperas todas las entradad y los agrega a
        la tabla de la app en orden asc por id para que se muestre arriba el ultimo producto agregado"""
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = "SELECT * FROM producto ORDER BY id ASC"
        registros_db = self.db_consulta(query)
        for fila in registros_db:
            print(fila)
            self.tabla.insert("",0, values=fila[1:])

    def get_con_stock(self):
        '''Funcion que sirve para consultar la tabla de BD, devuelve aquellos productos con stock disponiblelos
        y los agrega a la tabla de la  app en orden asc por id para que se muestre arriba el ultimo producto agregado'''
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = "SELECT * FROM producto WHERE stock > 0 ORDER BY id ASC"
        registros_db = self.db_consulta(query)
        for fila in registros_db:
            print(fila)
            self.tabla.insert("",0, values=fila[1:])

    def get_sin_stock(self):
        '''Funcion que sirve para consultar la tabla de BD, devuelve aquellos que no cuentan con stock disponible
        los agrega a la tabla de la app en orden asc por id para que se muestre arriba el ultimo producto agregado'''
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = "SELECT * FROM producto WHERE stock = 0 ORDER BY id ASC"
        registros_db = self.db_consulta(query)
        for fila in registros_db:
            print(fila)
            self.tabla.insert("",0, values=fila[1:])

    def validacion_nombre(self):
        """Funcion que valida si el campo de nombre esta vacio, devuelve un booleano"""
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        """Funcion que valida si el campo de precio es valido, este debe ser mayor a 0 y deben ser numeros
         devuelve un booleano"""

        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def validacion_categoria(self):
        """Funcion que valida si el campo categoria esta vacio, devuelve un booleano"""

        return self.categoria.get().strip() != ""

    def validacion_stock(self):
        """Funcion que valida que la cantidad de stock ingresada en dicho campo sea un numero igual a 0 o
        positivo, devuleve un booleano"""
        try:
            stock = float(self.stock.get())
            return stock >= 0
        except ValueError:
            return False

    def add_producto(self):
        """Funcion que sirve para agregarun nuevo producto en la base de datos. Implementa comprobaciones de datos
        usando otras funciones para asegurar que los datos ingresados son validos"""
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es un campo obligatorio, no puede estar vacio."
            return
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es un campo obligatorio y debe ser un numero valido mayor a 0."
            return
        if not self.validacion_categoria():
            print("La categoria es obligatoria")
            self.mensaje["text"] = "La categoria es un campo obligatorio, no puede estar vacio."
            return
        if not self.validacion_stock():
            print("El stock es obligatorio")
            self.mensaje["text"] = "El stock es un campo obligatorio y debe ser un numero igual o mayor a 0"

        self.detail = ""
        query = "INSERT INTO producto VALUES(NULL,?,?,?,?,?)"
        parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get(), self.detail)
        self.db_consulta(query, parametros)
        print("Los datos se han guardado con exito.")
        self.mensaje["text"] = f"Producto {self.nombre.get()} agregado con exito."
        self.nombre.delete(0,END)
        self.precio.delete(0, END)
        self.categoria.delete(0, END)
        self.stock.delete(0, END)
        self.get_productos()

    def del_producto(self):
        """Funcion que sirve para la implementacion del boton eliminar. Elimina de la tabla de la app y de la
        BD el elemento seleccionado"""
        self.mensaje["text"] = ""
        item = self.tabla.item(self.tabla.selection())
        valores = item["values"]
        nombre = valores[0]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "El producto {} se ha eliminado con exito!.".format(nombre)
        self.get_productos()

    def edit_producto(self):
        """Funcion que sirve para la implementacion del boton editar. Abre una nueva ventana donde permite al usuario
        reingresar datos nuevos o que permanezcan los ya existentes"""
        try:
            item = self.tabla.item(self.tabla.selection())
            valores = item["values"]
            nombre = valores[0]
            precio = valores[1]
            categoria = valores[2]
            stock = valores[3]
            detalle = valores[4]
            VentanaEditarProducto(self, nombre, precio, categoria, stock, detalle, self.mensaje)
        except IndexError:
            self.mensaje["text"] = "Por favor, seleccionar un producto"

    def mostrar_detalles(self):
        """Funcion que sirve para la implementacion del boton detalles. Abre una ventana nueva donde muestra en
        detalle el nombre del articulo, el precio, el apartado detalle (si lo tiene ingresado) y una imagen del producto"""
        try:
            item = self.tabla.item(self.tabla.selection())
            valores = item["values"]
            nombre = valores[0]
            precio = valores[1]
            detalle = valores[4]

            VentanaDetalles(self.ventana, nombre, precio, detalle)

        except IndexError:
            self.mensaje["text"] = "Por favor, seleccionar un producto"

    def get_imagen(self, donde, nombre, ancho_base):
        """Funcion echa para poder renderizar en pantalla cualquier imagen .PNG que este guardada en la carpeta
        recursos. Solo se le pasa donde se ejecutara (en que ventana), el nombre de la imagen sin su extencion (debe
        ser una imagen con extencion .png, de lo contrario no la muestra) y el ancho en px que ha de ocupar la imagen.
        La funcion se encarga de tomar ese valor base, calcular el alto que deberia tener para que no se pierda la
        relacion de aspecto de la imagen y la devuleve como un Label. Implmente excepciones para que no falle la ejecucion
        si falla la imagen (por formato o ruta) o algun atributo"""

        try:
            self.nombre = nombre
            self.donde = donde
            self.ancho_base = ancho_base
            ruta_imagen = os.path.join("recursos/", self.nombre + ".png")
            imagen_pil = Image.open(ruta_imagen)
            porcentaje_tamanio = (ancho_base / float(imagen_pil.size[0]))
            alto_final = int((float(imagen_pil.size[1]) * float(porcentaje_tamanio)))
            tamanio = ancho_base, alto_final
            resized_image = imagen_pil.resize(tamanio, Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(resized_image)
            etiqueta = tk.Label(donde)
            etiqueta.config(image=imagen_tk)
            etiqueta.image = imagen_tk
            return etiqueta

        except FileNotFoundError:
            return "No se encuentra imagen para este producto"

        except AttributeError:
            pass

class VentanaEditarProducto:
    """Ventana que se abre al usar el boton editar. Permite cambiar o mantener datos previamente creados y agregar
    detalles al articulo seleccionado"""

    def __init__(self, ventana_principal, nombre, precio, categoria, stock, detalle, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.detalle = detalle
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.wm_iconbitmap("recursos/icon.ico")

        #Contenedor frame para la edicion de productos
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=("Calibri", 16, "bold"))
        frame_ep.grid(row=0, column=0, columnspan=4, pady=20, padx=20)

        #Label y Entry para nombre antiguo SOLO LECTURA
        Label(frame_ep, text="Nombre antiguo ",font=("Calibri", 13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=self.nombre),
              state="readonly", font=("Calibri", 13)).grid(row=1, column=1)

        #Label y Entry para el nombre nuevo
        Label(frame_ep, text="Nombre nuevo ", font=("Calibri", 13)).grid(row=1, column=2)
        self.input_nombre_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_nombre_nuevo.grid(row=1, column=3)
        self.input_nombre_nuevo.focus()

        #Label y Entry para precio antiguo SOLO LECTURA
        Label(frame_ep, text="Precio antiguo ",font=("Calibri", 13)).grid(row=2, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=self.precio),
              state="readonly", font=("Calibri", 13)).grid(row=2, column=1)

        # Label y Entry para el precio nuevo
        Label(frame_ep, text="Precio nuevo ", font=("Calibri", 13)).grid(row=2, column=2)
        self.input_precio_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_precio_nuevo.grid(row=2, column=3)

        # Label y Entry para categoria antiguo SOLO LECTURA
        Label(frame_ep, text="Categoria antigua ", font=("Calibri", 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=self.categoria),
              state="readonly", font=("Calibri", 13)).grid(row=3, column=1)

        # Label y Entry para la categoria nueva
        Label(frame_ep, text="Categoria nuevo ", font=("Calibri", 13)).grid(row=3, column=2)
        self.input_categoria_nueva = Entry(frame_ep, font=("Calibri", 13))
        self.input_categoria_nueva.grid(row=3, column=3)

        # Label y Entry para stock antiguo SOLO LECTURA
        Label(frame_ep, text="Stock antiguo ", font=("Calibri", 13)).grid(row=4, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=self.stock),
              state="readonly", font=("Calibri", 13)).grid(row=4, column=1)

        # Label y Entry para el stock nuevo
        Label(frame_ep, text="Stock nuevo ", font=("Calibri", 13)).grid(row=4, column=2)
        self.input_stock_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_stock_nuevo.grid(row=4, column=3)

        #Label y Entry para detalle antiguo SOLO LECTURA
        Label(frame_ep, text="Detalle antiguo ", font=("Calibri", 13)).grid(row=5, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=self.detalle),
              state="readonly", font=("Calibri", 13)).grid(row=5, column=1)

        # Label y Entry para el detalle nuevo
        Label(frame_ep, text="Detalle nuevo ", font=("Calibri", 13)).grid(row=5, column=2)
        self.input_detalle_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_detalle_nuevo.grid(row=5, column=3)

        #Boton Actualizar Producto

        ttk.Style().configure("my.TButton", font=("Calibri", 14, "bold"))

        #Creacion del estilo para nuestro boton en una sola linea

        ttk.Button(frame_ep, text="Actualizar Producto",
                   style="my.TButton", command=self.actualizar).grid(row=6, column=1, columnspan=2, sticky=W+E)
    def actualizar(self):
        """Funcion que evalua y actualiza de ser necesario los datos ingresados en la ventana de editar producto. Si
        el campo en cuestion queda en blanco o no sufre cambios queda como estaba, al finalizar muestra un resumen
        unicamente con los cambios realizados"""
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        nueva_categoria = self.input_categoria_nueva.get() or self.categoria
        nuevo_stock = self.input_stock_nuevo.get() or self.stock
        nuevo_detalle = self.input_detalle_nuevo.get() or self.detalles

        query = "UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ?, detalles = ? WHERE nombre = ?"
        parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, nuevo_detalle, self.nombre)
        self.ventana_principal.db_consulta(query, parametros)

        cambios_realizados = []
        if nuevo_nombre != self.nombre:
            cambios_realizados.append("Nombre")
        if nuevo_precio != self.precio:
            cambios_realizados.append("Precio")
        if nueva_categoria != self.categoria:
            cambios_realizados.append("Categoría")
        if nuevo_stock != self.stock:
            cambios_realizados.append("Stock")
        if nuevo_detalle != self.detalle:
            cambios_realizados.append("Detalles")
        if cambios_realizados:
            mensaje_cambios = ", ".join(cambios_realizados)
            self.mensaje["text"] = f"El producto {self.nombre} se ha actualizado con éxito. Cambios realizados: {mensaje_cambios}."
        else:
            self.mensaje["text"] = f"No se han realizado cambios al producto {self.nombre}."

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()
class VentanaDetalles:
    """Ventana de detalles, se abre al usar el boton detalles. Muestra una ventana nueva donde aparecen el nombre, el
    precio, el detalle (si tiene alguno) y una imagen del producto seleccionado"""
    def __init__(self, ventana_principal, nombre, precio, detalle):
        self.nombre = nombre
        self.precio = precio
        self.detalle = detalle
        self.ventana_det = Toplevel(ventana_principal)
        self.ventana_det.title("Detalles del Artículo")
        self.ventana_det.wm_iconbitmap("recursos/icon.ico")

        # Agrega etiquetas para mostrar el nombre y el precio del artículo

        self.nombre_det = Label(self.ventana_det, text=f"Nombre: {nombre}", font=("Calibri", 13)).pack()
        self.precio_det = Label(self.ventana_det, text=f"Precio: {precio}", font=("Calibri", 13, "bold")).pack()
        self.detalle_det = Label(self.ventana_det, text=f"Detalle: {detalle}", font=("Calibri", 13)).pack()

        try:
            imagen = VentanaPrincipal.get_imagen(self, donde=self.ventana_det, nombre=self.nombre, ancho_base=400)
            imagen.pack()

        except AttributeError:
            pass


if __name__ == '__main__':
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

