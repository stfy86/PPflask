from modulo import *
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, landscape, portrait
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm

class MgrReporte():
    
    
    estiloHoja = None
    tablaStyle = None
    
    def __init__(self):
        self.estiloHoja = getSampleStyleSheet()          
        self.tablaStyle =  [
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
                ('GRID', (0,0), (-1,-1), 0.01*cm, 'Black'),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),               
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BACKGROUND',(0,0),(-1,-1),colors.cyan),
                ('BOX',(0,0),(-1,-1),0.25,colors.black),
                ('INNERGRID',(0,0),(-1,-1),0.25,colors.black)
                ]   
                
    #############################            
    # datos basicos del reporte
    #############################
    def titulo(self):        
        cabecera = self.estiloHoja['Heading1']
        cabecera.pageBreakBefore = 0
        cabecera.keepWithNext = 0
        cabecera.alignment=TA_CENTER
        cabecera.backColor = colors.cyan
        parrafo = Paragraph('Sistema de Planificacion de Proyecto ', cabecera)
        return parrafo
            
    def encabezado(self, cadena):
        estilo = self.estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        return parrafo2
    
    #############################            
    # reportes del modulo administracion
    #############################
    def generarProyecto(self):
        story = []
        #
        parrafo = self.titulo()
        story.append(parrafo)    
        #
        parrafo2 = self.encabezado('Proyectos del Sistema')
        story.append(parrafo2)
        story.append(Spacer(0, 20))
        #Estilos de la tabla para cabeceras y datos
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        cabecera = [Paragraph('Nombre de Proyecto',thead),Paragraph('Lider',thead),Paragraph('Estado',thead),Paragraph('Presupuesto',thead),Paragraph('Fecha de Creacion',thead),Paragraph('Descripcion',thead)]
        contenido = [cabecera]
        lista = MgrProyecto().listar()
        tabla = Table(contenido)
        for p in lista:
            lider = MgrProyecto().getLider(p.nombre)
            contenido.append([Paragraph(p.nombre,tbody), Paragraph(lider,tbody), Paragraph(p.estado,tbody), Paragraph(str(p.presupuesto),tbody),Paragraph(str(p.fechaDeCreacion),tbody), Paragraph(p.descripcion,tbody)])
            tabla = Table(contenido)                      
        story.append(tabla)                     
        tabla.setStyle(self.tablaStyle)
        return story

    def generarUser(self):
        story = []
        parrafo = self.titulo()
        story.append(parrafo)    
        parrafo2 = self.encabezado('Usuarios del Sistema')
        story.append(parrafo2)
        story.append(Spacer(0, 20))
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        #
        cabecera = [Paragraph('Nick',thead),Paragraph('Nombre',thead),Paragraph('Apellido',thead),Paragraph('Email',thead),Paragraph('Telefono',thead),Paragraph('Estado',thead),Paragraph('Observacion',thead)]
        contenido = [cabecera]
        lista = MgrUser().listar()
        tabla = Table(contenido)
        for u in lista:
            contenido.append([Paragraph(u.name,tbody), Paragraph(u.nombre,tbody), Paragraph(u.apellido,tbody), Paragraph(u.email,tbody),Paragraph(str(u.telefono),tbody), Paragraph(u.estado,tbody), Paragraph(u.obs,tbody)])
            tabla = Table(contenido)                      
        story.append(tabla)     
        tabla.setStyle(self.tablaStyle)
        return story    
    
    
    #############################            
    # reportes del modulo de gestion
    #############################
    def datosProyecto(self, proyecto):
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        contenido=[]
        contenido.append([Paragraph('Nombre de Proyecto',thead),Paragraph(proyecto.nombre,tbody)])
        tabla = Table(contenido)
        lider = MgrProyecto().getLider(proyecto.nombre)
        contenido.append([Paragraph('Lider de Proyecto',thead),Paragraph(lider,tbody)])
        contenido.append([Paragraph('Estado de Proyecto',thead),Paragraph(proyecto.estado,tbody)])
        contenido.append([Paragraph('Presupuesto de Proyecto',thead),Paragraph(str(proyecto.presupuesto),tbody)])
        contenido.append([Paragraph('Fecha de Creacion de Proyecto',thead),Paragraph(str(proyecto.fechaDeCreacion),tbody)])
        contenido.append([Paragraph('Descripcion del Proyecto',thead),Paragraph(proyecto.descripcion,tbody)])
        comite = MgrComite().search(proyecto.nombre)
        contenido.append([Paragraph('Nombre de Comite del Proyecto',thead),Paragraph(comite.nombre,tbody)])
        contenido.append([Paragraph('Cantidad de Miembros',thead),Paragraph(str(comite.cantMiembro),tbody)])
        tabla = Table(contenido)
        tabla.setStyle(self.tablaStyle)
        return tabla
    
    
    def listaUsuariosDeProyecto(self, proyecto):
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        cabecera = [Paragraph('Nick',thead),Paragraph('Nombre',thead),Paragraph('Apellido',thead),Paragraph('Email',thead),Paragraph('Estado',thead),Paragraph('Rol en el Proyecto',thead)]
        contenido = [cabecera]
        lista = MgrProyecto().usersDeProyecto(proyecto.nombre)
        tabla = Table(contenido)
        for u in lista:
            rol = MgrUser().rolDeUser(u, proyecto.nombre)
            contenido.append([Paragraph(u.name,tbody), Paragraph(u.nombre,tbody), Paragraph(u.apellido,tbody), Paragraph(u.email,tbody), Paragraph(u.estado,tbody), Paragraph(rol.nombre,tbody)])
            tabla = Table(contenido)                      
        tabla.setStyle(self.tablaStyle)
        return tabla
    
    def listaFasesDeProyecto(self, proyecto):
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        cabecera = [Paragraph('Nombre',thead),Paragraph('Orden',thead),Paragraph('Estado',thead),Paragraph('Tipo de Item',thead)]
        contenido = [cabecera]
        lista = MgrProyecto().fasesDeProyecto(proyecto.nombre)
        tabla = Table(contenido)
        for f in lista:
            tipoDeItem = MgrTipoDeItem().filtrarXId(f.tipoDeItemId)
            contenido.append([Paragraph(f.nombre,tbody), Paragraph(str(f.orden),tbody), Paragraph(f.estado,tbody), Paragraph(tipoDeItem.nombre,tbody)])
            tabla = Table(contenido)                      
        tabla.setStyle(self.tablaStyle)
        return tabla
    
    def listaUsuariosDeComite(self, proyecto):
        #Estilos de la tabla para cabeceras y datos
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        cabecera = [Paragraph('Nick',thead),Paragraph('Nombre',thead),Paragraph('Apellido',thead),Paragraph('Email',thead),Paragraph('Estado',thead)]
        contenido = [cabecera]
        lista = MgrComite().miembrosComite(proyecto.nombre)
        tabla = Table(contenido)
        for u in lista:
            contenido.append([Paragraph(u.name,tbody), Paragraph(u.nombre,tbody), Paragraph(u.apellido,tbody), Paragraph(u.email,tbody), Paragraph(u.estado,tbody)])
            tabla = Table(contenido)                      
        tabla.setStyle(self.tablaStyle)
        return tabla
        
    
    
    def generarReporteProyecto(self, proyecto):
        story = []
        #
        parrafo = self.titulo()
        story.append(parrafo)    
        #
        parrafo2 = self.encabezado('Datos de Proyecto')
        story.append(parrafo2)
        story.append(Spacer(0, 20))
        datos = self.datosProyecto(proyecto)
        story.append(datos)
        #
        parrafo3 = self.encabezado('Usuarios del Proyecto')
        story.append(parrafo3)
        story.append(Spacer(0, 20))
        usuariosP = self.listaUsuariosDeProyecto(proyecto)
        story.append(usuariosP)
        #
        parrafo3 = self.encabezado('Usuarios del Comite')
        story.append(parrafo3)
        story.append(Spacer(0, 20))
        usuariosC = self.listaUsuariosDeComite(proyecto)
        story.append(usuariosC) 
        #
        parrafo3 = self.encabezado('Fases del Proyecto')
        story.append(parrafo3)
        story.append(Spacer(0, 20))
        fases = self.listaFasesDeProyecto(proyecto)
        story.append(fases) 
        return story
    
    
    
    
    def generarReporteFase(self, proyecto):
        story = []
        contenido=[]
        #
        parrafo = self.titulo()
        story.append(parrafo)    
        #        
        parrafo2 = self.encabezado('Fases del Proyecto ' + proyecto.nombre )
        story.append(parrafo2)
        
        story.append(Spacer(0, 20))
        #
        lista = MgrProyecto().fasesDeProyecto(proyecto.nombre)
        for f in lista:
            parrafo2 = self.encabezado('Datos de Fase y Lista de Item de la fase')
            story.append(parrafo2)
            contenido = self.datosFase(f)
            tabla = Table(contenido)
            tabla.setStyle(self.tablaStyle)
            story.append(tabla)
            story.append(Spacer(0, 20)) 
            tablaF = self.listaDeItem(f)
            story.append(tablaF)   
            story.append(Spacer(0, 40))
            contenido = []
        
        return story       
    
    def listaDeItem(self, fase):
        tipoDeItem = MgrTipoDeItem().filtrarXId(fase.tipoDeItemId)
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        contenido=[]
        cabecera = [Paragraph('Nombre',thead),Paragraph('Version',thead),Paragraph('Complejidad',thead),Paragraph('Costo',thead),Paragraph('Estado',thead), Paragraph('Tipo De Item',thead)]
        contenido = [cabecera]
        tabla = Table(contenido)
        lista = MgrFase().filtrarItems(fase.nombre)
        for i in lista:
            tipoDeItem = MgrTipoDeItem().filtrarXId(i.tipoDeItemId)
            contenido.append([Paragraph(i.nombre,tbody), Paragraph(str(i.version),tbody), Paragraph(str(i.complejidad),tbody), Paragraph(str(i.costo),tbody), Paragraph(i.estado,tbody), Paragraph(tipoDeItem.nombre,tbody)])
            tabla = Table(contenido)  
        return tabla
    
    def datosFase(self, fase):
        contenido = []        
        thead = self.estiloHoja['Heading5']
        thead.alignment=TA_CENTER
        tbody = self.estiloHoja["BodyText"]
        tbody.alignment=TA_LEFT
        tipoDeItem = MgrTipoDeItem().filtrarXId(fase.tipoDeItemId)
        contenido.append([Paragraph('Nombre de Fase',thead),Paragraph(fase.nombre,tbody)])
        contenido.append([Paragraph('Orden',thead),Paragraph(str(fase.orden),tbody)])
        contenido.append([Paragraph('Estado',thead),Paragraph(fase.estado,tbody)])
        contenido.append([Paragraph('Tipo de Item',thead),Paragraph(tipoDeItem.nombre,tbody)])
        return contenido