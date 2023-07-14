import re

text = "{#xxxx#1/1111-1}"
print(re.search(r'(?<=#).*?(?=#)', text)[0])
print(re.search(r'(?<=#\w{4}#).*?(?=})', text)[0])