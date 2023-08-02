class MachineProcesingUnit:

    def __init__(self, block_id, element_type, element_name, alignment, text, style, layout_txt='0',
                 layout_tab=''):
        self.sttext_tag = 'ФрагТиповой'
        self.sttext_atrr = {'НомФраг': block_id,
                            'ЦифКЭлПер': element_type,
                            'БукКЭлПер': element_name,
                            'МакетВыравн': alignment,
                            'СодержФраг': text}
        self.layout_txt = ('МакетФрагТекст', layout_txt)
        self.layout_tab = ('МакетФрагТаб', layout_tab)
        self.style = style

    def add_text(self, text):
        self.sttext_atrr['СодержФраг'] += text
        
if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    from UnitStyle import Style, Styles

    block_id1 = '00001'
    block_id2 = '00002'
    block_id3 = '00003'
    styles = Styles()
    styles.add_style(Style(block_id=block_id1))
    styles.add_style(Style(block_id=block_id2))
    styles.add_style(Style(block_id=block_id3))
    machine_text1 = MachineProcesingUnit(block_id1, '1108', 'ОГРН', '3', 'Пример текста свободного блока1', styles.get_style(block_id1))
    machine_text2 = MachineProcesingUnit(block_id2, '1108', 'ОГРН', '3', 'Пример текста свободного блока2', styles.get_style(block_id2))
    machine_text3 = MachineProcesingUnit(block_id3, '1108', 'ОГРН', '3', 'Пример текста свободного блока3', styles.get_style(block_id3))

    content = ET.Element('Содержание')
    block1 = ET.SubElement(content, machine_text1.sttext_tag, machine_text1.sttext_atrr)
    ET.SubElement(block1, machine_text1.style.tag, machine_text1.style.attributes)
    block2 = ET.SubElement(content, machine_text2.sttext_tag, machine_text2.sttext_atrr)
    ET.SubElement(block2, machine_text2.style.tag, machine_text2.style.attributes)
    block3 = ET.SubElement(content, machine_text3.sttext_tag, machine_text3.sttext_atrr)
    ET.SubElement(block3, machine_text3.style.tag, machine_text3.style.attributes)
    tree = ET.ElementTree(content)
    with open("test_machine_unit.xml", 'wb') as fh:
        tree.write(fh, encoding="windows-1251")

    print(machine_text1)