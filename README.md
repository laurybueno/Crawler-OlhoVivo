# Crawler Olho Vivo
Este projeto é um crawler simples para a v0 da API Olho Vivo da SPTrans. Ele faz, uma vez por minuto, uma requisição para cada linha de ônibus cadastrada no arquivo `routes.txt`.

Requisições serão distribuídas em threads. Cada uma fica responsável por fazer 100 chamadas ao servidor da SPTrans.

Em média, todas as solicitações são respondidas em menos de 15 segundos.

# Execução
O método recomendado para rodar este software é via Docker. A imagem pode ser encontrada [aqui](https://hub.docker.com/r/laury/crawler-olhovivo/).

## Notas de uso
Coloque sua chave de acesso na variável de ambiente `API_KEY`.

As linhas de ônibus existentes na cidade devem ser especificadas pelo `routes.txt` contido no pacote GTFS atualizado diariamente pela SPTrans. Esse arquivo deve ser montado no container em `/data/gtfs/routes.txt`.

Arquivos JSON recebidos da API serão salvos em `/data`. Você provavelmente vai querer montar essa pasta como um volume.
