class Style:
    def __init__(self, name="New_style", font_family="Times New Roman", font_weight="normal", font_style="normal",
                 сolor="#000000",
                 font_size="12", line_height="medium", margin_top="medium", margin_bottom="medium", text_indent="35",
                 block_id=None):
        self.tag = 'СтильФрагТекст'
        self.attributes = {'name': name,
                           'font-family': font_family,
                           'font-weight': font_weight,
                           'font-style': font_style,
                           'сolor': сolor,
                           'font-size': font_size,
                           'line-height': line_height,
                           'margin-top': margin_top,
                           'margin-bottom': margin_bottom,
                           'text-indent': text_indent}
        self.block_id = block_id
        self.set_name(self.create_name())

    def get_atrributes_without_name(self):
        font_family = self.attributes.get('font-family')
        font_weight = self.attributes.get('font-weight')
        font_style = self.attributes.get('font-style')
        сolor = self.attributes.get('сolor')
        font_size = self.attributes.get('font-size')
        line_height = self.attributes.get('line-height')
        margin_top = self.attributes.get('margin-top')
        margin_bottom = self.attributes.get('margin-bottom')
        text_indent = self.attributes.get('text-indent')
        return font_family, font_weight, font_style, сolor, font_size, line_height, margin_top, margin_bottom, text_indent

    def get_attributes(self):
        font_family = self.attributes.get('font-family')
        font_weight = self.attributes.get('font-weight')
        font_style = self.attributes.get('font-style')
        font_size = self.attributes.get('font-size')
        return (font_family, font_weight, font_style, font_size)
    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes):
        self.__attributes = attributes

    @attributes.deleter
    def attributes(self):
        del self.__attributes

    def set_name(self, name):
        if self.attributes['name'] == "New_style":
            self.attributes['name'] = name

    def create_name(self):
        return f"{self.attributes['font-family']}_{self.attributes['font-weight']}_{self.attributes['font-style']}_{self.attributes['сolor']}_{self.attributes['font-size']}"

    def rename_style(self, name):
        self.attributes['name'] = name


class Styles:

    def __init__(self):
        self.styles_dict = {}

    def add_style(self, style):
        existing_style = self.find_style_name(style)
        if existing_style:
            del style.attributes
            style.attributes = {'name': existing_style}
        self.styles_dict[style.block_id] = style

    def find_style_name(self, new_style):
        for style in self.styles_dict.values():
            if style.get_atrributes_without_name() == new_style.get_atrributes_without_name():
                return style.attributes['name']

    def get_style(self, block_id):
        return self.styles_dict.get(block_id)

if __name__ == "__main__":
    styles = Styles()
    styles.add_style(Style(block_id='00001'))
    styles.add_style(Style(block_id='00002'))
    styles.add_style(Style(block_id='00003'))
    gstyle = styles.get_style('00002')
    print(gstyle)