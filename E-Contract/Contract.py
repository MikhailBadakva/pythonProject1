from TypElemList import type_elements
from UnitStyle import Style, Styles
from FreeTextUnit import FreeTextUnit
from MachineProcessingUnit import MachineProcesingUnit
from EDOParticipant import EDO_partipicant
import xml.etree.ElementTree as ET
import datetime
import docx
import re
import uuid


class Contract:
    R_Т = 'ON_SODSD'
    Form_version = '1.01'
    Program_version = '0.1'
    Typical_elemnents_list_version ='00.01'

    def __init__(self, context_contr_name, context_contr_id, context_contr_date, INN1, INN2):
        now = datetime.datetime.now()
        self.file_tag = 'Файл'
        self.file_attributes = {'ИдФайл': Contract.create_file_id(INN1, INN2),
                          'ВерсФорм': self.Form_version,
                          'ВерсПрог': self.Program_version,
                          'ВерсПеречня': self.Typical_elemnents_list_version}
        self.context_tag = 'Содержание'
        self.context_attributes = {'КНД': '1175016',
                             'НаимДок': context_contr_name,
                             'НомДок': context_contr_id,
                             'ДатаДок': context_contr_date,
                             'ДатаИнфСодСд': now.strftime("%d.%m.%Y"),
                             'ВремИнфСодСд': now.strftime("%H.%M.%S"),
                             'ПризнИн': '0',
                             'ПорФормДок': '2'}
        self.INN1 = ('ИННЮДСт1', INN1)
        self.INN2 = ('ИННЮДСт1', INN2)
        self.units = []
        self.styles = []

    @classmethod
    def create_file_id(cls, INN1, INN2):
        now = datetime.datetime.now()
        a = EDO_partipicant.get_edo_partipicant(INN1)
        o = EDO_partipicant.get_edo_partipicant(INN2)
        ggggmmdd = now.strftime("%Y%m%d")
        k1 = uuid.uuid4()
        k2 = '1'
        k3 = '00'
        k4 = '00'
        k5 = '01'
        return f"{cls.R_Т}_{a}_{o}_{ggggmmdd}_{k1}_{k2}_{k3}_{k4}_{k5}"


contract = Contract('Договор поставки', '08843672/195031-055', '01.03.2019', '7706664260', '7721247141')
print(Contract.create_file_id('7706664260', '7721247141'))