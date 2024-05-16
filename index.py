from tkinter import ttk
from tkinter import * 

import sqlite3



class product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('products aplication')

        #CONECTAR UN FRAME CONTAINER
        Frame = LabelFrame(self.wind, text="registra Nuevo Producto")
        Frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Entrada de Nombre
        Label(Frame, text="Nombre: ").grid(row=1,column=0)
        self.name = Entry(Frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
    
        #PRECIO
        Label(Frame,text="Precio").grid(row=2,column=0)
        self.price = Entry(Frame)
        self.price.grid(row= 2, column=1)
    
        #Boton Agregar Producto 

        ttk.Button(Frame, text="guardar Producto", command=self.add_product).grid(row = 3 , columnspan = 2 , sticky = W + E)

        #MENSAJE DEL BOTON
        self.message = Label(text= '', fg='red')
        self.message.grid(row=3, column=0, columnspan= 2, sticky= W + E )

        #TABLA
        self.tree = ttk.Treeview(height=10, columns=2,)
        self.tree.grid(row=4, column = 0, columnspan= 2)
        self.tree.heading("#0", text="nombre", anchor= CENTER)
        self.tree.heading("#1", text="precio", anchor=CENTER)

       #BOTONES
        ttk.Button(text='Eliminar', command=self.delete_product).grid(row=5,column=0, sticky=W+E)
        ttk.Button(text='Actualizar',command=self.edit_product).grid(row=5, column=1, sticky=W+E)
       
        #RELLENAR LAS FILAS DE LA TABLA
        self.get_products()

    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            results = cursor.execute(query,parameters,)
            conn.commit()
            return results
    
    def get_products(self):
       #limpiando la tabla
       records = self.tree.get_children()
       for element in records:
           self.tree.delete(element)
        #CONSULTA
       query =  '''SELECT * FROM products ORDER BY price DESC'''
       db_rows = self.run_query(query)
       for row in db_rows:
            self.tree.insert('',0,text=row[1], values=row[2])


    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = '''INSERT INTO products VALUES(NULL, ?,?)'''
            parameters = (self.name.get(), self.price.get())
            self.run_query(query,parameters)
            self.message['text'] = 'producto {} Agregado Exitosamente '.format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
            self.get_products()
        else:
            self.message['text'] = 'Nombre y Precio Son Requeridos'
            self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = "Elija un Producto"
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM products WHERE name = ?'
        self.run_query(query,(name,))
        self.message['text'] = ' el {} Eliminado Exitosamente'.format(name)
        self.get_products()
        
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = "Elija un Producto"
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price  = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'


        #NOMBRE VIEJO
        Label(self.edit_wind, text="Nombre Viejo: ").grid(row=0,column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row=0, column = 2)


        #NOMBRE NUEVO
        Label(self.edit_wind, text= 'Nuevo Nombre').grid(row=1, column= 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)


        #PRECIO VIEJO
        Label(self.edit_wind, text='Precio Antiguo').grid(row=2, column =2)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row=2,column=2)


        #PRECIO NUEVO
        Label(self.edit_wind, text='Nuevo Precio').grid(row=3,column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3,column=2)

        Button(self.edit_wind, text='Editar', command= lambda: self.edit_records( new_name.get() , name , new_price.get() , old_price )).grid(row=4, column=2,sticky=W)


    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = '{} Se Actualizó Correctamente'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    aplication = product(window)
    window.mainloop()