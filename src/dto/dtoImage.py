class ImagenDTO:
    def __init__(self, _namefile, _datafile, _id_face):
        self._namefile = _namefile
        self._datafile = _datafile
        self._id_face = _id_face

    @property
    def get_namefile(self):
        return self._namefile

    @get_namefile.setter
    def namefile(self, value):
        self._namefile = value

    @property
    def get_datafile(self):
        return self._datafile

    @get_datafile.setter
    def datafile(self, value):
        self._datafile = value

    @property
    def get_id_face(self):
        return self._id_face

    @get_id_face.setter
    def id_face(self, value):
        self._id_face = value


   
