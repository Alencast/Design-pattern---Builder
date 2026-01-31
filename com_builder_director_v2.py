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

    
    def __init__(self, builder):
        self.builder = builder
    
    def adicionar_proteinas(self, queijo=None, presunto=None):
     
        if presunto:
            self.builder.presunto(presunto)
        if queijo:
            self.builder.queijo(queijo)
        return self
    
    def adicionar_vegetais(self, alface=None, tomate=None):
       
        if alface:
            self.builder.alface(alface)
        if tomate:
            self.builder.tomate(tomate)
        return self
    
    def adicionar_condimentos(self, maionese=False):
       
        if maionese:
            self.builder.maionese(True)
        return self
    
    def build(self):
        
        return self.builder.build()


# o cliente que vai definir os ingredientes, mas o director garante a ordem correta

# Sanduíche completo
s1 = (SanduicheDirector(SanduicheBuilder("integral"))
      .adicionar_proteinas(queijo="mussarela", presunto="presunto cozido")  # 1º Proteínas
      .adicionar_vegetais(alface="alface americana", tomate="tomate cereja")  # 2º Vegetais
      .adicionar_condimentos(maionese=True)                                   # 3º Condimentos
      .build())

print("Completo:", s1)

# Sanduíche vegetariano, ignora as opções de proteína 
s2 = (SanduicheDirector(SanduicheBuilder("francês"))
      .adicionar_proteinas(queijo="cottage")              # 1º Só queijo
      .adicionar_vegetais(alface="alface", tomate="tomate")  # 2º Vegetais
      .build())
print("Vegetariano:", s2)

# Sanduíche simples (só proteínas)
s3 = (SanduicheDirector(SanduicheBuilder("ciabatta"))
      .adicionar_proteinas(queijo="brie", presunto="parma")  # 1º Proteínas
      .build())
print("Simples:", s3)

print("\n Exemplo dem o director\n")
s4 = (SanduicheBuilder("integral")
      .presunto("presunto")
      .maionese(True)        # sem a ordem determinada pelo director
      .alface("alface")     
      .build())
print("Ordem errada:", s4)
