from modulo import *
from sqlalchemy import and_, or_

class MgrCambio():

    def getLBItem(self, item):
        listaLB = [] 
        todasLB = LineaBase.query.all()
        for lb in todasLB:
            l = LineaBase.query.filter(LineaBase.idLineaBase == lb.idLineaBase).first()
            if item in l.itemsLB:
                listaLB.append(l)
        return listaLB
        
        
    def calculo_adelante_grafo(self, item, lista_items):

        item.estado = "Revision"
        db.session.commit()
        # Obtenemos los hijos del item recibido
        hijosRelacion = Relacion.query.filter(Relacion.itemOrigenId==item.idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente').all()

        # Obtenemos los sucesores del item recibido
        sucesoresRelacion = Relacion.query.filter(Relacion.itemOrigenId==item.idItem,Relacion.tipoDeRelacion=='antecesor-sucesor',Relacion.estado=='Pendiente').all()

        # Obtenemos los sucesores del item recibido
        sucesoresRelacion2 = Relacion.query.filter(Relacion.itemDestinoId==item.idItem,Relacion.tipoDeRelacion=='sucesor-antecesor',Relacion.estado=='Pendiente').all()

        # Por cada uno de los hijos
        for hijos in hijosRelacion:
            #Se obtiene el item
            hijo = Item.query.filter(Item.idItem == hijos.itemDestinoId).first()
            # Si el hijo no se encuentra ya en la lista de items afectados
            if hijo != None and (not(hijo in lista_items) ):
                # Se agrega a la lista
                lista_items.append(hijo)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el hijo como
                # item a analizar
                hijo.estado = "Revision"
                db.session.commit()
                self.calculo_adelante_grafo(hijo, lista_items)

        # Por cada uno de los sucesores
        for sucesores in sucesoresRelacion:
            #Se obtiene el item
            sucesor = Item.query.filter(Item.idItem == sucesores.itemDestinoId).first()
            # Si el sucesor no se encuentra ya en la lista de items afectados
            if sucesor != None and (not(sucesor in lista_items)):
                # Se agrega a la lista
                lista_items.append(sucesor)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el sucesor como
                # item a analizar
                sucesor.estado = "Revision" 
                
                db.session.commit()
                
                self.calculo_adelante_grafo(sucesor, lista_items)
        
        # Por cada uno de los sucesores segundo caso
        for sucesores in sucesoresRelacion2:
            #Se obtiene el item
            sucesor2 = Item.query.filter(Item.idItem == sucesores.itemOrigenId).first()
            # Si el sucesor no se encuentra ya en la lista de items afectados
            if sucesor2 != None and (not(sucesor2 in lista_items)):
                # Se agrega a la lista
                lista_items.append(sucesor2)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el sucesor como
                # item a analizar
                
                sucesor2.estado = "Revision" 
                db.session.commit()
                self.calculo_adelante_grafo(sucesor2, lista_items)

        # Retornamos la lista de items que seran afectados hacia adelante
        return lista_items


   
    def calculo_atras_grafo(self, item, lista_items):
        item.estado = "Revision"
        db.session.commit()
        padreId = Relacion.query.filter(Relacion.itemDestinoId==item.idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente').first()
        if padreId != None:
            print "para ver si imprime algo, "
            padre = Item.query.filter(Item.idItem == padreId.itemOrigenId).first()

            # Si el padre no se encuentra ya en la lista de items afectados
            if padre!= None and (not(padre in lista_items)):

                # Lo agregamos a la lista
                lista_items.append(padre)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el padre como
                # item a analizar
                padre.estado = "Revision" 
                db.session.commit()
                self.calculo_atras_grafo(padre, lista_items)

                # Obtenemos los hijos del padre 
                hijosRelacion = Relacion.query.filter(Relacion.itemOrigenId==padre.idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente').all()

                # Obtenemos los sucesores del padre 
                sucesoresRelacion = Relacion.query.filter(Relacion.itemOrigenId==padre.idItem,Relacion.tipoDeRelacion=='antecesor-sucesor',Relacion.estado=='Pendiente').all()

                # Por cada uno de los hijos
                for hijos in hijosRelacion:
                    #Se obtiene el item
                    hijo = Item.query.filter(Item.idItem == hijos.itemDestinoId).first()
                    # Si el hijo no se encuentra ya en la lista de items afectados
                    if hijo != None and (not(hijo in lista_items)) and hijo.idItem != itemOrigen.idItem:
                        # Se agrega a la lista
                        lista_items.append(hijo)
                        # Se llama recursivamente al metodo, pasando la lista actualizada y el hijo como
                        # item a analizar
                        
                        hijo.estado = "Revision" 
            
                        db.session.commit()
                        self.calculo_adelante_grafo(hijo, lista_items)


                # Por cada uno de los sucesores
                for sucesores in sucesoresRelacion:
                    #Se obtiene el item
                    sucesor = Item.query.filter(Item.idItem == sucesores.itemDestinoId).first()
                    # Si el sucesor no se encuentra ya en la lista de items afectados
                    if sucesor != None and (not(sucesor in lista_items)) and sucesor.idItem != itemOrigen.idItem:
                        # Se agrega a la lista
                        lista_items.append(sucesor)
                        # Se llama recursivamente al metodo, pasando la lista actualizada y el sucesor como
                        # item a analizar
                    
                        sucesor.estado = "Revision" 
                        
                        db.session.commit()
                        self.calculo_adelante_grafo(sucesor, lista_items)


        # Obtenemos el antecesor del item a analizar
        antecesorId = Relacion.query.filter(Relacion.itemDestinoId==item.idItem,Relacion.tipoDeRelacion=='antecesor-sucesor',Relacion.estado=='Pendiente').first()
        #antecesorIdRelacion = antecesorId.itemDestinoId

        if antecesorId != None:
            antecesor = Item.query.filter(Item.idItem == antecesorId.itemOrigenId).first()   
            # Si el anteccesor no se encuentra ya en la lista de items afectados
            if antecesor != None and (not(antecesor in lista_items)):
                # Lo agregamos a la lista
                lista_items.append(antecesor)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el padre como
                # item a analizar
                
                antecesor.estado = "Revision" 
        
                db.session.commit()
                self.calculo_atras_grafo(antecesor, lista_items)

                # Obtenemos los hijos del antecesor 
                hijosRelacion = Relacion.query.filter(Relacion.itemOrigenId==antecesor.idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente').all()

                # Obtenemos los sucesores del padre 
                sucesoresRelacion = Relacion.query.filter(Relacion.itemDestinoId==antecesor.idItem,Relacion.tipoDeRelacion=='sucesor-antecesor',Relacion.estado=='Pendiente').all()

                # Por cada uno de los hijos
                for hijos in hijosRelacion:
                    #Se obtiene el item
                    hijo = Item.query.filter(Item.idItem == hijos.itemDestinoId).first()
                    # Si el hijo no se encuentra ya en la lista de items afectados
                    if hijo != None and (not(hijo in lista_items)) and hijo.idItem != itemOrigen.idItem:
                        # Se agrega a la lista
                        lista_items.append(hijo)
                        # Se llama recursivamente al metodo, pasando la lista actualizada y el hijo como
                        # item a analizar
                        
                        hijo.estado = "Revision" 
                        
                        db.session.commit()
                        self.calculo_adelante_grafo(hijo, lista_items)


                # Por cada uno de los sucesores
                for sucesores in sucesoresRelacion:
                    #Se obtiene el item
                    sucesor = Item.query.filter(Item.idItem == sucesores.itemOrigenId).first()
                    # Si el sucesor no se encuentra ya en la lista de items afectados
                    if sucesor != None and (not(sucesor in lista_items)) and sucesor.idItem != itemOrigen.idItem:
                        # Se agrega a la lista
                        lista_items.append(sucesor)
                        # Se llama recursivamente al metodo, pasando la lista actualizada y el sucesor como
                        # item a analizar
                        
                        sucesor.estado = "Revision" 
                
                        db.session.commit()
                        self.calculo_adelante_grafo(sucesor, lista_items)
        
        # Obtenemos el antecesor segundo caso del item a analizar
        antecesorId2 = Relacion.query.filter(Relacion.itemOrigenId==item.idItem,Relacion.tipoDeRelacion=='sucesor-antecesor',Relacion.estado=='Pendiente').first()
        #antecesorIdRelacion = antecesorId.itemDestinoId

        if antecesorId2 != None:
            antecesor2 = Item.query.filter(Item.idItem == antecesorId2.itemDestinoId).first()   
            # Si el anteccesor no se encuentra ya en la lista de items afectados
            if antecesor2 != None and (not(antecesor2 in lista_items)):
                # Lo agregamos a la lista
                lista_items.append(antecesor2)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el padre como
                # item a analizar
                
                antecesor2.estado = "Revision" 
                
                db.session.commit()         
                self.calculo_atras_grafo(antecesor2, lista_items)

                # Obtenemos los hijos del antecesor 
                hijosRelacion = Relacion.query.filter(Relacion.itemOrigenId==antecesor2.idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente').all()

                # Obtenemos los sucesores del padre 
                sucesoresRelacion = Relacion.query.filter(Relacion.itemDestinoId==antecesor2.idItem,Relacion.tipoDeRelacion=='sucesor-antecesor',Relacion.estado=='Pendiente').all()

                # Por cada uno de los hijos
                for hijos in hijosRelacion:
                    #Se obtiene el item
                    hijo = Item.query.filter(Item.idItem == hijos.itemDestinoId).first()
                    # Si el hijo no se encuentra ya en la lista de items afectados
                    if hijo != None and (not(hijo in lista_items)) and hijo.idItem != itemOrigen.idItem:
                        # Se agrega a la lista
                        lista_items.append(hijo)
                        # Se llama recursivamente al metodo, pasando la lista actualizada y el hijo como
                        # item a analizar
                        
                        hijo.estado = "Revision" 
                        
                        db.session.commit()       
                        self.calculo_adelante_grafo(hijo, lista_items)


                # Por cada uno de los sucesores
                for sucesores in sucesoresRelacion:
                    #Se obtiene el item
                    sucesor = Item.query.filter(Item.idItem == sucesores.itemOrigenId).first()
                    # Si el sucesor no se encuentra ya en la lista de items afectados
                    if sucesor != None and (not(sucesor in lista_items)) and sucesor.idItem != itemOrigen.idItem:
                        # Se agrega a la lista
                        lista_items.append(sucesor)
                        # Se llama recursivamente al metodo, pasando la lista actualizada y el sucesor como
                        # item a analizar
                        
                        sucesor.estado = "Revision" 
                        
                        db.session.commit()       
                        self.calculo_adelante_grafo(sucesor, lista_items)

        return lista_items