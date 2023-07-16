class EDO_partipicant:
    EDO_partipicants = {
        '7706664260': '2BM-5029112443-643902001-201809170824291744204',
        '7721247141': '2BM-1624014670-162401001-201704130206443850414'
    }

    @classmethod
    def get_edo_partipicant(cls, INN):
        return cls.EDO_partipicants[INN]
