from ..models.autenticacion.m_authe import AuthService 
mod_login = AuthService()
class Logincontroller():
    def c_login_credentials(self, users):
        data= mod_login.login_user(users)
        return data
    
    
    def c_login_credentials_faces(self, id_face_identy):
        data= mod_login.login_user_id_face(id_face_identy)
        return data
    
    
 