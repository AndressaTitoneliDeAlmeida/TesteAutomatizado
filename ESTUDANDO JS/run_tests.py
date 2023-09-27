import requests
import json
import os
import subprocess
import pprint


# ID da collection e a chave de acesso key
collection_id = "28806666-f5828280-7332-4874-b2e8-030066db6f0b"
access_key = "PMAK-64caa072cffd9900387e3f49-d933ab116fb057626da68870ae1a1e2ae4"

# Mapeamento entre a pasta da request do Postman e o caminho para o arquivo CSV (localhost)
request_csv_mapping = {
    "1.1 Cadastro de Motorista cuja situação é aguardando análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.1_CONTEXTO.csv",
    "1.2 Cadastro de Motorista cuja situação deve ser diferente de aguardando análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.2_CONTEXTO.csv",
    "2.1 Cadastro de Veículo cuja situação deve ser aguardando análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.1_CONTEXTO.csv",
    "2.2 Cadastro de Veículo cuja situação deve ser diferente de aguardando análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.2_CONTEXTO.csv",
    "3.1 Cadastro do Conjunto cuja situação deve ser aguardando análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\3.1_CONTEXTO.csv",
    "3.2 Cadastro do Conjunto cuja situação deve ser aguardando análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\3.2_CONTEXTO.csv",
    "1.1 Consulta de Obj não Cadastrado": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.1_Consulta_de_Objeto_nao_Cadastrado.csv",
    "1.2 Consulta de Obj com Cadastro Inválido": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.2_Consulta_de_Objeto_com_Cadastro_Invalido.csv",
    "1.3 Consulta de Obj Aguardando Análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.3_Consulta_de_Objeto_Aguardando_Analise.csv",
    "1.4 Consulta de Obj Não Recomendado": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.4_Consulta_de_Objeto_nao_Recomendado.csv",
    "1.5 Consulta de Obj Recomendado": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\1.5_Consulta_de_Objeto_Recomendado.csv",
    "2.1 Consulta de Conjunto não Cadastrado": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.1_Consulta_de_Conjunto_nao_Cadastrado.csv",
    "2.2 Consulta de Conjunto com Cadastro Inválido": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.2_Consulta_de_Conjunto_com_Cadastro_Invalido.csv",
    "2.3 Consulta de Conjunto Aguardando Análise": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.3_Consulta_de_Conjunto_Aguardando_Analise.csv",
    "2.4 Consulta de Conjunto não Recomendado": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.4_Consulta_de_Conjunto_nao_Recomendado.csv",
    "2.5 Consulta de Conjunto Recomendado": r"C:\Users\AndressaTitonelideAl\Desktop\TESTE_SCRIPT\2.5_Consulta_de_Conjunto_Recomendado.csv",
}

# Função para executar o teste do request e CSV
def run_test(request_name, csv_path):
    print(f"Executando request: {request_name}")
    command = f"npx newman run https://api.postman.com/collections/28806666-f5828280-7332-4874-b2e8-030066db6f0b?apikey=PMAK-64caa072cffd9900387e3f49-d933ab116fb057626da68870ae1a1e2ae4 --folder '{request_name}' --env-var 'caminho_para_csv={csv_path}'"
    print(f"Comando: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")
    print("Resultado:")
    pprint.pprint(result)
    
    if result.stdout:
        print("Output:")
        print(result.stdout)
        try:
            json_output = json.loads(result.stdout)
            pprint.pprint(json_output)
            with open(f"{request_name}_report.txt", "w", encoding="utf-8") as report_file:
                report_file.write(result.stdout)
        except json.decoder.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print("A saída do comando não possui um formato JSON válido.")
    else:
        print("Nenhum resultado retornado.")
        
    if result.stderr:
        print("Erro padrão (stderr):")
        print(result.stderr)
    if result.returncode != 0:
        print(f"Ocorreu um erro na execução do Newman. Código de retorno: {result.returncode}")


# Obtém a coleção do Postman
response = requests.get(f"https://api.postman.com/collections/28806666-f5828280-7332-4874-b2e8-030066db6f0b?apikey=PMAK-64caa072cffd9900387e3f49-d933ab116fb057626da68870ae1a1e2ae4")

# Verifica se a resposta obteve sucesso
if response.status_code == 200:
    collection_data = response.json()
    print(json.dumps(collection_data, indent=2))  # Imprime os dados da coleção
    # Itera sobre as requests da coleção
    for item in collection_data.get("collection", {}).get("item", []):
        request_name = item.get("name")
        if request_name in request_csv_mapping:
            csv_path = request_csv_mapping[request_name]
            run_test(request_name, csv_path)
        else:
            print(f"AVISO: Não foi encontrado um arquivo CSV mapeado para a request '{request_name}'.")
else:
    print(f"Erro ao obter a coleção. Código de status: {response.status_code}")
    print(response.text)
