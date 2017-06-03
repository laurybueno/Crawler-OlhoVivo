# Crawler Olho Vivo
Este projeto é um crawler simples para a v0 da API Olho Vivo da SPTrans. Ele faz, uma vez por minuto, uma requisição para cada linha de ônibus cadastrada no arquivo `routes.txt`.

Requisições serão distribuídas em threads. Cada uma fica responsável por fazer 100 chamadas ao servidor da SPTrans.

Em média, todas as solicitações são respondidas em menos de 15 segundos.

## Notas de uso
Coloque sua chave de acesso na variável de ambiente `API_KEY`.

As linhas de ônibus existentes na cidade devem ser especificadas pelo arquivo `routes.txt` contido no pacote GTFS atualizado diariamente pela SPtrans.

Arquivos JSON recebidos da API serão salvos em `/data`. Você provavelmente vai querer montar essa pasta como um volume.
