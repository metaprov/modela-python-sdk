import inspect
import sys

from .markdown_writer import MarkdownWriter, MarkdownTranslator
from docutils.io import StringOutput
from io import open
from os import path
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import ensuredir, os_path

from modela import *

logger = logging.getLogger(__name__)

class MarkdownBuilder(Builder):
    name = 'markdown'
    format = 'markdown'
    epilog = __('The markdown files are in %(outdir)s.')

    out_suffix = '.md'
    allow_parallel = True
    default_translator_class = MarkdownTranslator

    current_docname = None

    markdown_http_base = 'https://localhost'

    def init(self):
        self.secnumbers = {}

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = path.join(self.outdir, docname + self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                pass

    def get_class_path(self, cls_name) -> str:
        clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        cls = [cls for cls in clsmembers if cls[0] == cls_name]
        if len(cls) > 0:
            mod = cls[0][1].__module__
            return "/docs/PythonSDK/reference/%s#class-%s" % ("/".join(mod.split(".")[1:]), cls[0][1].__qualname__)

        return ""

    def get_target_uri(self, docname: str, typ=None):
        # Returns the target markdown file name
        split = docname.split(".")
        split[0] = "/docs/PythonSDK/reference"
        return "/".join(split)

    def get_refid(self, refid: str):
        split = refid.split(".")
        return ("#class-%s" % split[-1]).lower()


    def prepare_writing(self, docnames):
        self.writer = MarkdownWriter(self)

    def create_index(self, pathname):
        if not path.exists(path.join(pathname, "_index.md")):
            section = pathname.split("/")[-1].title()
            if section == "Infra":
                section = "Infrastructure"

            if section == "Rst":
                return

            frontmatter = """---
title: "%s"
linkTitle: "%s"
description: >
  Reference for the %s module
---\n""" % (section, section, section)
            try:
                with open(path.join(pathname, "_index.md"), 'w', encoding='utf-8') as f:  # type: ignore
                    f.write(frontmatter)
            except (IOError, OSError) as err:
                logger.warning(__('error writing file %s: %s'), path.join(pathname, "_index.md"), err)

    def write_doc(self, docname, doctree):
        self.current_docname = docname
        self.secnumbers = self.env.toc_secnumbers.get(docname, {})
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)

        outname = os_path(docname)
        split = outname.split(".")
        if split[0] == "modela":
            if len(split) > 2:
                outname = "/".join(split[1:])
            elif len(split) > 1:
                outname = split[1]

        if outname in ("index", "modules", "client"):
            return


        outfilename = path.join(
            self.outdir,
            outname + self.out_suffix
        )

        weight = 0
        if outname in ("data", "infra", "inference", "team", "training"):
            outfilename = path.join(self.outdir, outname, "_index.md")
            weight = -1

        ensuredir(path.dirname(outfilename))
        #self.create_index(path.dirname(outfilename))
        fmname = docname.split(".")[-1]
        fmname = fmname[0].capitalize() + fmname[1:]
        if fmname == "Models":
            fmname = "Data Models"

        frontmatter = """---
title: "%s"
linkTitle: "%s"
weight: %d
description: >
  Reference documentation for %s
---\n""" % (fmname, fmname, weight, fmname)
        try:
            with open(outfilename, 'w', encoding='utf-8') as f:  # type: ignore
                f.write(frontmatter + self.writer.output)
        except (IOError, OSError) as err:
            logger.warning(__('error writing file %s: %s'), outfilename, err)

    def finish(self):
        pass
