# Equivalência estrutural da Fase 8

As extrações estruturais precederam as correções comportamentais e foram
versionadas em commits independentes.

| Módulo | Símbolos extraídos | Resultado |
| --- | ---: | --- |
| `front_matter.py` | 1 classe e 3 funções | corpos executáveis idênticos |
| `links.py` | 2 funções | corpos executáveis idênticos |

As constantes específicas acompanharam seus módulos proprietários. O alias
público `FM_EXCLUSIONS` é transitório e evita que G-FM consulte um nome privado
entre módulos antes da extração do gate na Fase 9.

`validate_front_matter()` permanece deliberadamente no `__init__.py`, pois
implementa G-FM e pertence à Fase 9. Os reexports mantêm a compatibilidade dos
consumidores atuais; as três interceptações de `validate_links()` no teste do
pipeline foram migradas para o módulo no qual o nome é consultado.

As correções BEH-03, BEH-04 e BEH-05 não alteram schemas, dados controlados,
perfil Markdown nem política de gates.
