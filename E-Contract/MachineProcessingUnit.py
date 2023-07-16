class MachineProcesingUnit:

    def __init__(self, block_id, element_type, element_name, alignment, text, style, layout_txt='0',
                 layout_tab=''):
        self.sttext_tag = 'ФрагТиповой'
        self.sttext_attributes = {'НомФраг': block_id,
                            'ЦифКЭлПер': element_type,
                            'БукКЭлПер': element_name,
                            'МакетВыравн': alignment,
                            'СодержФраг': text}
        self.layout_txt = ('МакетФрагТекст', layout_txt)
        self.layout_tab = ('МакетФрагТаб', layout_tab)
        self.style = style