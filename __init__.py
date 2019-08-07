__doc__="""A tool for processing a LaTeX ins and dtx into sty files
"""
#
# Copyright (c) 2019, Keith F. Prussing
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import re

from SCons.Action        import Action
from SCons.Builder       import Builder
from SCons.Tool.pdflatex import PDFLaTeXAuxAction
from SCons.Tool.tex      import tex_pdf_emitter


def _dtx_emitter(target, source, env):
    """An emitter to add additional outputs generated by dtx files
    """
    root, _ = os.path.splitext(str(source[0]))
    target, source = tex_pdf_emitter(target, source, env)
    target.extend([root + x for x in (".ilg", ".ind")])
    return target, source


def _ins_emitter(target, source, env):
    """Scan the .ins file for the generated files
    """
    basedir = None
    outdir = None
    pattern = r"\\(" + "|".join([
            r"file{\s*(.*?)\s*}\s*{\s*\\from{(.*?)}\s*{.*?}\s*}",
            r"usedir{\s*(.*?)\s*}",
            r"BaseDirectory{\s*(.*?)\s*}"
        ]) + ")"
    with open(str(source[0]), "r") as src:
        ins = re.sub(r"[^\\]%.*", "", src.read())

    flags = re.MULTILINE | re.DOTALL
    for pat, tgt, src, usedir, base in re.findall(pattern, ins, flags):
        if re.match("file", pat):
            target.append(os.path.join(outdir, tgt) if outdir else tgt)
            source.extend([x.strip() for x in src.split(",")])
        elif re.match("usedir", pat) and usedir:
            outdir = os.path.join(basedir, usedir) if basedir \
                                                   else outdir
        elif re.match("BaseDirectory", pat) and base:
            basedir = base
        else:
            # This should never actually happen.
            raise NotImplementedError

    # print("source: {0}".format([str(x) for x in source]))
    # print("target: {0}".format([str(x) for x in target]))
    return target, source


_ins2sty = Builder(action=Action("$INS2STYCOM", "$INS2STYCOMSTR"),
                   emitter=_ins_emitter)
_dtxidx = Builder(action=Action("$DTXIDXCOM", "$DTXIDXCOMSTR"),
                  source_suffix=".idx", suffix=".ind")
_dtxglo = Builder(action=Action("$DTXGLOCOM", "$DTXGLOCOMSTR"),
                  source_suffix=".glo", suffix=".gls")


def generate(env):
    """Add the Builders and construction variables to the Environment
    """

    # Add the dtx as an extension for the PDF builder
    env["BUILDERS"]["PDF"].add_action(".dtx", PDFLaTeXAuxAction)
    env["BUILDERS"]["PDF"].add_emitter(".dtx", _dtx_emitter)

    # Add the ins as an extension for the PDF builder
    env["INS2STY"] = env["PDFLATEX"]
    env.SetDefault(
            INS2STYCOM = "$INS2STY ${SOURCE}",
            INS2STYCOMSTR = "",
            # DTXIDXCOM = "$MAKEINDEX -s gind.ist -o ${TARGET} ${SOURCE}",
            # DTXIDXCOMSTR = "",
            # DTXGLOCOM = "$MAKEINDEX -s gglo.ist -o ${TARGET} ${SOURCE}",
            # DTXGLOCOMSTR = "",
        )
    env["BUILDERS"]["ins2sty"] = _ins2sty
    # env["BUILDERS"]["dtxidx"] = _dtxidx
    # env["BUILDERS"]["dtxglo"] = _dtxglo
    return


def exists(env):
    return True

