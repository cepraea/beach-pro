# Confirmação contratual de `documents`

O repositório não contém um JSON Schema para o envelope completo de
`docs/registry/registro-documentos.yaml`. Essa ausência não autoriza descartar
entradas que não sejam mapeamentos.

Cada item aceito pelo estreitamento é posteriormente validado contra
`docs/contracts/schemas/documento.schema.json`. O tipo raiz desse contrato é
`object`. Portanto, um escalar em `documents[index]` não pode representar um
documento válido e deve produzir erro antes da validação de instância.

A correção não altera schemas nem dados controlados. Ela torna explícita a
falha que o estreitamento anterior ocultava e continua a percorrer os demais
itens para preservar diagnósticos verificáveis.
