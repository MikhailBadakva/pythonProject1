import xml.etree.ElementTree as ET
import datetime
import docx
import re
from TypElemList import type_elements



class StyleText:

    def __init__(self, name, font_family="Times New Roman", font_weight="normal", font_style="normal", сolor="#000000",
                 font_size="12", line_height="medium", margin_top="medium", margin_bottom="medium", text_indent="48"):
        self.style_tag = 'СтильФрагТекст'
        self.style_atrr = {'name': name,
                           'font-family': font_family,
                           'font-weight': font_weight,
                           'font-style': font_style,
                           'сolor': сolor,
                           'font-size': font_size,
                           'line-height': line_height,
                           'margin-top': margin_top,
                           'margin-bottom': margin_bottom,
                           'text-indent': text_indent}

    def get_atrr(self):
        return (self.style_atrr['font-family'], self.style_atrr['font-weight'], self.style_atrr['font-style'],
                self.style_atrr['font-size'])


class StandardText:

    def __init__(self, block_id, element_type, element_name, alignment, text, style_text, layout_txt='0',
                 layout_tab=''):
        self.sttext_tag = 'ФрагТиповой'
        self.sttext_atrr = {'НомФраг': block_id,
                            'ЦифКЭлПер': element_type,
                            'БукКЭлПер': element_name,
                            'МакетВыравн': alignment,
                            'СодержФраг': text}
        self.layout_txt = ('МакетФрагТекст', layout_txt)
        self.layout_tab = ('МакетФрагТаб', layout_tab)
        self.style_text = style_text


class FreeText:

    def __init__(self, block_id, alignment, text, style_text, layout_txt='0', layout_tab=''):
        self.sttext_tag = 'ФрагПроизв'
        self.sttext_atrr = {'НомФраг': block_id,
                            'МакетВыравн': alignment,
                            'СодержФраг': text}
        self.layout_txt = ('МакетФрагТекст', layout_txt)
        self.layout_tab = ('МакетФрагТаб', layout_tab)
        self.style_text = style_text

    def add_text(self, text):
        self.sttext_atrr['СодержФраг'] += text


class EContract:

    def __init__(self, file_id, context_contr_name, context_contr_id, context_contr_date, INN1, INN2,
                 file_formvers='1.01', file_progvers='0.1', file_listvers='00.01'):
        self.file_tag = 'Файл'
        self.file_attr = {'ИдФайл': file_id,
                          'ВерсФорм': file_formvers,
                          'ВерсПрог': file_progvers,
                          'ВерсПеречня': file_listvers}
        now = datetime.datetime.now()
        self.context_tag = 'Содержание'
        self.context_atrr = {'КНД': '1175016',
                             'НаимДок': context_contr_name,
                             'НомДок': context_contr_id,
                             'ДатаДок': context_contr_date,
                             'ДатаИнфСодСд': now.strftime("%d.%m.%Y"),
                             'ВремИнфСодСд': now.strftime("%H.%M.%S"),
                             'ПризнИн': '0',
                             'ПорФормДок': '2'}
        self.INN1 = ('ИННЮДСт1', INN1)
        self.INN2 = ('ИННЮДСт1', INN2)
        self.blocks = []

    def set_block_text(self, block_text):
        self.blocks.append(block_text)

    def createXML(self, filename):
        root = ET.Element(self.file_tag, self.file_attr)
        context = ET.Element(self.context_tag, self.context_atrr)
        root.append(context)
        INN1 = ET.SubElement(context, self.INN1[0])
        INN1.text = self.INN1[1]
        INN2 = ET.SubElement(context, self.INN2[0])
        INN2.text = self.INN2[1]
        for block in self.blocks:
            block_ = ET.SubElement(context, block.sttext_tag, block.sttext_atrr)
            block_layout = ET.SubElement(block_, block.layout_txt[0]) if block.layout_txt[1] else ET.SubElement(block_,
                                                                                                                block.layout_tab[
                                                                                                                    0])
            block_layout.text = block.layout_txt[1] if block.layout_txt[1] else block.layout_tab[1]
            block_style = ET.SubElement(block_, block.style_text.style_tag, block.style_text.style_atrr)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fh:
            tree.write(fh, encoding="windows-1251")


if __name__ == "__main__":
    econtarct = EContract(
        'ON_SODSD_2BM-5029112443-643902001-201809170824291744204_2BM-1624014670-162401001-201704130206443850414_20230512_99fe79d2-5b5d-4674-98b1-e0cb98a128ac-1-00-00-01',
        'Договор поставки', '08843672/195031-055', '01.03.2019', '7706664260', '7721247141')
    # econtarct.set_block_text(StandardText('000001', '1103', 'НаимОрг', '3', 'Акционерное общество «Атомный энергопромышленный комплекс', StyleText('Основной')))
    # econtarct.set_block_text(FreeText('000002',  '3', 'Свободный текст', StyleText('Основной')))

    doc = docx.Document('АСЭ_пример дог-ра Куку.docx')
    i = 1
    for paragraph in doc.paragraphs:
        flg_new_block = True
        flg_start_standard_block = False
        standard_block = ''
        if paragraph.text:
            for run in paragraph.runs:
                font_family = run.font.name if run.font.name else "Times New Roman"
                font_weight = "bold" if run.font.bold else "normal"
                font_style = "italic" if run.font.italic else "normal"
                font_size = f'{run.font.size}' if run.font.size else "177800"
                # line_height = "medium"
                # margin_top = "medium"
                # margin_bottom = "medium"
                # text_indent = "48"
                if '{' in run.text:
                    flg_start_standard_block = True
                if flg_start_standard_block:
                    standard_block += run.text
                    if '}' in run.text:
                        element_type = re.search(r'(?<=#).*?(?=#)', standard_block)[0]
                        element_name = type_elements[element_type]
                        text_ = re.search(r'(?<=#\w{4}#).*?(?=})', standard_block)[0]
                        econtarct.set_block_text(StandardText(f'{i:06d}', element_type, element_name, '3', text_,
                                                              StyleText('Основной', font_family=font_family,
                                                                        font_weight=font_weight, font_style=font_style,
                                                                        font_size=font_size)))
                        standard_block = ''
                        flg_start_standard_block = False
                        flg_new_block = True
                        i += 1
                elif flg_new_block:
                    econtarct.set_block_text(FreeText(f'{i:06d}', '3', run.text,
                                                      StyleText('Основной', font_family=font_family,
                                                                font_weight=font_weight, font_style=font_style,
                                                                font_size=font_size)))
                    i += 1
                    flg_new_block = False
                elif (font_family, font_weight, font_style, font_size) != econtarct.blocks[-1].style_text.get_atrr():
                    econtarct.set_block_text(FreeText(f'{i:06d}', '3', run.text,
                                                      StyleText('Основной', font_family=font_family,
                                                                font_weight=font_weight, font_style=font_style,
                                                                font_size=font_size)))
                    i += 1
                else:
                    econtarct.blocks[-1].add_text(run.text)

econtarct.createXML("test.xml")
