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
  
    #Director que garante a ordem obrigatória de construção:
    #1. adicionar_proteinas() - obrigatório primeiro
    #2. adicionar_vegetais() - obrigatório após proteínas
    #3. adicionar_condimentos() - obrigatório após vegetais
    #4. build() - só funciona após todos os passos obrigatórios
   
    
    def __init__(self, builder):
        self.builder = builder
        #  controlar a ordem de construção
        # _ atributo interno privado, não se usa fora da classe
        self._proteinas_adicionadas = False
        self._vegetais_adicionados = False
        self._condimentos_adicionados = False
    
    def adicionar_proteinas(self, queijo=None, presunto=None):
        # Proteínas vem  primeiro
        if self._proteinas_adicionadas:
            raise ValueError("Proteínas já foram adicionadas")
        
        if presunto:
            #Fluent Interface
            self.builder.presunto(presunto)
        if queijo:
            self.builder.queijo(queijo)
        
        self._proteinas_adicionadas = True
        return self
    
    def adicionar_vegetais(self, alface=None, tomate=None):
        # vgetais só podem ser adicionados após proteínas
        if not self._proteinas_adicionadas:
            raise ValueError("Proteínas devem ser adicionadas primeiro")
        if self._vegetais_adicionados:
            raise ValueError("Vegetais já foram adicionados")
        
        if alface:
            self.builder.alface(alface)
        if tomate:
            self.builder.tomate(tomate)
        
        self._vegetais_adicionados = True
        return self
    
    def adicionar_condimentos(self, maionese=False):
        # Condimentos por último
        if not self._proteinas_adicionadas:
            raise ValueError("Proteínas devem ser adicionadas primeiro")
        if not self._vegetais_adicionados:
            raise ValueError("Vegetais devem ser adicionados antes dos condimentos")
        if self._condimentos_adicionados:
            raise ValueError("Condimentos já foram adicionados")
        
        if maionese:
            self.builder.maionese(True)
        
        self._condimentos_adicionados = True
        return self
    
    def build(self):
        
        if not self._proteinas_adicionadas:
            raise ValueError("Não é possível construir: proteínas devem ser adicionadas")
        if not self._vegetais_adicionados:
            raise ValueError("Não é possível construir: vegetais devem ser adicionados")
        if not self._condimentos_adicionados:
            raise ValueError("Não é possível construir: condimentos devem ser adicionados")
        
        sanduiche = self.builder.build()
        self.reset()  # Reseta automaticamente após build para permitir reutilização
        return sanduiche
    
    def reset(self, builder=None):
        # Reseta o director para construir um novo sanduíche
        if builder:
            self.builder = builder
        
        self._proteinas_adicionadas = False
        self._vegetais_adicionados = False
        self._condimentos_adicionados = False
        return self


# o cliente que vai definir os ingredientes, mas o director garante a ordem correta

# Sanduíche completo (ordem obrigatória: proteínas -> vegetais -> condimentos)
s1 = (SanduicheDirector(SanduicheBuilder("integral"))
      .adicionar_proteinas(queijo="mussarela", presunto="presunto cozido")  # 1º Proteínas
      .adicionar_vegetais(alface="alface americana", tomate="tomate cereja")  # 2º Vegetais
      .adicionar_condimentos(maionese=True)                                   # 3º Condimentos
      .build())

print("Completo:", s1)

# Sanduíche vegetariano (todos os passos obrigatórios)
s2 = (SanduicheDirector(SanduicheBuilder("francês"))
      .adicionar_proteinas(queijo="cottage")              # 1º Só queijo
      .adicionar_vegetais(alface="alface", tomate="tomate")  # 2º Vegetais
      .adicionar_condimentos()                            # 3º Sem condimentos, mas passo obrigatório
      .build())
print("Vegetariano:", s2)

# Sanduíche simples (todos os passos obrigatórios)
s3 = (SanduicheDirector(SanduicheBuilder("ciabatta"))
      .adicionar_proteinas(queijo="brie", presunto="parma")  # 1º Proteínas
      .adicionar_vegetais()                               # 2º Sem vegetais, mas passo obrigatório
      .adicionar_condimentos()                            # 3º Sem condimentos, mas passo obrigatório
      .build())
print("Simples:", s3)


s4 = (SanduicheBuilder("integral")
      .presunto("presunto")
      .maionese(True)        # sem a ordem determinada pelo director
      .alface("alface")     
      .build())
print("Sem director (ordem livre):", s4)


# Teste 1: Tentar adicionar vegetais antes de proteínas
try:
    s5 = (SanduicheDirector(SanduicheBuilder("integral"))
          .adicionar_vegetais(alface="alface")  # Erro: proteínas devem vir primeiro
          .build())
except ValueError as e:
    print(f"Erro esperado: {e}")

# Teste 2: Tentar adicionar condimentos antes de vegetais
try:
    s6 = (SanduicheDirector(SanduicheBuilder("integral"))
          .adicionar_proteinas(queijo="mussarela")
          .adicionar_condimentos(maionese=True)  # Erro: vegetais devem vir primeiro
          .build())
except ValueError as e:
    print(f"Erro esperado: {e}")

# Teste 3: Tentar construir sem completar todos os passos
try:
    s7 = (SanduicheDirector(SanduicheBuilder("integral"))
          .adicionar_proteinas(queijo="mussarela")
          .adicionar_vegetais(alface="alface")
          # Falta adicionar_condimentos()
          .build())
except ValueError as e:
    print(f"Erro esperado: {e}")

# Teste 4: Tentar adicionar proteínas duas vezes
try:
    s8 = (SanduicheDirector(SanduicheBuilder("integral"))
          .adicionar_proteinas(queijo="mussarela")
          .adicionar_proteinas(presunto="presunto")  
          .build())
except ValueError as e:
    print(f"Erro esperado: {e}")
