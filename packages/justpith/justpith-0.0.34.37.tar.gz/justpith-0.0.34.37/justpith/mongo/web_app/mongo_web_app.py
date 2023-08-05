from ..mongo import Mongo

class MongoWebApp(Mongo):
    def __init__(self,host, port, db):
        super(MongoWebApp,self).__init__(host, port, db)


    def get_news_reccomandations(self, user_id):
        selected_collection = self.connection["Users"]
        result = selected_collection.find_one({"_id": str(user_id)},{"raccomandations":1})
        selected_collection = self.connection["News"]
        racc_list = []
        for id_news, weight in result["raccomandations"].iteritems():
            racc_news = {}
            news = selected_collection.find_one({"_id": int(id_news)})
            racc_news["_id"] = id_news
            racc_news["weight"] = weight
            #print(str(news)+" id:"+id_news+" weight:"+str(weight))
            racc_news["category_title"] = news["category_title"]
            racc_news["news_source"] = news["news_source"]
            racc_news["url"] = news["url"]
            racc_news["article"] = news["article"]
            racc_news["title"] = news["title"]
            racc_list.append(racc_news)

        return racc_list


    def get_news_for_learning(self, category, user_id):
        id_news_for_learning = []
        news_for_learning = []

        selected_collection = self.connection["ControllerCurrent"]
        result = selected_collection.find_one({}, {category: 1})

        id_current_jobs = result[category]
        if id_current_jobs != 0:
            pass

        selected_collection = self.connection["Indexes"]
        result = selected_collection.find_one({"_id": id_current_jobs}, {"id_to_idcorpus":1})

        news_in_current_model = result["id_to_idcorpus"]

        selected_collection = self.connection["NewsVotes"]
        for elem in news_in_current_model:
            id_news = news_in_current_model[elem]
            vote_register = selected_collection.find_one({"_id": id_news}, {"register":1})

            if vote_register is not None and str(user_id) in vote_register["register"]:
                continue
            else:
                id_news_for_learning.append(id_news)

        selected_collection = self.connection["News"]
        for elem in id_news_for_learning:
            result = selected_collection.find_one({"_id":elem}, {"article":1, "category_title":1, "title":1, "url":1, "_id":1})
            news_for_learning.append(result)

        return news_for_learning