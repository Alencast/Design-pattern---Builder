


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


# Criando sanduíches sem Builder Pattern
# Problema: construtor com muitos parâmetros, difícil de ler e manter

# Sanduíche completo


# new Sanduiche("integral", null, "presunto", null, null, true) parametros em java
s1 = Sanduiche("integral", queijo="mussarela", presunto="presunto cozido", 
               alface="alface americana", tomate="tomate cereja", maionese=True)
print("Completo:", s1)

# Sanduíche vegetariano
s2 = Sanduiche("francês", queijo="cottage", alface="alface", tomate="tomate")
print("Vegetariano:", s2)

# Sanduíche simples (só proteínas)
s3 = Sanduiche("ciabatta", queijo="brie", presunto="parma")
print("Simples:", s3)
