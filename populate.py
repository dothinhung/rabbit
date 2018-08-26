import mlab
from models.user import User

mlab.connect()

new_user = User(
    fname = "Nhung",
    email = "nhung11296@gmail.com",
    uname = "nhung",
    password = "123456"
)

new_user.save()