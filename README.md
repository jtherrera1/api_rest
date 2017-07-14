## Jose Talavera Herrera
Desafio de semântica
================

Um dos nossos maiores desafios aqui na globo.com é a categorização e a recomendação de conteúdo. Para melhorar a experiência em nossos sites, buscamos aperfeiçoar continuamente a nossa capacidade de entregar matérias e vídeos relevantes de forma personalizada para nossos usuários.

Há várias estratégias de recomendação. Uma das mais comuns é agrupar conteúdos sobre assuntos afins em uma oferta conjunta. Para tal, é necessário que antes saibamos o que há nos textos, vídeos e imagens que produzimos.

O Desafio
---

Você deverá criar uma aplicação web capaz de extrair entidades ([Named-entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)) de textos postados através de uma [API REST](http://www.restapitutorial.com/). **Não é obrigatória** a etapa de classificação automática das entidades, mas uma **atividade bônus** seria categorizá-las de acordo com suas entradas na [DBpedia](http://wiki.dbpedia.org).  No projeto, há um arquivo JSON com algumas matérias e suas entidades que podem ser usadas como casos de teste.

Exemplo de JSON a ser enviado para a API:
```json
{
    "title": "Título da matéria",
    "subtitle": "Subtítulo",
    "body": "Corpo da matéria",
    "tenant": "produto",
    "url": "http://produto.globo.com/teste/exemplo.html"
}
```

Requisição:
```bash
curl -XPOST 'http://localhost:8080/api/' -H "Content-Type: application/json" -d @exemplo.json
```
A resposta deverá ser um JSON no formato que achar conveniente, contendo os itens identificados e os dados que considerar relevantes.


Criação e instalação do projeto
---
- Você deverá usar este repositório para desenvolver seu projeto, ou seja, todos os seus commits devem estar registrados aqui. Queremos ver como você trabalha.
- O programa pode ser feito na linguagem de sua preferência.
- A aplicação deverá funcionar no Ubuntu 16.04 ou no macOS.
- Sua instalação deverá ter o menor número possível de passos manuais (recomendamos make ou bash script para automatizar o processo).
- Considere, caso necessário, que já possuímos MySQL, Java, Ruby e Python em nossas máquinas.


Dicas
---
- Procure registrar todas as suas ideias (mesmo que não aproveitadas), seus passos e os motivos que embasaram suas decisões.
- Admita que o serviço não precisará atender requisições simultâneas.
- Gostamos de performance 😀 , testes automatizados 😀😀 e código claro, bem modularizado 😀😀😀
- Caso tenha alguma dúvida, entre em contato conosco.

Boa sorte!

Instalação de Dependências
---
1. Executar o archivo install.sh. Se for necessario, dar os permisos de execução com: chmod ugo+x install.sh
``` 
./install.sh
```

API REST
---
1. Primeir executar o archivo process/mediator.py
``` 
python process/mediator.py
```

Exemplos de requisições
---
```bash
curl -H "Content-Type: application/json" -X POST -d @example.json http://localhost:5000/todo/api/v1.0/nltk_entities 
curl -H "Content-Type: application/json" -X POST -d @example.json http://localhost:5000/todo/api/v1.0/nltk_process
curl -H "Content-Type: application/json" -X POST -d @example.json http://localhost:5000/todo/api/v1.0/polyglot_entities
curl -H "Content-Type: application/json" -X POST -d @example.json http://localhost:5000/todo/api/v1.0/polyglot_process
```
Saida para "api/\*_entities:
```json
{
	"results": "entity1", "entity2"
}
```

Execução dos Testes
---
1. Ingresar no diretorio tests :
```
cd tests
```
2. Executar tests/execute_test.sh. Se for necessario, dar os permisos de execução com: chmod ugo+x e executar execute_test.sh
```
./execute_test.sh
```

