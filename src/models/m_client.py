
class Id_Face():

    def __init__(self, id_face_identy) -> None:
        self.__id_face_identy = id_face_identy

    def get_id_faces_identy(self):
        return self.__id_face_identy

    def set_id_faces_identy(self, id_faces_identy):
        self.__id_face_identy = id_faces_identy


class UserFile():

    def __init__(self, username, password, email) -> None:
        self._username = username
        self._password = password
        self._email = email

    @property
    def get_username(self):
        return self._username

    @get_username.setter
    def username(self, value):
        self._username = value

    @property
    def get_password(self):
        return self._password

    @get_password.setter
    def password(self, value):
        self._password = value

    @property
    def get_email(self):
        return self._email

    @get_email.setter
    def email(self, value):
        self._email = value


class User_login():

    def __init__(self, id, username, password,  roles) -> None:
        self.__id = id
        self.__username = username
        self.__password = password
        self.__roles = roles
  
    
    def user_validated(self, id,  username, password,  roles):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__roles = roles

##### GETTER AND SETTER #####
    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_fullname(self):
        return self.__fullname

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def get_roles(self):
        return self.__roles
    def get_email(self):
        return self.__email