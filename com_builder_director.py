class Sanduiche:
    def __init__(self, pão, queijo=None, presunto=None, alface=None, tomate=None, maionese=False):
        self.pão = pão
        self.queijo = queijo
        self.presunto = presunto
        self.alface = alface
        self.tomate = tomate
        self.maionese = maionese

    def __str__(self):
        return f"Sanduíche({self.pão}, queijo={self.queijo}, presunto={self.presunto}, " \
               f"alface={self.alface}, tomate={self.tomate}, maionese={self.maionese})"


class SanduicheBuilder:
    def __init__(self, pão):
        self._pão = pão
        self._queijo = None
        self._presunto = None
        self._alface = None
        self._tomate = None
        self._maionese = False

    def queijo(self, tipo):
        self._queijo = tipo
        return self

    def presunto(self, tipo):
        self._presunto = tipo
        return self

    def alface(self, tipo):
        self._alface = tipo
        return self

    def tomate(self, tipo):
        self._tomate = tipo
        return self

    def maionese(self, valor=True):
        self._maionese = valor
        return self

    def build(self):
        return Sanduiche(
            pão=self._pão,
            queijo=self._queijo,
            presunto=self._presunto,
            alface=self._alface,
            tomate=self._tomate,
            maionese=self._maionese
        )


class SanduicheDirector:
  
    @staticmethod
    def sanduiche_americano():
       
        return (SanduicheBuilder("integral")
                .presunto("presunto cozido")  
                .queijo("mussarela")          
                .alface("alface americana")   
                .tomate("tomate cereja")
                .maionese(True)               
                .build())
    
    @staticmethod
    def sanduiche_natural():
       
        return (SanduicheBuilder("integral")
                .queijo("cottage")            
                .alface("alface crespa")      
                .tomate("tomate comum")
                .build())
    
    @staticmethod
    def sanduiche_simples():
       
        return (SanduicheBuilder("francês")
                .presunto("presunto defumado") 
                .queijo("prato")                
                .build())
    
    @staticmethod
    def sanduiche_vegano():
    
        return (SanduicheBuilder("integral")
                .alface("alface roxa")
                .tomate("tomate seco")
                .build())


# Cliente n sabe a ordem de montagem, só escolhe a receita
print(" Cardápio \n")

s1 = SanduicheDirector.sanduiche_americano()
print("Americano:", s1)

s2 = SanduicheDirector.sanduiche_natural()
print("Natural:", s2)

s3 = SanduicheDirector.sanduiche_simples()
print("Simples:", s3)

s4 = SanduicheDirector.sanduiche_vegano()
print("Vegano:", s4)

print("\n(sem Director)\n")
s5 = SanduicheBuilder("ciabatta").queijo("brie").presunto("parma").maionese().build()
print("Gourmet:", s5)
