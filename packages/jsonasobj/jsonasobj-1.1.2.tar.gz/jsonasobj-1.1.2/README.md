# jsonasobj

## Introduction

This is an extension to the python *json* library that represents the JSON
as a first class python object rather than a straight 
dictionary.  Contents can still be accessed using dictionary format.

### Changes in version 1.1.0:
1) Method signatures all have full typing

2) `load` function will take a file name, a url -or- an open file as an argument


---
**Warning**: Version 1.0.0 of this package is NOT backwards compatible with earlier versions.  The JSONObj functions:
* setattr(...)
* get(...)

have been replaced with
* _setattr(...)
* _get(...)

This was done because anything without a "_" prefix presents a potential collision with the JSON itself.

---
## Requirements

* Python (3.0 or later)

## Installation

*jsonasobj* can be installed with *pip*:

```bash
pip install jsonasobj
```

## Short Example
--------------

```python

import jsonasobj

test_json = """{
  "@context": {
    "name": "http://xmlns.com/foaf/0.1/name",
    "knows": "http://xmlns.com/foaf/0.1/knows",
    "menu": {
      "@id": "name:foo",
      "@type": "@id"
    }
  },
  "@id": "http://me.markus-lanthaler.com/",
  "name": "Markus Lanthaler",
  "knows": [
    {
      "name": "Dave Longley",
      "menu": "something",
      "modelDate" : "01/01/2015"
    }
  ]
}"""

py_obj = jsonasobj.loads(test_json)
py_obj.knows[0].extra = {'age': 17}
py_obj.knows.append(dict(name='Barack Obama'))
del py_obj.knows[0]['menu']
print(py_obj.name)
print(py_obj['name'])
print(py_obj.knows[0].name)
print(py_obj['@context'].name)
print(py_obj._as_json_dumps())
print(py_obj._as_dict)
```

Result:

```bash
Markus Lanthaler
Markus Lanthaler
Dave Longley
http://xmlns.com/foaf/0.1/name
{
   "@id": "http://me.markus-lanthaler.com/",
   "knows": [
      {
         "extra": {
            "age": 17
         },
         "name": "Dave Longley",
         "modelDate": "01/01/2015"
      },
      {
         "name": "Barack Obama"
      }
   ],
   "name": "Markus Lanthaler",
   "@context": {
      "menu": {
         "@id": "name:foo",
         "@type": "@id"
      },
      "knows": "http://xmlns.com/foaf/0.1/knows",
      "name": "http://xmlns.com/foaf/0.1/name"
   }
}
{'@id': 'http://me.markus-lanthaler.com/', 'knows': [{'modelDate': '01/01/2015', 'extra': {'age': 17}, 'name': 'Dave Longley'}, {'name': 'Barack Obama'}], 'name': 'Markus Lanthaler', '@context': {'menu': {'@id': 'name:foo', '@type': '@id'}, 'knows': 'http://xmlns.com/foaf/0.1/knows', 'name': 'http://xmlns.com/foaf/0.1/name'}}
```

## Source

http://github.com/hsolbrig/jsonasobj
