package web.pulso.utils;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import web.pulso.models.*;
import web.pulso.repository.EscalaRepository;
import web.pulso.repository.PlantaoRepository;
import web.pulso.utils.generatePlantaoStrategy.GeracaoPlantoesStrategy;


import java.time.LocalDate;
import java.util.*;

@Component
public class EscalaBuilder {

    private final EscalaRepository escalaRepository;
    private final PlantaoRepository plantaoRepository;

    private String nome;
    private LocalDate mesReferencia;
    private Profissional lider;
    private Setor setor;

    private GeracaoPlantoesStrategy strategy;
    private Map<?, Plantao> contexto;

    public EscalaBuilder(EscalaRepository escalaRepository,
                         PlantaoRepository plantaoRepository) {
        this.escalaRepository = escalaRepository;
        this.plantaoRepository = plantaoRepository;
    }

    public EscalaBuilder withNome(String nome) {
        this.nome = nome;
        return this;
    }

    public EscalaBuilder withMesReferencia(LocalDate mesReferencia) {
        this.mesReferencia = mesReferencia;
        return this;
    }

    public EscalaBuilder withLider(Profissional lider) {
        this.lider = lider;
        return this;
    }

    public EscalaBuilder withSetor(Setor setor) {
        this.setor = setor;
        return this;
    }

    public EscalaBuilder withPlantoesStrategy(
            GeracaoPlantoesStrategy strategy,
            Map<?, Plantao> contexto) {

        this.strategy = strategy;
        this.contexto = contexto;
        return this;
    }

    @Transactional
    public Escala build() {

        Objects.requireNonNull(nome);
        Objects.requireNonNull(mesReferencia);
        Objects.requireNonNull(lider);
        Objects.requireNonNull(setor);

        Escala escala = new Escala();
        escala.setNome(nome);
        escala.setMesReferencia(mesReferencia);
        escala.setLiderEscala(lider);
        escala.setSetor(setor);

        escalaRepository.save(escala);

        if (strategy != null) {
            List<Plantao> plantoes = strategy.gerar(escala, contexto);
            plantaoRepository.saveAll(plantoes);
            escala.setPlantoes(plantoes);
        }

        reset();
        return escala;
    }

    private void reset() {
        nome = null;
        mesReferencia = null;
        lider = null;
        setor = null;
        strategy = null;
        contexto = null;
    }
}


// Director para EscalaBuilder - garante ordem de construção e valida os passos.
// 
// Ordem obrigatória de construção:
// 1. definirDadosBasicos() - nome e mês de referência
// 2. definirEstrutura() - líder e setor
// 3. definirPlantoes() - estratégia de geração de plantões
// 
// O método build() só funciona se todos os passos obrigatórios foram executados.
// Chamadas fora de ordem ou repetidas lançam IllegalStateException.
class EscalaDirector {
    
    private final EscalaBuilder builder;
    
    // Estados de construção
    private boolean dadosBasicosDefinidos = false;
    private boolean estruturaDefinida = false;
    private boolean plantoesDefinidos = false;
    
    public EscalaDirector(EscalaBuilder builder) {
        this.builder = builder;
    }
    
    // Passo 1: Define dados básicos (nome e mês de referência).
    // Deve ser chamado primeiro.
    public EscalaDirector definirDadosBasicos(String nome, LocalDate mesReferencia) {
        if (dadosBasicosDefinidos) {
            throw new IllegalStateException(
                "Dados básicos já foram definidos. Evite chamadas repetidas."
            );
        }
        
        if (estruturaDefinida || plantoesDefinidos) {
            throw new IllegalStateException(
                "definirDadosBasicos() deve ser chamado primeiro, antes de definirEstrutura() ou definirPlantoes()."
            );
        }
        
        if (nome != null) {
            this.builder.withNome(nome);
        }
        if (mesReferencia != null) {
            this.builder.withMesReferencia(mesReferencia);
        }
        
        dadosBasicosDefinidos = true;
        return this;
    }
    
    // Passo 2: Define estrutura organizacional (líder e setor).
    // Deve ser chamado após definirDadosBasicos().
    public EscalaDirector definirEstrutura(Profissional lider, Setor setor) {
        if (!dadosBasicosDefinidos) {
            throw new IllegalStateException(
                "definirEstrutura() só pode ser chamado após definirDadosBasicos()."
            );
        }
        
        if (estruturaDefinida) {
            throw new IllegalStateException(
                "Estrutura já foi definida. Evite chamadas repetidas."
            );
        }
        
        if (plantoesDefinidos) {
            throw new IllegalStateException(
                "definirEstrutura() deve ser chamado antes de definirPlantoes()."
            );
        }
        
        if (lider != null) {
            this.builder.withLider(lider);
        }
        if (setor != null) {
            this.builder.withSetor(setor);
        }
        
        estruturaDefinida = true;
        return this;
    }
    
    // Passo 3: Define plantões (estratégia de geração).
    // Deve ser chamado após definirEstrutura().
    public EscalaDirector definirPlantoes(GeracaoPlantoesStrategy strategy, Map<?, Plantao> contexto) {
        if (!dadosBasicosDefinidos || !estruturaDefinida) {
            throw new IllegalStateException(
                "definirPlantoes() só pode ser chamado após definirDadosBasicos() e definirEstrutura()."
            );
        }
        
        if (plantoesDefinidos) {
            throw new IllegalStateException(
                "Plantões já foram definidos. Evite chamadas repetidas."
            );
        }
        
        if (strategy != null) {
            this.builder.withPlantoesStrategy(strategy, contexto);
        }
        
        plantoesDefinidos = true;
        return this;
    }
    
    // Constrói a escala.
    // Só funciona se todos os passos obrigatórios foram executados.
    public Escala build() {
        if (!dadosBasicosDefinidos) {
            throw new IllegalStateException(
                "build() não pode ser chamado sem definir os dados básicos. Chame definirDadosBasicos() primeiro."
            );
        }
        
        if (!estruturaDefinida) {
            throw new IllegalStateException(
                "build() não pode ser chamado sem definir a estrutura. Chame definirEstrutura()."
            );
        }
        
        if (!plantoesDefinidos) {
            throw new IllegalStateException(
                "build() não pode ser chamado sem definir os plantões. Chame definirPlantoes()."
            );
        }
        
        Escala escala = this.builder.build();
        
        // Reseta os estados após o build
        reset();
        
        return escala;
    }
    
    // Reseta os estados do director para permitir nova construção.
    private void reset() {
        dadosBasicosDefinidos = false;
        estruturaDefinida = false;
        plantoesDefinidos = false;
    }
}

// Exemplo de uso do EscalaDirector:
//
// EscalaBuilder builder = new EscalaBuilder(escalaRepository, plantaoRepository);
// EscalaDirector director = new EscalaDirector(builder);
//
// Escala escala = director
//     .definirDadosBasicos("Escala Janeiro 2026", LocalDate.of(2026, 1, 1))
//     .definirEstrutura(profissionalLider, setor)
//     .definirPlantoes(estrategia, contextoPlantoes)
//     .build();
//
// Tentativas de uso inválido lançam IllegalStateException:
// - Chamar definirEstrutura() antes de definirDadosBasicos()
// - Chamar definirPlantoes() antes de definirEstrutura()
// - Chamar build() sem completar todos os passos
// - Chamar o mesmo método duas vezes
