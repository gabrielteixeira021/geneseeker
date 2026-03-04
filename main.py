"""
GeneSeeker - Identificador de ORFs

Propósito: Identificar Open Reading Frames (ORFs) em sequências de DNA
analisando os 3 quadros de leitura possíveis.

Um ORF é uma sequência de DNA que começa com um códon de início (ATG)
e termina com um códon de parada (TAA, TAG ou TGA).
"""

import argparse
from geneseeker import sequence, orf_finder, reporter, utils


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace: # type: ignore
    """
    Define e processa os argumentos da linha de comando.

    Argumentos esperados:
        input       Caminho para o arquivo FASTA de entrada (obrigatório).
        --output    Caminho para o arquivo de saída (opcional).
        --min-len   Tamanho mínimo de ORF em pares de bases (padrão: 100).
        --format    Formato do relatório de saída: 'text', 'csv' ou 'json' (padrão: 'text').

    Returns:
        argparse.Namespace: Objeto com os valores dos argumentos.

    TODO:
    - Criar o parser com argparse.ArgumentParser.
    - Adicionar todos os argumentos descritos acima.
    - Retornar parser.parse_args().
    """
    pass


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def load_sequences(input_path: str) -> dict: # type: ignore
    """
    Lê e valida as sequências do arquivo FASTA de entrada.

    Fluxo esperado:
        1. Chamar sequence.read_fasta() para carregar as sequências.
        2. Chamar sequence.validate_sequence() em cada sequência carregada.
        3. Chamar utils.clean_sequence() para normalizar cada sequência válida.
        4. Retornar o dicionário {id: sequência_limpa} pronto para análise.

    Args:
        input_path (str): Caminho do arquivo FASTA.

    Returns:
        dict: Dicionário {id_sequencia: sequencia_normalizada}.

    TODO:
    - Implementar o fluxo descrito acima.
    - Emitir aviso (ou ignorar) sequências que falhem na validação.
    """
    pass


def run_analysis(sequences: dict, min_len: int) -> list: # type: ignore
    """
    Executa a identificação de ORFs em todas as sequências carregadas.

    Fluxo esperado:
        1. Iterar sobre cada sequência do dicionário.
        2. Chamar orf_finder.find_orfs() passando a sequência e min_len.
        3. Para cada ORF encontrada, chamar orf_finder.translate_orf() e
           anexar a tradução ao objeto/dicionário da ORF.
        4. Acumular e retornar a lista completa de ORFs de todas as sequências.

    Args:
        sequences (dict): Dicionário {id_sequencia: sequencia}.
        min_len (int): Comprimento mínimo em pares de bases.

    Returns:
        list: Lista de todas as ORFs identificadas (com tradução incluída).

    TODO:
    - Implementar o fluxo descrito acima.
    """
    pass


def output_results(orfs: list, format_type: str, output_path: str | None) -> None:
    """
    Formata, exibe e (opcionalmente) salva os resultados.

    Fluxo esperado:
        1. Chamar reporter.display_summary() para imprimir o resumo no terminal.
        2. Chamar reporter.format_output() para obter a string formatada.
        3. Se output_path foi fornecido, chamar reporter.save_results() para
           gravar o arquivo; caso contrário, imprimir no stdout.

    Args:
        orfs (list): Lista de ORFs resultante de run_analysis().
        format_type (str): Formato de saída ('text', 'csv', 'json').
        output_path (str | None): Caminho do arquivo de saída, ou None.

    TODO:
    - Implementar o fluxo descrito acima.
    """
    pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Ponto de entrada principal do GeneSeeker.

    Orquestra o pipeline completo:
        1. parse_args()        — processa os argumentos da CLI.
        2. load_sequences()    — lê, valida e limpa as sequências FASTA.
        3. run_analysis()      — identifica ORFs e traduz as sequências.
        4. output_results()    — formata e exibe/salva os resultados.

    TODO:
    - Chamar as funções na ordem acima, passando os argumentos corretos.
    - Encapsular a execução em try/except para tratar erros de I/O e
      sequências inválidas de forma amigável.
    """
    pass


if __name__ == "__main__":
    main()



