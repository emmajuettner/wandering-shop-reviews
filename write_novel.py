import json
import math
import random
import os
from pathlib import Path
from jinja2 import FileSystemLoader, Environment
import tracery
from tracery.modifiers import base_english

# This code is a mess, sorry!

# Utility functions

def generateFromGrammar(grammarFile, origin):
	grammarStr = Path("grammars/"+grammarFile+".json").read_text()
	grammarJson = json.loads(grammarStr)
	grammar = tracery.Grammar(grammarJson)
	grammar.add_modifiers(base_english)
	return grammar.flatten("#" + origin + "#")

def addToNovel(newParagraph):
	global novel
	novel += "<p>" + newParagraph + "</p>"
	
novel = ""
addToNovel("testing basic setup")
addToNovel("I bought " + generateFromGrammar("magical-objects", "item") + " from this shop. five stars")

# Build an html file populated with the novel we've generated
loader = FileSystemLoader(".")
env = Environment(
    loader=loader, extensions=["jinja2_humanize_extension.HumanizeExtension"]
)
template = env.get_template("index.jinja")
Path("index.html").write_text(
    template.render(
        {
            "novel" : novel
        }
    )
)
print("Generated index.html")
