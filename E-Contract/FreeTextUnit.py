class FreeTextUnit:

    def __init__(self, block_id, alignment, text, style, layout_txt='0', layout_tab=''):
        self.sttext_tag = 'ФрагПроизв'
        self.sttext_atrr = {'НомФраг': block_id,
                            'МакетВыравн': alignment,
                            'СодержФраг': text}
        self.layout_txt = ('МакетФрагТекст', layout_txt)
        self.layout_tab = ('МакетФрагТаб', layout_tab)
        self.style = style