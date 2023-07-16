class Style:
    def __init__(self, name="New_style", font_family="Times New Roman", font_weight="normal", font_style="normal",
                 сolor="#000000",
                 font_size="12", line_height="medium", margin_top="medium", margin_bottom="medium", text_indent="35"):
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
        self.first_unit_id = None

    def get_atrributes_without_name(self):
        return (self.attributes['font-family'],
                self.attributes['font-weight'],
                self.attributes['font-style'],
                self.attributes['сolor'],
                self.attributes['font-size'],
                self.attributes['line-height'],
                self.attributes['margin-top'],
                self.attributes['margin-bottom'],
                self.attributes['text-indent'])

    def get_attributes(self):
        return self.attributes

    def set_name(self, name):
        if self.name == "New_style":
            self.attributes['name'] = name

    def create_name(self):
        return f'{font_family}_{font_weight}_{font_style}_{сolor}_{font_size}'

    def rename_style(self, name):
        self.attributes['name'] = name

class Styles:

    def __init__(self):
        self.styles_list = []

    def add_style(self, style):
        self.styles_list.append(style)

    def find_style_name(self, new_style):
        for style in self.styles_list:
            if style.get_atrributes_without_name() == new_style.get_atrributes_without_name():
                return style.attributes[]