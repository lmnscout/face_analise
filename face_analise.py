import boto3
import json

client = boto3.client('rekognition')
s3 = boto3.resource('s3')

def detecta_faces():
    faces_detectadas = client.index_faces(
        CollectionId = 'faces',
        DetectionAttributes = ['DEFAULT'],
        ExternalImageId = 'TEMPORARIA',
        Image = {
            'S3Object': {
                'Bucket': 'fa-imagens-lmnscout',
                'Name': '_analise.png',
            },
        }
    )
    return faces_detectadas

def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for imagem in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagem]['Face']['FaceId'])
    return faceId_detectadas

def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for id in faceId_detectadas:
        resultado_comparacao.append(
            client.search_faces(
                CollectionId = 'faces',
                FaceId = id,
                FaceMatchThreshold = 80,
                MaxFaces = 10,
            )
        )
    return resultado_comparacao

def compara_imagens2():
    resultado_comparacao = []
    resultado_comparacao.append(
        client.search_faces_by_image(
            CollectionId='faces',
            Image={
                'S3Object': {
                    'Bucket': 'fa-imagens-lmnscout',
                    'Name': '_analise.png',
                }
            },
            MaxFaces=10,
            FaceMatchThreshold=80,
        )
    )
    return resultado_comparacao

def gera_dados_json(resultado_comparacao):
    dados_json = []
    for i in resultado_comparacao:
        if(len(i.get('FaceMatches')) >= 1):
            perfil = dict(
                nome = i['FaceMatches'][0]['Face']['ExternalImageId'],
                similaridade = round(i['FaceMatches'][0]['Similarity'], 2)
                )
            dados_json.append(perfil)
    return dados_json

def publica_dados(dados_json):
    arquivo = s3.Object('fa-site-lmnscout', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))

def exclui_imagem_colecao(faceId_detectadas):
    client.delete_faces(
        CollectionId = 'faces',
        FaceIds = faceId_detectadas
    )

def main(event, context):
    faces_detectadas = detecta_faces()
    faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
    resultado_comparacao = compara_imagens(faceId_detectadas)
    # resultado_comparacao = compara_imagens2()
    dados_json = gera_dados_json(resultado_comparacao)
    publica_dados(dados_json)
    exclui_imagem_colecao(faceId_detectadas)
    # print(json.dumps(faces_detectadas, indent=4))
    # print(faceId_detectadas)
    print(json.dumps(resultado_comparacao, indent=4))
    # print(json.dumps(dados_json, indent=4))

