'''
CHANGELOG:
    V1
        Crear las tablas de todas sus clases.
        Agregar usuarios nuevos a las tablas.
        Mostrar los usuarios existentes.
        Tiene un login en el menu principal, el cual pide un usuario y una contraseña que evalua si existen y son correctos.
    V2
        Permite agregar y mostrar contactos.
            Los contactos los agrega en la misma tabla, pero al mostrarlos, solo muestra los que fueron agregados por el usuario activo.
    V4
        Permite agregar y mostrar correos.
            Los correos tambien los guarda en la misma tabla, pero usa el mismo identificador de usuario para que no se puedan ver entre usuarios distintos.
    V5
        Nuevo acomodo de los menus!! tal como se muestra en el documento "Proyecto".
            Se agrego un atributo estado a los correos, para definir en que "Carpeta" se encuentran".
                Los estados pueden ser: "borrador","enviado","papelera","eliminado".
        Se puede buscar un correo por fecha, mediante el formato AAAA-MM-DD.
    V6
        Agregado el modulo buscar contacto, donde pide al usuario que de una lista seleccione el id de usuario, y devuelve el correo (muy util).
        Se puede buscar un correo mediante el nombre de un contacto.
        Al enviar correos, muestra un menu para seleccionar contacto existente o nuevo.
    V7
        Correccion de errores en general, mejorada indentacion y organizacion de modulos.
        Agregado el modulo eliminar contacto, elimina un solo contacto de la base de datos, usa el mismo modulo de seleccion que el enviar a.
    V8
        Al agregar un correo o cotacto, ya maneja automaticamente el ID, lo hace contando los que ya existen para ese usuario, y sumando 1.
        Permite modificar un contacto, usa la misma implementacion que el de eliminar, proimero busca el contacto y despues lo modifica.
        Se ha cambiado la implementacion del metodo buscar correo, ahora es una sola funcion dinamica, que permite seleccionar un ID para seleccionar un solo correo.
    V9
        Se pueden mover los correos entre carpetas, ya sea de uno en uno, o todos los que esten en una misma carpeta de una sola vez
        Se puede modificar un solo correo, la unica condicion es que se encuentre como borrador
        Los correos enviados pueden ser reenviados
'''

import sqlite3 # Importa las librerias para sqlite3
from datetime import datetime # Para que almacene la hora en la que se guarda un correo
import os # Para limpiar la pantalla

def cls(): # Limia la pantalla de la consola
    os.system('cls' if os.name=='nt' else 'clear') #Detecta el sistema operativo, para poder limipar la pantalla

def pause(): # Para pausar el programa despues de haber impreso algo
    input ("Presione entrar para continuar...")
    cls()

def saltoLinea(): #Da un salto de linea entre resultados
    print ("\n")

class UsuarioSoftware():
    def __init__(self):
        self.nombreUsuario = nombreUsuario
        self.coreoUsuario = coreoUsuario
        self.idUsuario = idUsuario
        self.contraseniaUsuario = contraseniaUsuario
        self.usuarioAutenticado = usuarioAutenticado # Muy util para tener control de que datos son de cada usuario

    def crearTabla(self): #Crea una tabla vacioa
        c.execute ("CREATE TABLE IF NOT EXISTS UsuarioSoftware (nombreUsuario TEXT,  coreoUsuario TEXT, idUsuario TEXT, contraseniaUsuario TEXT)") # Crea la tabla

    def agregar(self,nombreUsuario,coreoUsuario,idUsuario,contraseniaUsuario): #Agrega los valores dados a la tabla
        c.execute ("INSERT INTO UsuarioSoftware (nombreUsuario, coreoUsuario, idUsuario, contraseniaUsuario) VALUES (?,?,?,?)", (nombreUsuario,coreoUsuario,idUsuario,contraseniaUsuario))

    def mostrar(self): #Muestra TODOS los usuarios que existen en la base
        rows = c.execute("SELECT * FROM UsuarioSoftware ORDER BY idUsuario")
        for row in rows:
            print ("Nombre de Usuario:          ", row[0])
            print ("Correo de usuario:          ", row[1])
            print ("ID de usuario:              ", row[2])
            print ("Contraseña de usuario:      ", row[3]) # TODO BORRAR
            saltoLinea()

    def comparaContrasenia(self,usuarioAutenticado,usuarioAIngresar,contraseniaAIngresar):
        rows = c.execute("SELECT idUsuario FROM UsuarioSoftware WHERE nombreUsuario == ? AND contraseniaUsuario == ?" ,(usuarioAIngresar,contraseniaAIngresar))
        for row in rows:
            usuarioAutenticado = row[0]
        if usuarioAutenticado == None:
            return 0
        else:
            return usuarioAutenticado

class Contacto():
    def __init__(self):
        self.idUsuario = idUsuario
        self.nombreContacto = nombreContacto
        self.idContacto = idContacto
        self.correoContacto = correoContacto
        self.usuarioAutenticado = usuarioAutenticado
        self.textoABuscar = textoABuscar

    def crearTabla(self):
        c.execute ("CREATE TABLE IF NOT EXISTS Contacto (idUsuario INT, nombreContacto TEXT, correoContacto TEXT, idContacto TEXT)") # Crea la tabla

    def agregar(self,idUsuario,nombreContacto,correoContacto,idContacto): #Agrega los valores dados a la tabla
        c.execute ("INSERT INTO Contacto (idUsuario,nombreContacto,correoContacto,idContacto) VALUES (?,?,?,?)", (idUsuario,nombreContacto,correoContacto,idContacto))

    def mostrar(self,idUsuario): #Muestra TODOS los usuarios que existen en la base
        rows = c.execute ("SELECT * FROM Contacto WHERE idUsuario == ? " , (idUsuario,))
        resultados = 0
        for row in rows:
            print ("Nombre del contacto:        ", row[1])
            print ("Correo de contacto:         ", row[2])
            print ("ID de contacto:             ", row[3])
            resultados = (resultados + 1)
            saltoLinea()
        if resultados > 0:
            print ("Mostrando                   ", resultados," contactos")
            saltoLinea()
            pause()
        else:
            print ("No hay contactos registrados.")
            saltoLinea()
            pause()

    def seleccionarContacto (self,idUsuario,textoABuscar):
        rows = c.execute ("SELECT * FROM Contacto WHERE nombreContacto LIKE ? AND idUsuario == ? ORDER BY nombreContacto ASC" , (textoABuscar + '%',idUsuario,))
        IDcontactoSeleccionado = 0
        contactoSeleccionado = 0
        resultados = 0
        for row in rows:
            print ("Nombre del contacto:        ", row[1])
            print ("Correo de contacto:         ", row[2])
            print ("ID de contacto:             ", row[3])
            resultados = (resultados + 1)
            saltoLinea()
        if resultados > 0:
            print ("Mostrando                   ", resultados," contactos")
            saltoLinea()
            IDcontactoSeleccionado = input ("Slecciona el id del contacto que quieres seleccionar ")
        else:
            print ("No existen contactos con ese nombre.")
            saltoLinea()
            pause()
        rows = c.execute ("SELECT * FROM Contacto WHERE idContacto == ? AND idUsuario == ?" , (IDcontactoSeleccionado,idUsuario,))
        for row in rows:
            contactoSeleccionado = row[2]
        return contactoSeleccionado

    def eliminarContacto (self,idUsuario,textoABuscar): #Muestra TODOS los usuarios que existen en la base
        rows = c.execute ("SELECT * FROM Contacto WHERE correoContacto == ? AND idUsuario == ?" , (textoABuscar,idUsuario,))
        for row in rows:
            nombre = row[1]
        print ("El contacto llamado ", nombre," sera eliminado")
        saltoLinea()
        proceder = input ("Desea proceder= S/N: ")
        if (proceder == "s" or proceder == "S"):
            c.execute ("DELETE FROM Contacto WHERE correoContacto == ? AND idUsuario == ?" , (textoABuscar,idUsuario,))
            print ("Contacto eliminado con exito!")
            pause()
        elif (proceder == "n" or proceder == "N"):
            print ("El contacto no ha sido eliminado")
            pause()

    def modificar(self,idUsuario,textoABuscar):
        rows = c.execute ("SELECT * FROM Contacto WHERE correoContacto == ? AND idUsuario == ?" , (textoABuscar,idUsuario,))
        for row in rows:
            nombre = row[1]
            correo = row [2]
        print ("El contacto llamado ", nombre," sera modificado:")
        print ("Seleccione que campo se va a modificar:")
        print ("1.- Nombre")
        print ("2.- Correo")
        opcion = input ("Seleccione un campo: ")
        if opcion == "1":
            print ("Ingrese a continuacion el nuevo nombre para ",nombre)
            nuevoNombre = input ("Nombre: ")
            c.execute ("UPDATE Contacto SET nombreContacto == ? WHERE correoContacto == ? AND idUsuario == ?" , (nuevoNombre,textoABuscar,idUsuario,))
            print ("Contacto actualizado con exito!")
            pause()
        elif opcion == "2":
            print ("Ingrese a continuacion el nuevo correo para ",nombre)
            nuevoCorreo = input ("Nombre: ")
            c.execute ("UPDATE Contacto SET correoContacto == ? WHERE correoContacto == ? AND idUsuario == ?" , (nuevoCorreo,textoABuscar,idUsuario,))
            print ("Contacto actualizado con exito!")
            pause()

    def obtenerID(self,idUsuario):
        contador = c.execute("SELECT * FROM Contacto WHERE idUsuario == ?" ,(idUsuario,))
        ID = len(contador.fetchall())
        return ID

class Correo():
    def __init__(self):
        self.idUsuario = idUsuario
        self.idCorreo = idCorreo
        self.fechaCorreo = fechaCorreo
        self.asuntoCorreo = asuntoCorreo
        self.CC = CC
        self.Bcc = Bcc
        self.cuerpoCorreo = cuerpoCorreo
        self.archivoAdjunto = archivoAdjunto
        self.usuarioAutenticado = usuarioAutenticado
        self.estado = estado
        self.campoABuscar = campoABuscar
        self.textoABuscar = textoABuscar
        self.accionARealizar = accionARealizar

    def crearTabla(self):
        c.execute("CREATE TABLE IF NOT EXISTS Correo (idUsuario INT, idCorreo INT, fechaCorreo TEXT, asuntoCorreo TEXT, CC TEXT, Bcc TEXT, cuerpoCorreo TEXT, archivoAdjunto TEXT, estado TEXT)") # Crea la tabla

    def agregar(self,idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto, estado): #Agrega los valores dados a la tabla
        c.execute ("INSERT INTO Correo (idUsuario, idCorreo, fechaCorreo, asuntoCorreo, CC, Bcc, cuerpoCorreo, archivoAdjunto, estado) VALUES (?,?,?,?,?,?,?,?,?)", (idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto,estado))

    def obtenerID(self,idUsuario):
        contador = c.execute("SELECT * FROM Correo WHERE idUsuario == ?" ,(idUsuario,))
        ID = len(contador.fetchall())
        return ID

    def seleccionarCorreo (self,idUsuario,campoABuscar,textoABuscar):
        IDCOrreoSeleccionado = 0
        resultados = 0
        if campoABuscar == "cuerpoCorreo":
            rows = c.execute ("SELECT * FROM Correo WHERE cuerpoCorreo LIKE ? AND idUsuario == ? ORDER BY idCorreo DESC" , ('%' + textoABuscar + '%', idUsuario,))
        if campoABuscar == "asuntoCorreo":
            rows = c.execute ("SELECT * FROM Correo WHERE asuntoCorreo LIKE ? AND idUsuario == ? ORDER BY idCorreo DESC" , ('%' + textoABuscar + '%', idUsuario,))
        if campoABuscar == "fechaCorreo":
            rows = c.execute ("SELECT * FROM Correo WHERE fechaCorreo LIKE ?  AND idUsuario == ? ORDER BY idCorreo DESC" , (textoABuscar + '%', idUsuario,))
        if campoABuscar == "CC":
            rows = c.execute ("SELECT * FROM Correo WHERE CC == ? AND idUsuario == ?  ORDER BY idCorreo DESC" , (textoABuscar, idUsuario,))
        if campoABuscar == "Recientes":
            rows = c.execute ("SELECT * FROM Correo  WHERE idUsuario == ? ORDER BY fechaCorreo DESC LIMIT 5 " , (idUsuario,))
        for row in rows:
            print ("idUsuario:                  ", row[0]) # DEBUG
            print ("idCorreo:                   ", row[1])
            print ("fechaCorreo:                ", row[2])
            print ("asuntoCorreo:               ", row[3])
            print ("CC:                         ", row[4])
            print ("Bcc:                        ", row[5])
            print ("cuerpoCorreo:               ", row[6])
            print ("Achivo Adjunto:             ", row[7])
            print ("Estado del correo:          ", row[8])
            resultados = (resultados + 1)
            saltoLinea()
        if resultados > 0:
            print ("Encontrados                 ", resultados ," correos")
            saltoLinea()
            IDCOrreoSeleccionado = input ("Slecciona el id del contacto que quieres seleccionar ")
        else:
            print ("Su busqueda no arrojo resultados.")
            IDCOrreoSeleccionado = ""
            saltoLinea()
            pause()
        return IDCOrreoSeleccionado

    def eliminarCorreo (self,idUsuario,idCorreo,accionARealizar): #Muestra TODOS los usuarios que existen en la base
        rows = c.execute ("SELECT * FROM Correo WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
        for row in rows:
            para = row[4]
            asunto = row[3]
        if accionARealizar == "Enviar": # Para enviar a papelera
            print ("El correo dirigido a ",para ," con asunto ", asunto ," sera enviado.")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("UPDATE Correo SET estado = 'Enviado' WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
                print ("Correo enviado con exito! a" , para)
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("El correo no ha sido enviado")
                pause()
        if accionARealizar == "Reciclar": # Para enviar a papelera
            print ("El correo dirigido a ",para ," con asunto ", asunto ," sera enviado a la papelera.")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("UPDATE Correo SET estado = 'Papelera' WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
                print ("Correo enviado a la papelera con exito!")
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("El correo no ha sido enviado a la papelera")
                pause()
        if accionARealizar == "Restaurar": # Para enviar a papelera
            print ("El correo dirigido a ",para ," con asunto ", asunto ," sera restaurado como borrador.")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("UPDATE Correo SET estado = 'Borrador' WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
                print ("Correo restaurado con exito!")
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("El correo no ha sido restaurado")
                pause()
        if accionARealizar == "Eliminar": # Para enviar a papelera
            print ("El correo dirigido a ",para ," con asunto ", asunto ," sera eliminado por completo")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("DELETE FROM Correo WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
                print ("Correo eliminado con exito!")
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("El correo no ha sido eliminado")
                pause()

        if accionARealizar == "ReciclarVarios": # Para enviar a papelera
            print ("Todos los correos que se encuentren como borrador seran enviados a la papelera")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("UPDATE Correo SET estado = 'Papelera' WHERE estado == 'Borrador'  AND idUsuario == ?" , (idUsuario,))
                print ("Correos enviado a la papelera con exito!")
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("Los correos no ha sido enviados a la papelera")
                pause()
        if accionARealizar == "RestaurarVarios": # Para enviar a papelera
            print ("Todos los correos que se encuentren en la papelera seran marcados como borradores")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("UPDATE Correo SET estado = 'Borrador' WHERE estado == 'Papelera' AND idUsuario == ?" , (idUsuario,))
                print ("Correos restaurados con exito!")
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("Los correos no ha sido restaurados")
                pause()
        if accionARealizar == "EliminarVarios": # Para enviar a papelera
            print ("Todos los correos en la papelera seran eliminados")
            proceder = input ("Desea proceder= S/N: ")
            if (proceder == "s" or proceder == "S"):
                c.execute ("DELETE FROM Correo WHERE estado == 'Papelera' AND idUsuario == ?" , (idCorreo,idUsuario,))
                print ("Correos eliminados con exito!")
                pause()
            elif (proceder == "n" or proceder == "N"):
                print ("Los correos no han sido eliminados")
                pause()

    def modificarCorreo (self,idUsuario,idCorreo):
        rows = c.execute ("SELECT * FROM Correo WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
        for row in rows:
            idUsuario =         row[0]
            idCorreo =          row[1]
            fechaCorreo =       row[2]
            asuntoCorreo =      row[3]
            CC =                row[4]
            Bcc =               row[5]
            cuerpoCorreo =      row[6]
            archivoAdjunto =    row[7]
        print ("El correo esta guardado asi:")
        print ("1.- asuntoCorreo:               ", row[3])
        print ("2.- CC:                         ", row[4])
        print ("3.- Bcc:                        ", row[5])
        print ("4.- cuerpoCorreo:               ", row[6])
        campo = input ("Seleccione un campo a modificar")
        if campo == "1":
            print("El asunto actual del correo es: ",asuntoCorreo)
            asuntoCorreo = input ("Ingrese el nuevo asunto: ")
        elif campo == "2":
            print("El destinatario actual del correo es: ", CC)
            CC = menuSeleccionContacto()
        elif campo == "3":
            print("El Bcc actual del correo es: ", Bcc)
            Bcc = menuSeleccionContacto()
        elif campo == "4":
            print("El cuerpo actual del correo es: ")
            print (cuerpoCorreo)
            cuerpoCorreo = input ("Ingrese el nuevo cuerpo del correo: ")
        estado = "Borrador"
        c.execute ("DELETE FROM Correo WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,)) # ELimina el correo de la tabla ya que ya se han rescatado y modificado sus datos
        c.execute ("INSERT INTO Correo (idUsuario, idCorreo, fechaCorreo, asuntoCorreo, CC, Bcc, cuerpoCorreo, archivoAdjunto, estado) VALUES (?,?,?,?,?,?,?,?,?)", (idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto,estado))

    def reenviarCorreo (self,idUsuario,idCorreo):
        rows = c.execute ("SELECT * FROM Correo WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
        for row in rows:
            idUsuario =         row[0]
            idCorreo =          row[1]
            fechaCorreo =       row[2]
            asuntoCorreo =      row[3]
            CC =                row[4]
            Bcc =               row[5]
            cuerpoCorreo =      row[6]
            archivoAdjunto =    row[7]
        asuntoCorreo = (str("RE:" + asuntoCorreo))
        cuerpoCorreo = (str("Copia del correo enviado a " + CC + "\n" + cuerpoCorreo))
        fechaCorreo = datetime.now()
        CC = menuSeleccionContacto()
        estado = "Borrador"
        idCorreo = (objetoCorreo.obtenerID(objetoCorreo,usuarioAutenticado) + 1)
        enviar =                input ("Desea enviar el correo? S/N: ")
        if (enviar == "s" or enviar == "S"):
            estado = "Enviado"
            c.execute ("INSERT INTO Correo (idUsuario, idCorreo, fechaCorreo, asuntoCorreo, CC, Bcc, cuerpoCorreo, archivoAdjunto, estado) VALUES (?,?,?,?,?,?,?,?,?)", (idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto,estado))
            print ("Correo reenviado con exito!")
            pause()
        elif (enviar == "n" or enviar == "N"):
            estado = "Borrador"
            c.execute ("INSERT INTO Correo (idUsuario, idCorreo, fechaCorreo, asuntoCorreo, CC, Bcc, cuerpoCorreo, archivoAdjunto, estado) VALUES (?,?,?,?,?,?,?,?,?)", (idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto,estado))
            print ("Envio cancelado, correo guardado como borrador.")
            pause()

    def estadoDelCorreo(self,idUsuario,idCorreo):
        rows = c.execute ("SELECT * FROM Correo WHERE idCorreo == ? AND idUsuario == ?" , (idCorreo,idUsuario,))
        for row in rows:
            para = row[4]
            asunto = row[3]
            estado = row[8]
        return estado

def menuCorreos():
    objetoCorreo = Correo
    op = 0
    cls()
    while op != "4":
        print ("Menu Correos.")
        print ("1.- Mostrar los correos enviados recientemente.")
        print ("2.- Buscar correos.")
        print ("3.- Administrar correos.")
        print ("4.- Salir.")
        idUsuario = usuarioAutenticado # para separar los contactos entre usuarios
        op = input("Opcion: ")
        if op == "1":
            cls()
            print ("Mostrando los ultimos correos enviados.")
            campoABuscar = "Recientes"
            textoABuscar = ""
            IDCOrreoSeleccionado = objetoCorreo.seleccionarCorreo(objetoCorreo, idUsuario, campoABuscar, textoABuscar)
            if IDCOrreoSeleccionado != "":
                menuOpcionesCorreo(IDCOrreoSeleccionado)
            pause()
        elif op == "2":
            cls()
            opBuscar = 0
            while opBuscar != "3":
                print ("1.- Buscar los correos enviados por la fecha dada.")
                print ("2.- Buscar los correos enviados a un cierto contacto.")
                print ("3.- Buscar por una cadena en el Texto, CC o Asunto del correo.")
                print ("4.- Regresar al menu anterior.")
                opBuscar = input ("Seleccione un metodo de busqueda ")
                if opBuscar == "1": # Correos enviados a cierta fecha
                    cls()
                    campoABuscar = "fechaCorreo"
                    print ("Para buscar ingrese la fecha en que se creo el correo")
                    print ("Puede ser el año entero (AAAA), el mes (AAAA-MM) o el dia (AAAA-MM-DD)")
                    textoABuscar = input ("Ingrese la fecha en la que quiere que el correo se busque: ")
                    IDCOrreoSeleccionado = objetoCorreo.seleccionarCorreo(objetoCorreo, idUsuario, campoABuscar, textoABuscar)
                    if IDCOrreoSeleccionado != "":
                        menuOpcionesCorreo(IDCOrreoSeleccionado)
                    pause()
                elif opBuscar == "2": # Correos enviados a cierto contacto
                    cls()
                    campoABuscar = "CC"
                    textoABuscar = menuSeleccionContacto() # Espera un id de contacto a buscar
                    if textoABuscar != "":
                        print ("Buscando los correos enviados al contacto ", textoABuscar)
                        IDCOrreoSeleccionado = objetoCorreo.seleccionarCorreo(objetoCorreo, idUsuario, campoABuscar, textoABuscar)
                        if IDCOrreoSeleccionado != "":
                            menuOpcionesCorreo(IDCOrreoSeleccionado)
                    pause()
                elif opBuscar == "3":
                    cls()
                    print ("Desea buscar un correo que contenga una cadena de texto en:")
                    print ("1.- El cuerpo del correo.")
                    print ("2.- En el asunto del correo")
                    opBuscaeEn = input ("Seleccione una opcion: ")
                    if opBuscaeEn == "1":
                        campoABuscar = "cuerpoCorreo"
                        textoABuscar = input ("Ingrese la cadena que quiere buscar en el el cuerpo del correo")
                        IDCOrreoSeleccionado = objetoCorreo.seleccionarCorreo(objetoCorreo, idUsuario, campoABuscar, textoABuscar)
                        if IDCOrreoSeleccionado != "":
                            menuOpcionesCorreo(IDCOrreoSeleccionado)
                    if opBuscaeEn == "2":
                        campoABuscar = "asuntoCorreo"
                        textoABuscar = input ("Ingrese la cadena que quiere buscar en el el asunto del correo")
                        IDCOrreoSeleccionado = objetoCorreo.seleccionarCorreo(objetoCorreo, idUsuario, campoABuscar, textoABuscar)
                        if IDCOrreoSeleccionado != "":
                            menuOpcionesCorreo(IDCOrreoSeleccionado)
                    print ("En progreso")
                    pause()
                elif opBuscar == "4":
                    menuCorreos()
        elif op == "3":
            cls()
            print ("Menu de administracion de varios correos.")
            print ("Seleccione una opcion.")
            print ("1.- Vaciar papelera.")
            print ("2.- Restaurar papelera")
            print ("3.- Enviar a papelera")
            opcion = input ("Seleccione una opcion: ")
            if opcion == "1":
                IDCOrreoSeleccionado = ""
                accionARealizar = "EliminarVarios"
                objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)
            elif opcion == "2":
                IDCOrreoSeleccionado = ""
                accionARealizar = "RestaurarVarios"
                objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)
            elif opcion == "3":
                IDCOrreoSeleccionado = ""
                accionARealizar = "ReciclarVarios"
                objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)
        elif op == "4":
            menuPrincipal()

def menuContactos():
    objetoContacto = Contacto
    op = 0
    while op != "4":
        cls()
        print ("Menu Contactos")
        print ("1.- Insertar un nuevo contacto.")
        print ("2.- Mostrar los contactos existentes.")
        print ("3.- Eliminar algun contacto")
        print ("4.- Modificar algun contacto")
        print ("5.- Salir.")
        idUsuario = usuarioAutenticado # para separar los contactos entre usuarios
        op = input("Opcion: ")
        if op == "1":
            cls()
            nombreContacto =    input ("Ingrese el nombre del nuevo contacto:       ")
            correoContacto =    input ("Ingrese el correo del contacto:             ")
            idContacto = (objetoContacto.obtenerID(objetoContacto,usuarioAutenticado) + 1)
            objetoContacto.agregar(objetoContacto,idUsuario,nombreContacto,correoContacto,idContacto)
            pause()
        elif op == "2":
            cls()
            objetoContacto.mostrar(objetoContacto,idUsuario)
        elif op == "3":
            cls()
            contactoAEliminar = menuSeleccionContacto()
            if contactoAEliminar != 0:
                objetoContacto.eliminarContacto(objetoContacto,idUsuario,contactoAEliminar)
        elif op == "4":
            cls()
            contactoAModificar = menuSeleccionContacto()
            if contactoAModificar != 0:
                objetoContacto.modificar(objetoContacto,idUsuario,contactoAModificar)
        elif op == "5":
            menuPrincipal()

def menuCorreoNuevo():
    objetoCorreo = Correo
    idUsuario = usuarioAutenticado
    cls()
    print ("El correo se enviara a algun contacto ya registrado, o uno nuevo?")
    print ("1.- Contacto existente.")
    print ("2.- Nuevo contacto.")
    opcion = input ("Seleccione una opcion ")
    if opcion == "1":
        CC = menuSeleccionContacto()
        print ("CC:                                        ",CC)
    elif opcion == "2":
        CC =                    input ("Para:                                       ") # Asi de identado para que entre en el IF
    Bcc =                   input ("BCC:                                        ")
    idCorreo = (objetoCorreo.obtenerID(objetoCorreo,usuarioAutenticado) + 1)
    asuntoCorreo =          input ("Asunto:                                     ")
    cuerpoCorreo =          input ("Redacte el cuerpo del correo a continuacion: \n")
    archivoAdjunto =        "Archivo"
    fechaCorreo =           datetime.now()
    estado =                "Borrador"
    enviar =                input ("Desea enviar el correo? S/N: ")
    if (enviar == "s" or enviar == "S"):
        estado = "Enviado"
        objetoCorreo.agregar(objetoCorreo,idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto,estado)
        print ("Correo enviado!")
        pause()
    elif (enviar == "n" or enviar == "N"):
        estado = "Borrador"
        objetoCorreo.agregar(objetoCorreo,idUsuario,idCorreo,fechaCorreo,asuntoCorreo,CC,Bcc,cuerpoCorreo,archivoAdjunto,estado)
        print ("Envio cancelado, correo guardado como borrador.")
        pause()
    if opcion == "2":
        objetoContacto = Contacto
        cls()
        print ("Como ha enviado un correo a un contacto que no existe, puede agregarlo ahora.")
        nuevoContacto = input ("Desea agregar el contacto S/ N: ")
        if (nuevoContacto == "s" or nuevoContacto == "S"):
            print (nuevoContacto)
            nombreContacto =    input ("Ingrese el nombre del nuevo contacto:       ")
            print ("Ingrese el correo del contacto:             ", CC)
            correoContacto = CC
            idContacto = (objetoContacto.obtenerID(objetoContacto,usuarioAutenticado) + 1)
            objetoContacto.agregar(objetoContacto,idUsuario,nombreContacto,correoContacto,idContacto)
            pause()
        elif (nuevoContacto == "n" or nuevoContacto == "N"):
            print ("El contacto no sera agregado a tu lista.")
            pause()

def menuOpcionesCorreo(IDCOrreoSeleccionado):
    cls()
    objetoCorreo = Correo
    print ("Menu de opciones para un correo")
    estado = objetoCorreo.estadoDelCorreo(objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado)
    if estado == "Enviado":
        print ("El correo ya ha sido enviado, asi que no se puede eliminar o reciclar")
        print ("Las opciones que hay para este correo son:")
        print ("1.- Reenviar:")
        opcion = input ("Seleccione una opcion: ")
        if opcion == "1":
            objetoCorreo.reenviarCorreo(objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado)
            pause()
    elif estado == "Borrador":
        print ("El correo es un borrador")
        print ("Las opciones que hay para este correo son:")
        print ("1.- Enviar")
        print ("2.- Modificar")
        print ("2.- Enviar a papelera")
        opcion = input ("Seleccione una opcion: ")
        if opcion == "1":
            accionARealizar = "Enviar"
            objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)
            pause()
        elif opcion == "2":
            objetoCorreo.modificarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado)
        elif opcion == "3":
            accionARealizar = "Reciclar"
            objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)
    elif estado == "Papelera":
        print ("El coreo esta el la papelera")
        print ("Las opciones que hay para este correo son:")
        print ("1.- Restaurar.")
        print ("2.- Eliminar por completo.")
        opcion = input ("Seleccione una opcion: ")
        if opcion == "1":
            accionARealizar = "Restaurar"
            objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)
            pause()
        elif opcion == "2":
            accionARealizar = "Eliminar"
            objetoCorreo.eliminarCorreo (objetoCorreo,usuarioAutenticado,IDCOrreoSeleccionado,accionARealizar)

def menuUsuarioSoftware():
    objetoUsuario = UsuarioSoftware
    op = 0
    cls()
    while op != "3":
        print ("Menu Usuarios")
        print ("1.- Insertar un nuevo usuario del software")
        print ("2.- Mostrar los usuarios registrados")
        print ("3.- Salir")
        op = input  ("Opcion: ")
        if op == "1":
            cls()
            nombreUsuario =             input ("Ingrese el nombre del nuevo usuario:        ")
            coreoUsuario =              input ("Ingrese el correo del usuario:              ")
            idUsuario =                 input ("ID Usuario:                                 ") #TODO
            AUXcontraseniaUsuario1 =    input ("Ingrese la contraseña del usuario:          ")
            AUXcontraseniaUsuario2 =    input ("Vuelva a escribir la contraseña:            ")
            if AUXcontraseniaUsuario1 == AUXcontraseniaUsuario2:
                contraseniaUsuario = AUXcontraseniaUsuario1
                objetoUsuario.agregar(objetoUsuario,nombreUsuario,coreoUsuario,idUsuario,contraseniaUsuario)
            else:
                print ("Las contraseñas no coinciden, vuelva a intentarlo de nuevo")
        elif op == "2":
            cls()
            objetoUsuario.mostrar(objetoUsuario)
        elif op == "3":
            menuPrincipal()

def menuSeleccionContacto():
    objetoContacto = Contacto
    idUsuario = usuarioAutenticado
    contactoSeleccionado = 0
    op = 0
    cls()
    while op != "3":
        print ("Desea buscar un contacto por nombre, o mostrar todos los almacenados?.")
        print ("1.- Buscar un solo contacto por nombre.")
        print ("2.- Mostrar todos mis contactos.")
        print ("3.- Cancelar")
        op = input ("Seleccione una opcion: ")
        if op == "1":
            cls()
            textoABuscar = input  ("Ingrese el nombre del contacto que quiere buscar: ")
            contactoSeleccionado = objetoContacto.seleccionarContacto (objetoContacto,idUsuario,textoABuscar)
            return contactoSeleccionado
            op = "3"
        elif op == "2":
            cls()
            textoABuscar = ""
            contactoSeleccionado = objetoContacto.seleccionarContacto (objetoContacto,idUsuario,textoABuscar)
            return contactoSeleccionado
            op = "3"
        elif op == "3":
            return 0
            break

def menuPrincipal():
    global usuarioAutenticado # Si es 0, significa que no se ha iniciado sesion
    if usuarioAutenticado == 0:
        print ("Bienvenido, Ingreses sus datos de inicio")
        usuarioAIngresar =      input ("Ingrese su nombre de usuario:               ") # Crea una variable para comparar con las que hay en la base de usuarios
        contraseniaAIngresar =  input ("Ingrese su contraseña:                      ") # #Crea una variable para comparar con las que hay en la base de usuarios
        usuarioAutenticado = objetoUsuario.comparaContrasenia(objetoUsuario,usuarioAutenticado,usuarioAIngresar,contraseniaAIngresar) # Envia los datos y el objeto para su comparacion
    if usuarioAutenticado != 0:
        opcion = 0 #Reinicia la opcion, para evitar conflictos
        while opcion != "6":
            cls()
            print("Menu principal")
            print("Bienvenido usuario ",usuarioAutenticado)
            print("1.- Correo enviado")
            print("2.- Contactos")
            print("3.- Correo nuevo")
            print("4.- Salir del programa")
            opcion = input ("Seleccione una opcion: ")
            if opcion == "1":
                menuCorreos()
            elif opcion == "2":
                menuContactos()
            elif opcion == "3":
                menuCorreoNuevo()
            elif opcion == "646":
                menuUsuarioSoftware()
            elif opcion == "4":
                print ("Guardando cambios...")
                db.commit() # Guarda los cambios
                db.close() # Cierra la base
                usuarioAutenticado = 0
                exit() #Cierra el programa
            else:
                print("Opcion no valida")
                menuPrincipal()
    else:
        print("Nombre o contraseña incorrectos, Intentelo nuevamente")
        menuPrincipal()


db = sqlite3.connect("Correo.db") # Crea la coneccion entre el programa y el archivo
c = db.cursor() # Crea en C, un apuntador a la base de datos, cualquier movimiento se realiza apuntando a C

# EL SIG CODIGO CREA LAS TABLAS SOLO SI NO EXISTEN, recomendable dejarlo así #####################
objetoUsuario = UsuarioSoftware
objetoContacto = Contacto
objetoCorreo = Correo
objetoUsuario.crearTabla(objetoUsuario)
objetoCorreo.crearTabla(objetoCorreo)
objetoContacto.crearTabla(objetoContacto)
#####################################################################

## SOLO PARA DEBUG:########################################
#c.execute ("INSERT INTO UsuarioSoftware (nombreUsuario, coreoUsuario, idUsuario, contraseniaUsuario) VALUES (?,?,?,?)",  (123,123,123,123))
#db.commit() # Guarda los cambios
#db.close() # Cierra la base
#exit() #Cierra el programa
##########################################################

usuarioAutenticado = 0 #Para que sea global
menuPrincipal() #Ejecucion del programa
