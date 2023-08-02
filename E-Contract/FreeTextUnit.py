class FreeTextUnit:

    def __init__(self, block_id, alignment, text, style, layout_txt='0', layout_tab=''):
        self.sttext_tag = 'ФрагПроизв'
        self.sttext_atrr = {'НомФраг': block_id,
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
    free_text1 = FreeTextUnit(block_id1, '3', 'Пример текста свободного блока1', styles.get_style(block_id1))
    free_text2 = FreeTextUnit(block_id2, '3', 'Пример текста свободного блока2', styles.get_style(block_id2))
    free_text3 = FreeTextUnit(block_id3, '3', 'Пример текста свободного блока2', styles.get_style(block_id3))

    content = ET.Element('Содержание')
    block1 = ET.SubElement(content, free_text1.sttext_tag, free_text1.sttext_atrr)
    ET.SubElement(block1, free_text1.style.tag, free_text1.style.attributes)
    block2 = ET.SubElement(content, free_text2.sttext_tag, free_text2.sttext_atrr)
    ET.SubElement(block2, free_text2.style.tag, free_text2.style.attributes)
    block3 = ET.SubElement(content, free_text3.sttext_tag, free_text3.sttext_atrr)
    ET.SubElement(block3, free_text3.style.tag, free_text3.style.attributes)
    tree = ET.ElementTree(content)
    with open("test_free_unit.xml", 'wb') as fh:
        tree.write(fh, encoding="windows-1251")

    print(free_text1)