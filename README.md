# Design Pattern - Builder

Exemplos de implementação do padrão Builder para construção de sanduíches.

## Arquivos

### sem_builder.py
Implementação **sem** o padrão Builder. Mostra os problemas de usar construtores com muitos parâmetros:
- Difícil leitura com vários parâmetros nomeados
- Sem controle de ordem de construção
- Menos flexível e verboso

### com_builder_director_v2.py
Implementação **com** Builder Pattern e Director:
- **Builder**: constrói o objeto passo a passo com interface fluente
- **Director**: organiza a sequência de construção (proteínas → vegetais → condimentos)
- Código mais legível e manutenível
- Flexível para diferentes combinações

## Como executar

```bash
# Sem Builder Pattern
python sem_builder.py

# Com Builder Pattern + Director
python com_builder_director_v2.py
```

## Comparação

**Sem Builder:**
```python
s1 = Sanduiche("integral", queijo="mussarela", presunto="presunto cozido", 
               alface="alface americana", tomate="tomate cereja", maionese=True)
```

**Com Builder:**
```python
s1 = (SanduicheDirector(SanduicheBuilder("integral"))
      .adicionar_proteinas(queijo="mussarela", presunto="presunto cozido")
      .adicionar_vegetais(alface="alface americana", tomate="tomate cereja")
      .adicionar_condimentos(maionese=True)
      .build())
```