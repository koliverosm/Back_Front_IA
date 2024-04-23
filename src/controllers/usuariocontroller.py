from ..models.m_usuario import Usuario
#mod_login = User_login()
mod_usuario = Usuario()


class Usuariocontroller():
    def c_validate(self, json):
        data = mod_usuario.validate(json)
        return data

    def c_crear_usuario(self, json):
        data = mod_usuario.crear_usuario(json)
        return data

    def c_crear_usuario_admin(self, json):
        data = mod_usuario.crear_user_admin(json)
        return data

    def c_consultar_usuarios(self):
        data = mod_usuario.m_consultar_usuarios()
        return data

    def c_consultar_usuario_id(self):
        query = mod_usuario.m_consultar_usuario_id()
        return query

    def c_actualizar_usuario_id(self):
        query = mod_usuario.m_actualizar_usuario()
        return query

    def c_bajar_usuario(self):
        query = mod_usuario.m_bajar_usuario()
        return query
