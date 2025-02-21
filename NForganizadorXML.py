import os
import shutil
import xml.etree.ElementTree as ET

def solicitar_caminho(mensagem):
    """Solicita ao usuário um caminho válido e verifica se ele existe."""
    while True:
        caminho = input(mensagem).strip()
        if os.path.exists(caminho):
            return caminho
        else:
             print("Caminho inválido. Tente novamente.")

def obter_dados_nota(caminho_arquivo):
    """ Lê o XML e tenta extrair as informações:
    - Nome da empresa
    - Data de emissão
    - Tipo de nota (Entrada/Saída) ou se é um Evento de NF-e   """
    try:
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()

        # Tratar  namespaces
        namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # Verificar se é um EVENTO (ex: Carta de Correção, Cancelamento)
        if root.tag.endswith("procEventoNFe"):
            return None, None, None, None, "Evento"

        # Tenta encontrar a NF-e dentro do XML
        inf_nfe = root.find(".//nfe:infNFe", namespace)
        if inf_nfe is None:
            print(f"⚠ Arquivo {caminho_arquivo} não é um XML de NF-e válido.")
            return None, None, None, None, None

        # Obtendo os dados principais
        empresa = root.find(".//nfe:emit/nfe:xNome", namespace)
        data_emissao = root.find(".//nfe:ide/nfe:dhEmi", namespace)  # Formato: YYYY-MM-DDTHH:MM:SS-03:00
        tipo_nf = root.find(".//nfe:ide/nfe:tpNF", namespace)  # Tipo da nota (0 = Entrada, 1 = Saída)

        if empresa is None or data_emissao is None or tipo_nf is None:
            return None, None, None, None, None

        empresa = empresa.text.strip()
        data = data_emissao.text[:10].replace("-", "")  # Extrai somente a data (YYYYMMDD)
        tipo_nf = tipo_nf.text.strip()

        # Define se é Entrada ou Saída
        tipo_nota = "Entrada" if tipo_nf == "0" else "Saída"

        ano, mes, dia = data[:4], data[4:6], data[6:8]

        return empresa, ano, mes, dia, tipo_nota

    except Exception as e:
        print(f"Erro ao ler {caminho_arquivo}: {e}")
        return None, None, None, None, None

def organizar_notas(pasta_origem, pasta_destino):
    
    """    Percorre os arquivos XML na pasta origem, extrai os dados e move para a pasta destino.
    Se for um Evento de NF-e, organiza na pasta "Eventos".    """
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivos_xml = [f for f in os.listdir(pasta_origem) if f.endswith(".xml")]

    if not arquivos_xml:
        print("Nenhum arquivo XML encontrado na pasta de origem.")
        return

    for arquivo in arquivos_xml:
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        empresa, ano, mes, dia, tipo_nota = obter_dados_nota(caminho_arquivo)

        if tipo_nota == "Evento":
         # Pasta para eventos de NF-e
            caminho_final = os.path.join(pasta_destino, "Eventos")
            os.makedirs(caminho_final, exist_ok=True)
            destino_final = os.path.join(caminho_final, arquivo)
            shutil.move(caminho_arquivo, destino_final)
            print(f"Evento NF {arquivo} movido para {destino_final}")

        elif empresa and ano and mes and dia and tipo_nota:
       # Criando estrutura de diretórios para notas fiscais normais
            caminho_final = os.path.join(pasta_destino, empresa, ano, mes, dia, tipo_nota)
            os.makedirs(caminho_final, exist_ok=True)
            destino_final = os.path.join(caminho_final, arquivo)
            shutil.move(caminho_arquivo, destino_final)
            print(f"Nota {arquivo} ({tipo_nota}) movida para {destino_final}")
        else:
            print(f"Não foi possível processar: {arquivo}")

if __name__ == "__main__":
    print("Organizador de Notas Fiscais XML")
    print("Este programa ajudará a organizar suas notas fiscais separando por empresa, data e tipo (Entrada/Saída/Eventos).\n")

     pasta_origem = solicitar_caminho("Digite o caminho da pasta onde estão os arquivos XML: ")
    pasta_destino = solicitar_caminho("Digite o caminho onde deseja salvar os arquivos organizados: ")

    organizar_notas(pasta_origem, pasta_destino)

    print("\nOrganização concluída!")
