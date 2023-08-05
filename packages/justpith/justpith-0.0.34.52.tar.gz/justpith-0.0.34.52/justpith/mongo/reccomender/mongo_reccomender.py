from ..mongo import Mongo

class MongoReccomender(Mongo):
    def __init__(self,host, port, db):
        super(MongoReccomender,self).__init__(host, port, db)

    def update_user_raccomandation(self, user_id, new_raccomandations, category):
        collection_name = "Raccomandations_"+category
        selected_collection = self.connection[collection_name]
        for id_news, weight in new_raccomandations.iteritems():
            selected_collection.update({'_id': str(user_id)}, {'$set': {'raccomandations.'+str(id_news): weight}}, upsert=True)