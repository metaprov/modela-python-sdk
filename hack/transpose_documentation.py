# This module parses the Golang API structures defined in the modelaapi repository to transpose
# useful information from their comments to the Python SDK, for even better in-code Python documentation
# Author:   Liam Sagi <liam@metaprov.com>
# Copyright (C) 2022 modela.ai


import os
import glob
import pprint
import re

from modela.Configuration import convert_case
from astor.source_repr import split_lines
from tree_sitter import Language, Parser
import ast, astor

if not os.path.exists("go_lang.dll"):
    Language.build_library(
        'go_lang.dll',
        ['vendor/tree-sitter-go']
    )

GO_LANGUAGE = Language(os.path.join(os.getcwd(), 'go_lang.dll'), 'go')
go_parser = Parser()
go_parser.set_language(GO_LANGUAGE)
api_lib = {}

def fix_comment(comment: str):
    return comment[2:].lstrip()

def fix_cls_name(cls: bytes):
    cls = cls.decode('utf-8')
    if len(cls.split('.')) > 1:
        cls = cls.split('.')[-1]

    return cls

def generate_comment(doc: list[str]):
    if len(doc) == 1:
        return f' {doc[0]} '.replace('\r', '')
    else:
        docs = '\n    '.join(doc)
        return f'\n    {docs}\n    '.replace('\r', '')


def pretty_source(source):
    return ''.join(split_lines(source, maxline=1000))


def parse_api():
    if not os.path.isdir("modelaapi"):
        raise OSError("modelaapi directory not found. Run git clone https://github.com/metaprov/modelaapi.git")

    for file in glob.glob("modelaapi/pkg/apis/**/**/*_types.go"):
        #if '\\common_types' not in file:
        #    continue

        with open(file, 'rb') as f:
            cursor, comments = go_parser.parse(f.read()).walk(), []
            cursor.goto_first_child()
            while cursor.goto_next_sibling():
                if cursor.node.type == "comment":
                    if b'+' in cursor.node.text:
                        continue

                    comments.append(fix_comment(str(cursor.node.text.decode('utf-8'))))

                if cursor.node.type == "const_declaration":
                    comments = []

                if cursor.node.type == "type_declaration":
                    if len(cursor.node.children[1].children[1].children) == 0:
                        comments = []
                        continue

                    struct = str(cursor.node.children[1].children[0].text.decode('utf-8'))
                    api_lib[struct], comments = {"comments": comments, "fields": {}}, []

                    type_cursor = cursor.node.children[1].children[1].children[1].walk()
                    type_cursor.goto_first_child()
                    while type_cursor.goto_next_sibling():
                        if type_cursor.node.type == "comment":
                            if b'+' in type_cursor.node.text:
                                continue

                            comments.append(fix_comment(str(type_cursor.node.text.decode('utf-8'))))

                        if type_cursor.node.type == "field_declaration":
                            field = re.findall('name=(.*?)($|,|")', type_cursor.node.children[-1].text.decode('utf-8'))
                            if len(field) > 0:
                                api_lib[struct]["fields"][field[0][0]], comments = comments, []
                            else:
                                comments = []


def add_docs():
    for file in glob.glob("../modela/**/models.py"):
        with open(file, 'rb+') as f:
            pyfile = f.read()
            parsed = ast.parse(pyfile)
            for node in ast.walk(parsed):
                if not isinstance(node, ast.ClassDef):
                    continue
                #print(astor.dump_tree(node))

                if not len(node.body):
                    continue

                if not hasattr(node.decorator_list[0].keywords[0].value, 'attr'):
                    continue

                if (cls_name := node.decorator_list[0].keywords[0].value.attr) in api_lib:
                    docs = api_lib[cls_name]
                else:
                    continue

                for field in node.body.copy():
                    if isinstance(field, ast.Expr) and hasattr(field, 'value'):
                        node.body.remove(field)

                if isinstance(node.body[0], ast.Expr) and hasattr(node.body[0], 'value'):
                    if not len(docs["comments"]):
                        node.body = node.body[1:]
                    else:
                        node.body[0].value.s = docs["comments"][0]
                elif len(docs["comments"]):
                    node.body.insert(0, ast.Expr(value=ast.Constant(value=generate_comment(docs["comments"]))))


                fields = node.body.copy()
                for n in range(len(node.body)-1, 0, -1):
                    if not isinstance(fields[n], ast.AnnAssign):
                        continue

                    field = fields[n].target.id
                    if (doc_fld := convert_case(field)) in docs["fields"]:
                        if len(docs["fields"][doc_fld]) == 0:
                            continue

                        print("Out",generate_comment(docs["fields"][doc_fld]))
                        node.body.insert(n+1, ast.Expr(value=ast.Constant(value=generate_comment(docs["fields"][doc_fld]))))


                print(astor.dump_tree(node))

            src = astor.to_source(parsed, pretty_source=pretty_source)
            f.truncate(0)
            f.seek(0, 0)
            f.write(bytes(src, 'utf-8'))


if __name__ == "__main__":
    parse_api()
    add_docs()