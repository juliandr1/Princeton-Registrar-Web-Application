class CourseDetails:
    def __init__(self, cls_details, crs_details, depts, profs):
        self._clsdetails = cls_details
        self._crsdetails = crs_details
        self._depts = depts
        self._profs = profs
    def get_clsdetails(self):
        return self._clsdetails
    def get_crsdetails(self):
        return self._crsdetails
    def get_depts(self):
        return self._depts
    def get_profs(self):
        return self._profs
