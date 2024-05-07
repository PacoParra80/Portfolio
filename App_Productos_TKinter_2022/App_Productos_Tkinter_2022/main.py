import tkinter
from tkinter import *
import sqlite3
from tkinter import ttk


class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana =root
        self.ventana.title("App Gestor de Productos")  #Atributo para editar el título
        self.ventana.resizable(1,1)    #Con esto la ventana se puede redimensionar. Valor por defecto
        self.ventana.wm_iconbitmap("recursos/shopping.ico")

        #Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text = "Registrar un nuevo Producto", font=('Calibri', 16, 'bold'), padx=30, labelanchor="n")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Label Nombre
        self.etiqueta_nombre = Label(frame, text = "Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)
        #Entry Nombre
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()  #El foco solo lo puede llevar un cajón de texto
        self.nombre.grid(row=1,column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=3, column=0)

        # Desplegable Categoria
        self.categoria = ttk.Combobox(frame, state="readonly", values=["Informática", "Alimentación", "Ropa", "Otros"],
                                      width=20, font="Calibri")
        self.categoria.grid(row=3, column=1)


        #Boton de Añadir Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text = "Guardar Producto", command=self.add_producto, style='my.TButton')  #En command el nombre de la funcion va sin paréntesis
        self.boton_aniadir.grid(row=4, columnspan = 2,  ipadx=60) #sticky es lo que ocupará ese botón

        self.mensaje = Label(text = "", fg = "red", anchor=CENTER)
        self.mensaje.grid(row=4, column=0, columnspan=3, sticky=W + E)

        #Tabla Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11)) # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'), foreground="dark blue") # Se modifica
        # la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Eliminamos los bordes

        #Estructura de la Tabla
        self.tabla = ttk.Treeview(frame, height = 20, columns = ("#1", "#2"), style = "mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=2)
        self.tabla.heading("#0", text = "Nombre", anchor=CENTER)
        self.tabla.heading("#1", text="Precio", anchor=CENTER)
        self.tabla.heading("#2", text="Categoría", anchor=CENTER)



        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"))


        boton_eliminar = ttk.Button(text = 'ELIMINAR', style = "my.TButton", command=self.del_producto)
        boton_eliminar.grid(row = 6, column = 0, sticky = W + E)
        boton_editar = ttk.Button(text='EDITAR', style = "my.TButton", command=self.edit_producto)
        boton_editar.grid(row = 6, column = 2, sticky = W + E)


        self.get_productos()

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:

            self.tabla.insert("", 0, text = fila[1], values= (fila[2], fila[3]))


    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0


    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducida_por_usuario = self.categoria.get()
        return len(categoria_introducida_por_usuario) != 0




    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get())
            self.db_consulta(query, parametros)

            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get())
            self.nombre.delete(0,END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END) # Borrar el campo precio del formulario
            self.categoria.set("")  # Borrar el campo categoria del formulario

        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria():

            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria()==False:

            self.mensaje["text"] = "El precio y la categoría son obligatorios"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria():

            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria()==False:

            self.mensaje["text"] = "El nombre y la categoría son obligatorios"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria()==False:

            self.mensaje["text"] = "La categoría es obligatoria"
        elif self.validacion_nombre() == False and self.validacion_precio()==False and self.validacion_categoria():

            self.mensaje["text"] = "El nombre y el precio son obligatorios"
        else:

            self.mensaje["text"] = "El nombre, precio y categoría son obligatorios"

        self.get_productos()

    def del_producto(self):

        self.mensaje['text'] = ''  # Mensaje inicialmente vacio # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]  # El precio se encuentra dentro de una lista
        old_categoria = self.tabla.item(self.tabla.selection())['values'][1]

        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto" # Titulo de la ventana
        self.ventana_editar.resizable(1, 1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.wm_iconbitmap('recursos/shopping.ico') # Icono de la ventana

        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 40, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold')) # frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)
        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text = "Nombre antiguo: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_antiguo.grid(row=2, column=0) # Posicionamiento a traves de grid
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly',
                                          font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)
        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus() # Para que el foco del raton vaya a este Entry al inicio
        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep,text="Precio antiguo: ", font=('Calibri', 13)) # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=4, column=0) # Posicionamiento a traves de grid
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly',
                                          font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)
        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)
        # Label Categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoría antigua: ", font=('Calibri', 13))
        self.etiqueta_categoria_antigua.grid(row=6, column=0)
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),state='readonly',
                                             font=('Calibri', 13))
        self.input_categoria_antigua.grid(row=6, column=1)
        # Label Categoría nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=7, column=0)
        # Entry Categoría nueva (texto que si se podra modificar)
        self.input_categoria_nueva = ttk.Combobox(frame_ep, state="readonly", values=["Informática", "Alimentación", "Ropa", "Otros"],
                                                  width=20, font="Calibri")
        self.input_categoria_nueva.grid(row=7, column=1)


        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton',
                                           command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                     self.input_nombre_antiguo.get(),
                                                                                     self.input_precio_nuevo.get(),
                                                                                     self.input_precio_antiguo.get(),
                                                                                     self.input_categoria_nueva.get(),
                                                                                     self.input_categoria_antigua.get()))
        self.boton_actualizar.grid(row=8, columnspan=2, sticky=W + E)



    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria, antigua_categoria):
        producto_modificado = False

        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ? WHERE nombre = ? AND precio = ? AND categoria = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != "":  # Si el usuario escribe nuevo nombre,nuevo precio y nueva categoria, se cambian todos
            parametros = (nuevo_nombre, nuevo_precio,nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == "": # Si el usuario deja vacio el nuevo precio y la categoria, se mantiene el precio y categoriaanterior
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == "": # Si el usuario deja vacio el nuevo nombre y categoria, se mantiene el nombre y categoria anterior
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == "": # Si el usuario deja vacia la categoria, se mantiene la categoria anterior
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != "": # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != "": # Si el usuario deja vacio el nuevo precio, se mantiene el precio anterior
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != "": # Si el usuario deja vacio el nuevo nombre y precio, se mantiene el nombre y precio anterior
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, antiguo_nombre, antiguo_precio, antigua_categoria)
            producto_modificado = True


        if(producto_modificado):
            self.db_consulta(query,parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos() # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario










if __name__ == "__main__":
    root = Tk()  #Instancia de la ventana principal
    app = Producto(root)
    root.mainloop()