from modulo import *
from sqlalchemy import and_

class MgrGraficarItem():

    
    def calculo_adelante_grafo(self, item, lista_items, graph, itemOrigen):
        """
        Metodo que obtiene todos los items que seran afectado hacia adelante por el impacto de un item
        @param item: item que sera analizado hacia adelante
        @param lista_items: lista de los items afectados, la cual sera actualizada
        @return: lista de items afectados hacia adelante
        """ 

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
            if hijo != None and (not(hijo in lista_items)):
                # Se agrega a la lista
                lista_items.append(hijo)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el hijo como
                # item a analizar
                if (item.idItem == itemOrigen.idItem):
                    n = pydot.Node(item.nombre, style='filled', fillcolor = 'red')  
                else:
                    n = pydot.Node(item.nombre)
                graph.add_node(n)
                graph.add_edge(pydot.Edge(hijo.nombre, n, label = 'P-H', fontcolor= 'green', constraint=False , color = 'green'))
                self.calculo_adelante_grafo(hijo, lista_items, graph,  itemOrigen)

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
                if (item.idItem == itemOrigen.idItem):
                    n = pydot.Node(item.nombre, style='filled', fillcolor = 'red')  
                else:
                    n = pydot.Node(item.nombre)
                graph.add_node(n)
                graph.add_edge(pydot.Edge(sucesor.nombre, n, label = 'A-S',fontcolor= 'pink', constraint=False ,  color = 'pink'))
                self.calculo_adelante_grafo(sucesor, lista_items, graph, itemOrigen)
        
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
                if (item.idItem == itemOrigen.idItem):
                    n = pydot.Node(item.nombre, style='filled', fillcolor = 'red')  
                else:
                    n = pydot.Node(item.nombre)
                graph.add_node(n)
                graph.add_edge(pydot.Edge(sucesor2.nombre, n, label = 'A-S',fontcolor= 'pink', constraint=False ,  color = 'pink'))
                self.calculo_adelante_grafo(sucesor2, lista_items, graph, itemOrigen)

        # Retornamos la lista de items que seran afectados hacia adelante
        return lista_items, graph


   
    def calculo_atras_grafo(self, item, lista_items, graph, itemOrigen):
        """
        Metodo que obtiene todos los items que seran afectado hacia atras por el impacto de un item
        @param item: item que sera analizado hacia atras
        @param lista_items: lista de los items afectados, la cual sera actualizada
        @return: lista de items afectadoa hacia atras
        """

        # Obtenemos el padre del item a analizar
        print "itemRecibido en calculoAtras", item.nombre
        padreId = Relacion.query.filter(Relacion.itemDestinoId==item.idItem,Relacion.tipoDeRelacion=='padre-hijo',Relacion.estado=='Pendiente').first()
        #padreIdRelacion = padreId.itemOrigenId
        print "padreId en calculoAtras", padreId
        if padreId != None:
            print "para ver si imprime algo, "
            padre = Item.query.filter(Item.idItem == padreId.itemOrigenId).first()

            # Si el padre no se encuentra ya en la lista de items afectados
            if padre!= None and (not(padre in lista_items)):

                # Lo agregamos a la lista
                lista_items.append(padre)
                # Se llama recursivamente al metodo, pasando la lista actualizada y el padre como
                # item a analizar
                if (item.idItem == itemOrigen.idItem):
                    n = pydot.Node(item.nombre, style='filled', fillcolor = 'red')  
                else:
                    n = pydot.Node(item.nombre)
                graph.add_node(n)
                graph.add_edge(pydot.Edge(n, padre.nombre,label = 'H-P',fontcolor= 'red', constraint=False , color = 'red'))
                self.calculo_atras_grafo(padre, lista_items, graph, itemOrigen)

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
                        if (padre.idItem == itemOrigen.idItem):
                            n = pydot.Node(padre.nombre, style='filled', fillcolor = 'red')  
                        else:
                            n = pydot.Node(padre.nombre)
                        graph.add_node(n)
                        graph.add_edge(pydot.Edge(hijo.nombre, n, label = 'P-H', fontcolor= 'green', constraint=False , color = 'green'))
                        self.calculo_adelante_grafo(hijo, lista_items, graph,  itemOrigen)


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
                        if (padre.idItem == itemOrigen.idItem):
                            n = pydot.Node(padre.nombre, style='filled', fillcolor = 'red')  
                        else:
                            n = pydot.Node(padre.nombre)
                        graph.add_node(n)
                        graph.add_edge(pydot.Edge(sucesor.nombre, n, label = 'S-A',fontcolor= 'pink', constraint=False ,  color = 'pink'))
                        self.calculo_adelante_grafo(sucesor, lista_items, graph, itemOrigen)


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
                if (item.idItem == itemOrigen.idItem):
                    n = pydot.Node(item.nombre, style='filled', fillcolor = 'red')  
                else:
                    n = pydot.Node(item.nombre)
                graph.add_node(n)
                graph.add_edge(pydot.Edge(n, antecesor.nombre, label = 'S-A',fontcolor= 'blue', constraint=False , color = 'blue'))
                self.calculo_atras_grafo(antecesor, lista_items, graph, itemOrigen)

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
                        if (antecesor.idItem == itemOrigen.idItem):
                            n = pydot.Node(antecesor.nombre, style='filled', fillcolor = 'red')  
                        else:
                            n = pydot.Node(antecesor.nombre)
                        graph.add_node(n)
                        graph.add_edge(pydot.Edge(hijo.nombre, n, label = 'P-H', fontcolor= 'green', constraint=False , color = 'green'))
                        self.calculo_adelante_grafo(hijo, lista_items, graph,  itemOrigen)


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
                        if (antecesor.idItem == itemOrigen.idItem):
                            n = pydot.Node(antecesor.nombre, style='filled', fillcolor = 'red')  
                        else:
                            n = pydot.Node(antecesor.nombre)
                        graph.add_node(n)
                        graph.add_edge(pydot.Edge(sucesor.nombre, n, label = 'S-A',fontcolor= 'pink', constraint=False ,  color = 'pink'))
                        self.calculo_adelante_grafo(sucesor, lista_items, graph, itemOrigen)
        
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
                if (item.idItem == itemOrigen.idItem):
                    n = pydot.Node(item.nombre, style='filled', fillcolor = 'red')  
                else:
                    n = pydot.Node(item.nombre)
                graph.add_node(n)
                graph.add_edge(pydot.Edge(n, antecesor2.nombre, label = 'S-A',fontcolor= 'blue', constraint=False , color = 'blue'))
                self.calculo_atras_grafo(antecesor2, lista_items, graph, itemOrigen)

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
                        if (antecesor2.idItem == itemOrigen.idItem):
                            n = pydot.Node(antecesor2.nombre, style='filled', fillcolor = 'red')  
                        else:
                            n = pydot.Node(antecesor2.nombre)
                        graph.add_node(n)
                        graph.add_edge(pydot.Edge(hijo.nombre, n, label = 'P-H', fontcolor= 'green', constraint=False , color = 'green'))
                        self.calculo_adelante_grafo(hijo, lista_items, graph,  itemOrigen)


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
                        if (antecesor2.idItem == itemOrigen.idItem):
                            n = pydot.Node(antecesor2.nombre, style='filled', fillcolor = 'red')  
                        else:
                            n = pydot.Node(antecesor2.nombre)
                        graph.add_node(n)
                        graph.add_edge(pydot.Edge(sucesor.nombre, n, label = 'S-A',fontcolor= 'pink', constraint=False ,  color = 'pink'))
                        self.calculo_adelante_grafo(sucesor, lista_items, graph, itemOrigen)
    


        # Retornamos la lista de items que seran afectados hacia atras
        return lista_items, graph