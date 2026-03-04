# GeneSeeker — Modelagem do Sistema

## 1. Diagrama de Componentes

```mermaid
graph TD
    subgraph CLI["CLI — main.py"]
        PA[parse_args]
        LS[load_sequences]
        RA[run_analysis]
        OR[output_results]
        MAIN[main]
    end

    subgraph SEQ["geneseeker/sequence.py"]
        RF[read_fasta]
        VS[validate_sequence]
    end

    subgraph UTL["geneseeker/utils.py"]
        CS[clean_sequence]
        RC[get_reverse_complement]
    end

    subgraph ORF["geneseeker/orf_finder.py"]
        FO[find_orfs]
        TR[translate_orf]
    end

    subgraph REP["geneseeker/reporter.py"]
        DS[display_summary]
        FMT[format_output]
        SR[save_results]
    end

    FASTA[(Arquivo FASTA\ninput)]
    OUT[(Arquivo de saída\ntext / csv / json)]
    STDOUT[Terminal stdout]

    MAIN --> PA
    MAIN --> LS
    MAIN --> RA
    MAIN --> OR

    LS --> RF
    LS --> VS
    LS --> CS

    RA --> FO
    RA --> TR
    FO --> RC

    OR --> DS
    OR --> FMT
    OR --> SR

    FASTA --> RF
    SR --> OUT
    DS --> STDOUT
    FMT --> STDOUT
```

## 2. Diagrama de Sequência — Pipeline Principal

```mermaid
sequenceDiagram
    actor User
    participant CLI as main.py
    participant SEQ as sequence.py
    participant UTL as utils.py
    participant ORF as orf_finder.py
    participant REP as reporter.py

    User->>CLI: python main.py genome.fasta --min-len 100 --format csv

    CLI->>CLI: parse_args()
    CLI->>SEQ: read_fasta(input_path)
    SEQ-->>CLI: {id: raw_sequence, ...}

    loop Para cada sequência
        CLI->>SEQ: validate_sequence(seq)
        SEQ-->>CLI: True / False
        CLI->>UTL: clean_sequence(seq)
        UTL-->>CLI: sequência normalizada
    end

    CLI->>ORF: find_orfs(sequence, min_len)
    Note over ORF,UTL: find_orfs chama get_reverse_complement\npara analisar a fita reversa
    ORF->>UTL: get_reverse_complement(sequence)
    UTL-->>ORF: complemento reverso
    ORF-->>CLI: [lista de ORFs]

    loop Para cada ORF
        CLI->>ORF: translate_orf(orf_sequence)
        ORF-->>CLI: sequência de aminoácidos
    end

    CLI->>REP: display_summary(orfs)
    REP-->>User: resumo no terminal

    CLI->>REP: format_output(orfs, format_type)
    REP-->>CLI: string formatada

    alt output_path fornecido
        CLI->>REP: save_results(output, output_path)
        REP-->>User: arquivo salvo
    else sem output_path
        CLI-->>User: imprime no stdout
    end
```

## 3. Diagrama de Classes / Módulos

```mermaid
classDiagram
    class main {
        +parse_args() Namespace
        +load_sequences(input_path: str) dict
        +run_analysis(sequences: dict, min_len: int) list
        +output_results(orfs: list, format_type: str, output_path: str) None
        +main() None
    }

    class sequence {
        +read_fasta(file_path: str) dict
        +validate_sequence(sequence: str) bool
    }

    class utils {
        +clean_sequence(sequence: str) str
        +get_reverse_complement(sequence: str) str
    }

    class orf_finder {
        +find_orfs(sequence: str, min_length: int) list
        +translate_orf(orf_sequence: str) str
    }

    class reporter {
        +display_summary(orfs: list) None
        +format_output(orfs: list, format_type: str) str
        +save_results(formatted_output: str, output_path: str) None
    }

    main --> sequence : usa
    main --> utils : usa
    main --> orf_finder : usa
    main --> reporter : usa
    orf_finder --> utils : usa (complemento reverso)
```

## 4. Estrutura de Dados — Objeto ORF

Cada ORF identificada por `find_orfs()` é representada como um dicionário:

```mermaid
classDiagram
    class ORF {
        +sequence_id: str
        +start: int
        +end: int
        +frame: int
        +strand: str
        +dna_sequence: str
        +length: int
        +translation: str
    }
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `sequence_id` | `str` | Identificador da sequência FASTA de origem |
| `start` | `int` | Posição de início na sequência original (0-based) |
| `end` | `int` | Posição de fim (exclusive) na sequência original |
| `frame` | `int` | Quadro de leitura: `0`, `1` ou `2` |
| `strand` | `str` | Fita: `'+'` (direta) ou `'-'` (reversa) |
| `dna_sequence` | `str` | Sequência de DNA da ORF (ATG...STOP) |
| `length` | `int` | Comprimento em pares de bases |
| `translation` | `str` | Sequência de aminoácidos resultante |

## 5. Diagrama de Fluxo — `find_orfs()`

```mermaid
flowchart TD
    A([Início: find_orfs]) --> B[Obter complemento reverso\nget_reverse_complement]
    B --> C{Para cada fita\nforward e reverse}
    C --> D[Frame 0, 1 e 2]
    D --> E[Varrer a sequência\nprocurando ATG]
    E --> F{ATG encontrado?}
    F -- Não --> E
    F -- Sim --> G[Registrar posição de início\navar em busca de códon STOP]
    G --> H{TAA / TAG / TGA\nencontrado?}
    H -- Não --> G
    H -- Sim --> I[Calcular comprimento da ORF]
    I --> J{len >= min_length?}
    J -- Não --> E
    J -- Sim --> K[Adicionar ORF à lista]
    K --> E
    E --> L([Retornar lista de ORFs])
```

## 6. Mapa de Dependências de Arquivos

```mermaid
graph LR
    M[main.py]
    SQ[sequence.py]
    UT[utils.py]
    OF[orf_finder.py]
    RP[reporter.py]
    IN[__init__.py]

    M --> SQ
    M --> UT
    M --> OF
    M --> RP
    OF --> UT
    IN -.-> SQ
    IN -.-> OF
    IN -.-> RP
    IN -.-> UT
```

## 7. Visão Geral dos Dados de Teste

```mermaid
mindmap
  root((test_data/))
    ORFs conhecidas
      01–10: 3 ORFs por arquivo
      16–25: multi-ORFs\n4-8 ORFs
    Sem ORFs
      11–15: zero ORFs
    Por tamanho
      26–30: sequências curtas
      31–35: sequências longas
    Por frame
      36–39: apenas frame 0
      40–43: apenas frame 1
      44–47: apenas frame 2
    Multi-sequências
      48+: múltiplas entradas\nno mesmo FASTA
```
