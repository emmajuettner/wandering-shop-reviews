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

def aggregateFlavorTextGrammars():
	flavorGrammars = ["pottery-and-porcelain","a-tangled-tale"]
	skipFields = ["source-url","source-title","source-author","source-date"]
	combinedFlavorGrammar = {}
	for grammarFileName in flavorGrammars:
		grammarStr = Path("grammars/"+grammarFileName+".json").read_text()
		grammarJson = json.loads(grammarStr)
		for key in grammarJson.keys():
			if (key not in skipFields):
				combinedFlavorGrammar.setdefault(key, [])
				combinedFlavorGrammar[key]+=grammarJson[key]
	return combinedFlavorGrammar

allFlavorGrammars = aggregateFlavorTextGrammars()

def generateFromGrammar(grammarFile, origin):
	grammarStr = Path("grammars/"+grammarFile+".json").read_text()
	grammarJson = json.loads(grammarStr)
	grammar = tracery.Grammar(grammarJson)
	grammar.add_modifiers(base_english)
	return grammar.flatten("#" + origin + "#")
	
def populateFlavorText(textToPopulate):
	grammar = tracery.Grammar(allFlavorGrammars)
	grammar.add_modifiers(base_english)
	cleanedTextToPopulate = textToPopulate.replace("((","#").replace("))","#")
	return grammar.flatten(cleanedTextToPopulate)

def chooseRandom(arr) :
	return random.choice(arr)

def addToNovel(newParagraph):
	global novel
	novel += "<p>" + newParagraph + "</p>"
	
novel = ""

for i in range(10):
	review_sentiment = chooseRandom(["positive", "mixed", "negative"])
	if review_sentiment == "positive":
		addToNovel(chooseRandom(["★★★★★","★★★★☆"]))
		addToNovel(populateFlavorText(generateFromGrammar("review-formats","positive-format")))
	elif review_sentiment == "negative":
		addToNovel(chooseRandom(["★☆☆☆☆","★★☆☆☆"]))
		addToNovel(populateFlavorText(generateFromGrammar("review-formats","negative-format")))
	else:
		addToNovel(chooseRandom(["★★☆☆☆","★★★☆☆","★★★★☆"]))
		addToNovel(populateFlavorText(generateFromGrammar("review-formats","mixed-format")))
	addToNovel("<hr>")

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
