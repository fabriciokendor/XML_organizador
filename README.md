Esse arquivo que organiza XMl está em constante aperfeiçoamento

As maiores dificuldades que tive em desenvolver esse script foi testar as bibliotecas xml.etree.ElementTree e Shutil.
Biblioteca xml tive que entender o funcionamento de como ela se comportava ao pesquisar o XMl.
um erro que levou um bom tempo para descobrir foi o espaçamento dos nomes nos xmls que não tinha no início das Nf-e.

Os XMLS consistes em 
- NF-e
- CT-e
- Cupom fiscal
- Eventos

Motivo do desenvolvimento:
Trabalho comom TI em um escritório de contabilidade, vendo a dificuldade na hora da importação de arquivos XMLs por parte 
dos usuários que perdiam muito tempo organizando os arquivos para separar em entrada saída e eventos,
resolvi desenvolver esse perqueno script em Python para organizar os Xmls e facilitar a importação dos mesmos.

Pontos a serem melhorados:
1 - quando o nome da empresa está em um caps diferente ele coloca em outra pasta Exemplo: EMPRESA1 , empresa1 
Como melhorar: Criar um método de ignorar o Caps ou usa ro CNPJ com o chave.
Criar por CNPJ é mais fácil.

2 - criar uma interface amigável para que todos os usuários possam executar e colocar tudo em um pacote de instalação.

Fabricio Rodrigues 2025.
