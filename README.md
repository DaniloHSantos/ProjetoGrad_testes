<h1 align="center"> Gerador de Imagens em GrayScale na resolução de 28x28 para treinamento de rede neural </h1>

Esse projeto é um teste simples para gerar imagens para o treino de uma rede neural. As imagens são geradas a partir do movimento do mouse que é salvo em imagens na resolução de 28x28 em GrayScale.

<h4 align="center"> 
    :construction:  Projeto em construção  :construction:
</h4>

### :hammer: Como utilizar

Primeiro de tudo você deve clonar o repositório para a sua máquina. Em seguida devem ser instaladas as dependências necessárias:

 - Python (3.12.8)
 - Um leitor de Notebooks Python (Pode ser tanto a extenção do VSCode quanto o próprio Jupyter Notebook)
 - OpenCV (Biblioteca para o Python)

Antes de gerar as imagens entre no diretório `GeradorDados\DataBase`. Nesse dirtório vão ter duas pastas nomeadas `Bold` e `Thin`. O programa vai gerar imagens nessas duas pastas. Em cada uma delas você deve criar pastas para abrigar as imagens geradas de acordo com as lables que você deseja. Por exemplo, nesse projeto já existem 4 lables, `SetaCima`, `SetaBaixo`, `SetaDireita` e `SetaEsquerda`. Existe uma pasta com cada um desses nomes em ambas as pastas `Bold` e `Thin`. Se deseja gerar imagens de mais classes crie em cada uma destas pastas uma nova pasta com o nome da classe que você deseja gerar.

Com as pastas prontas, acesse o notebook `GeradorDados.ipynb`.

Antes de executar o programa você deve alterar alguns dados na célula `Função Chamada para desenhar`. Esses dados são:
 - A variável `Contagem`: Por padrão 1 e deve ser deixada assim na primeira utilização, mas quando algumas imagens ja forem geradas deve ser alterado para um número maior para que o programa não subistitua imagens já geradas.
  - A variável `LableImage`: Essa variável deve ser alterada para a lable desejada para as imagens geradas. É recomendado que as imagens geradas na mesma execução tenham a mesma lable pois na aplicação não é possível mudar o nome nem o caminho em que elas seram salvas.
  
É esperado que após cada execução sejam alteradas as variáveis `LableImage` e `Contagem` para melhor organização e para poder salvar as imagens nos caminhos corretos.

Rode o código e uma janela irá abrir aonde, com o clique do botão esquerdo do mouse, você poderá desenhar o padrão que quiser.

Enquando a janela estiver aberta existem 3 comandos possíveis com as teclas do teclado:

 - `Q`: Fecha a janela e encerra o programa.
 - `S`: Salva duas versões do desenho nas pastas da Lable selecionada em `Bold` e `Thin`.
 - `R`: Limpa a tela de desenho para que um novo desenho possa ser feito.

### Tecnologias Utilizadas

 - `Python`
 - `Jupyter Notebook`

### Autores

| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/117547163?v=4" width=115><br><sub>Danilo Honorio dos Santos</sub>](https://github.com/DaniloHSantos) |
| :---: |