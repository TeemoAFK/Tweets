
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "6BDDg6utL2Rw6j7QkZkJBV2Ly"
csecret = "VObLerV1bM4rwIcvQaiQiw6n96BzOj3pWu3DEjD0CZwi9ZctHj"
atoken = "926742758-3fCnfJ79xHhYz8Ac63tTSkzAVCw2nL6PQmTnKxhD"
asecret = "H2ESTiycco5m3tDYgN3SenFde2V6bdyIyGp3TLPtWpWxu"

#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('script3')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['script3']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["#copaamerica","copa america","Semifinal","#argentina","#brasil","#chile","#peru"])
twitterStream.filter(locations=[-78.546291,-0.246991,-78.272463,-0.06841])