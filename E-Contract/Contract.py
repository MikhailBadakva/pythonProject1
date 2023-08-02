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
        self.styles = Styles()

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

    def add_unit(self, obj):
        self.units.append(obj)

    def get_style_doc_run(self, run):
        font_family = run.font.name if run.font.name else "Times New Roman"
        font_weight = "bold" if run.font.bold else "normal"
        font_style = "italic" if run.font.italic else "normal"
        font_size = f'{run.font.size}' if run.font.size else "177800"
        # line_height = "medium"
        # margin_top = "medium"
        # margin_bottom = "medium"
        # text_indent = "48
        return (font_family, font_weight, font_style, font_size)

    def get_element_type(self, standard_block):
        element_type = re.search(r'(?<=#).*?(?=#)', standard_block)[0]
        element_name = type_elements[element_type]
        text_ = re.search(r'(?<=#\w{4}#).*?(?=})', standard_block)[0]
        return (element_type, element_name, text_)
    def create_from_docx(self, doc_docx):
        doc = docx.Document(doc_docx)
        i = 1
        for paragraph in doc.paragraphs:
            flg_new_block = True
            flg_start_standard_block = False
            standard_block = ''
            prev_font_family = prev_font_weight = prev_font_style = prev_font_size = None
            if paragraph.text:
                for run in paragraph.runs:
                    font_family, font_weight, font_style, font_size = self.get_style_doc_run(run)
                    if '{' in run.text:
                        flg_start_standard_block = True
                    if flg_start_standard_block:
                        standard_block += run.text
                        if '}' in run.text:
                            self.styles.add_style(
                                Style(block_id=f'{i:06d}', font_family=font_family, font_weight=font_weight,
                                      font_style=font_style, font_size=font_size))
                            element_type, element_name, text_ = self.get_element_type(standard_block)
                            self.add_unit(MachineProcesingUnit(f'{i:06d}', element_type, element_name, '3', text_,
                                                                  self.styles.get_style(f'{i:06d}')))
                            standard_block = ''
                            flg_start_standard_block = False
                            flg_new_block = True
                            i += 1
                    elif flg_new_block:
                        self.styles.add_style(
                            Style(block_id=f'{i:06d}', font_family=font_family, font_weight=font_weight,
                                  font_style=font_style, font_size=font_size))
                        self.add_unit(FreeTextUnit(f'{i:06d}', '3', run.text,
                                                   self.styles.get_style(f'{i:06d}')))
                        i += 1
                        flg_new_block = False
                    elif (font_family, font_weight, font_style, font_size) != (prev_font_family, prev_font_weight, prev_font_style, prev_font_size):
                        self.styles.add_style(
                            Style(block_id=f'{i:06d}', font_family=font_family, font_weight=font_weight,
                                  font_style=font_style, font_size=font_size))
                        self.add_unit(FreeTextUnit(f'{i:06d}', '3', run.text,
                                                          self.styles.get_style(f'{i:06d}')))
                        i += 1
                    else:
                        self.units[-1].add_text(run.text)
                    prev_font_family, prev_font_weight, prev_font_style, prev_font_size = font_family, font_weight, font_style, font_size
    def createXML(self, filename):
        root = ET.Element(self.file_tag, self.file_attributes)
        context = ET.Element(self.context_tag, self.context_attributes)
        root.append(context)
        INN1 = ET.SubElement(context, self.INN1[0])
        INN1.text = self.INN1[1]
        INN2 = ET.SubElement(context, self.INN2[0])
        INN2.text = self.INN2[1]
        for block in self.units:
            block_ = ET.SubElement(context, block.sttext_tag, block.sttext_atrr)
            block_layout = ET.SubElement(block_, block.layout_txt[0]) if block.layout_txt[1] else ET.SubElement(block_,
                                                                                                                block.layout_tab[
                                                                                                                    0])
            block_layout.text = block.layout_txt[1] if block.layout_txt[1] else block.layout_tab[1]
            block_style = ET.SubElement(block_, block.style.tag, block.style.attributes)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fh:
            tree.write(fh, encoding="windows-1251")

contract = Contract('Договор поставки', '08843672/195031-055', '01.03.2019', '7706664260', '7721247141')
contract.create_from_docx('АСЭ_пример дог-ра Куку.docx')
contract.createXML("test_1.xml")
print(Contract.create_file_id('7706664260', '7721247141'))