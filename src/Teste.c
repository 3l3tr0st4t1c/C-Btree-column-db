#include "database.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

int main() {
    const char *db_nome = "banco.dat";
    int i;
    int falhas = 0;

    printf("--- MONGOLDB STRESS TEST (V2 COLUNAR) ---\n");

    remove(db_nome);
    if (Inicializar_Banco(db_nome) == 0) {
        printf("[OK] Banco inicializado com sucesso.\n");
    } else {
        printf("[INFO] Banco ja existia ou erro na criacao.\n");
    }

    printf("[FASE 1] Inserindo 5000 pedidos colunares...\n");
    for (i = 1; i <= 5000; i++) {
        // Criando pacotes de dados simulando a API do iFood
        ColunaCliente c;
        memset(&c, 0, sizeof(ColunaCliente));
        c.idCliente = i;
        sprintf(c.nome, "Cliente Numero %d", i);

        ColunaFinanceiro f;
        memset(&f, 0, sizeof(ColunaFinanceiro));
        f.valorBruto = i * 200; // Simulando R$ 2,00 em centavos

        ColunaEntrega e;
        memset(&e, 0, sizeof(ColunaEntrega));
        sprintf(e.logradouro, "Rua do Teste %d", i);

        ColunaStatus s;
        memset(&s, 0, sizeof(ColunaStatus));
        s.displayID = i;
        s.status = 1; // Status confirmado
        s.momentoEntrada = time(NULL);

        // Inserção enviando os blocos estruturados
        if (Inserir_Pedido(db_nome, &c, &f, &e, &s) != 0) {
            printf("[ERRO] Falha ao inserir ID %d\n", i);
            falhas++;
        }
    }

    if (falhas == 0) {
        printf("[SUCESSO] Todos os 5000 pedidos foram inseridos nas 4 colunas.\n");
    } else {
        printf("[ALERTA] Ocorreram %d falhas durante a insercao.\n", falhas);
    }

    // Busca de Dados
    printf("[FASE 2] Verificando integridade das chaves e extents...\n");
    falhas = 0;
    for (i = 1; i <= 5000; i++) {
        EnderecoColunar res = Buscar_Pedido(db_nome, i);

        // Se o bloco de inicio for 0, o Extent falhou e o ID não foi achado
        if (res.col_cliente.bloco_inicio == 0) {
            printf("[ERRO] ID %d nao foi encontrado pela busca!\n", i);
            falhas++;
        }
    }

    if (falhas == 0) {
        printf("[STATUS FINAL] TESTE V2 CONCLUIDO COM 100%% DE SUCESSO!\n");
    } else {
        printf("[STATUS FINAL] Teste falhou com %d erros de busca/integridade.\n", falhas);
    }

    return 0;
}
