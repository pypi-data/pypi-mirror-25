
# Terrapin 

Terrapin is a lightweight template language. It uses the [ply]](https://github.com/dabeaz/ply) libary to tokenise and parse. 

## To install

`pip install terrapin`

## Usage

```
from terrapin.parser import Parser

template = 'Hello {{name}}'
context = {
	"name" : "bob"
}

terrapin = Parser()
output = terrapin.parse(template, context)
print(output)
```

## Syntax

Terrapin supports the following

- Variables from the context: `{{variable}}`
- Truthy if `{% if variable %}I'm alive{% endif %}`
- Equality if `{% if variable == "String" %}I'm alive{% endif %}`
- Non Equality if `{% if variable != "String" %}I'm alive{% endif %}`
- Else `{% if variable %}foo{% else %}bar{% endif %}`