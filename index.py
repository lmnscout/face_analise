
import boto3

s3 = boto3.resource('s3')
client = boto3.client('rekognition')

def lista_imagens():
    imagens=[]
    bucket = s3.Bucket('fa-imagens-lmnscout')
    for imagem in bucket.objects.all():
        imagens.append(imagem.key)
    return imagens

def cria_colecao():
    response = client.create_collection(
    CollectionId = 'faces'
)

def deleta_colecao():
    response = client.delete_collection(
    CollectionId = 'faces'
)

def indexa_colecao(imagens):
    for i in imagens:
        response = client.index_faces(
            CollectionId = 'faces',
            DetectionAttributes = [],
            ExternalImageId = i[:-4],
            Image = {
                'S3Object': {
                    'Bucket': 'fa-imagens-lmnscout',
                    'Name': i, 
                },
            },
        )


imagens = lista_imagens()
# deleta_colecao()
cria_colecao()
indexa_colecao(imagens)
print(imagens)
