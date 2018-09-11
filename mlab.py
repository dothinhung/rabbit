import mongoengine
# mlab là file connect data, lần sau khi connect chỉ cần confix từ host-password
# mongodb://admin:admin123@ds243049.mlab.com:43049/muadongkhonglanh-c4e19
# mongodb://adminc4e19:adminc4e19@ds243049.mlab.com:43049/muadongkhonglanh-c4e19
# mongodb://<dbuser>:<dbpassword>@ds125272.mlab.com:25272/project-c4e19
# client = MongoClient("mongodb://user_name:user_password@SERVER_IP/prod-db")
# db = client['prod-db']


host = "ds125272.mlab.com"
port = 25272
db_name = "project-c4e19"
user_name = "exercise1"
password = "exercise1"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())