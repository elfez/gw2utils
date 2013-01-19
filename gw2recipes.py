#!/usr/bin/python

import gw2spidy
from html import HTML
import cPickle
from os import path
import time
import cgitb
cgitb.enable()

CACHEDIR = "/tmp"
MODTIME = 30 * 60       # Time in seconds to cache data

disc = ['Huntsman', 'Artificer', 'Weaponsmith', 'Armorsmith', 'Leatherworker',
        'Tailor', 'Jeweler', 'Cook']

class recipe:

    def __init__ (self, name, buyPrice, sellPrice, matCost, itemId, disc, 
            skill):
        self.name = name
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice
        self.matCost = matCost
        self.itemId = itemId
        self.disc = disc
        self.flipProfit = (self.sellPrice * 0.85) - self.buyPrice
        self.instantProfit = (self.buyPrice * 0.85) - self.matCost
        self.craftProfit = (self.sellPrice * 0.85) - self.matCost
        self.skill = skill

    def isProfitable(self):
        if (self.flipProfit or self.instantProfit or self.craftProfit)> 50:
            return True

    def genTR(self):
        tr = HTML('tr')

        url = "http://www.gw2spidy.com/recipe/%d" % self.itemId
        # Name
        tr.td.a(self.name, href=url, target="_blank")
        for i in (self.toS(self.matCost),
                self.toS(self.buyPrice), 
                self.toS(self.sellPrice),
                self.toS(self.instantProfit),
                self.toS(self.flipProfit),
                self.toS(self.craftProfit)):
                

            tr.td(i, align="right")
            # Profession
        tr.td(disc[self.disc])
        tr.td(str(self.skill))
        return (tr)

    def toS(self, val):
        return "%.2f" % (val / 100.0)

def populateScripts(ent):

    scr = """
function filter2 (phrase, _id){
	var words = phrase.value.toLowerCase().split(" ");
	var table = document.getElementById(_id);
	var ele;
	for (var r = 1; r < table.rows.length; r++){
		ele = table.rows[r].innerHTML.replace(/<[^>]+>/g,"");
	        var displayStyle = 'none';
	        for (var i = 0; i < words.length; i++) {
		    if (ele.toLowerCase().indexOf(words[i])>=0)
			displayStyle = '';
		    else {
			displayStyle = 'none';
			break;
		    }
	        }
		table.rows[r].style.display = displayStyle;
	}
}
"""
    scr2 = """
$(document).ready(function()
{

  $("#recipes").tablesorter({widgets:['zebra'], sortList: [[4,1],],});

});
"""


    body.script(' ', src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js")
    script = body.script(scr, escape=False, type="text/javascript")
    body.link(' ', escape=False, rel="stylesheet", text="text/css", 
            href="http://www.magweb.net/static/js/tablesorter/themes/blue/style.css")
    body.script(" ", escape=False, type="text/javascript", 
            src="http://www.magweb.net/static/js/tablesorter/jquery.tablesorter.js")
    body.script(scr2, escape=False, type="text/javascript")

def getRecipes(d):

    recipes= []
    cSkill = disc[d]
    datafile = "%s/%s_data.pkl" % (CACHEDIR, cSkill)

    fetchData = False
    if path.exists(datafile):
        if time.time() - path.getmtime(datafile) > MODTIME:
            fetchData = True
    else:
        fetchData = True

    if fetchData:
        res = gw2.getRecipesOfDiscipline(d+1, allPages = True)
        for i in res:
            newItem = recipe(i['name'], i['result_item_max_offer_unit_price'],
                    i['result_item_min_sale_unit_price'], i['crafting_cost'],
                    i['data_id'], d, i['rating'])
            recipes.append(newItem)

        output = open(datafile, 'wb')
        cPickle.dump(recipes, output)
    else:
        infile = open(datafile, 'rb')
        recipes = cPickle.load(infile)
        infile.close()

    return recipes


gw2 = gw2spidy.Gw2Spidy()

print "Content-type: text/html\n"

page = HTML('html')
body = page.body()
populateScripts(body)
body.ul.li("All prices in silver")
body.ul.li("Instant profit = craft, sell to highest buyer")
body.ul.li("Flip profit = buy at highest buyer, sell at lowest seller")
body.ul.li("Craft profit = Craft, sell at lowest seller")

form = body.form("Filter:", style="margin-left: 10px;")
form.input(' ', type="text", name="filtrpt", onkeyup="filter2(this,'recipes')")
tab = body.table(id="recipes", klass="tablesorter", border="1")
thead = tab.thead()
thead.th("Name")
thead.th("Mat Cost")
thead.th("Highest Buy")
thead.th("Lowest Sell")
thead.th("Instant Profit")
thead.th("Flip Profit")
thead.th("Craft Profit")
thead.th("Profession")
thead.th("Skill")

for d in range(len(disc)):
    recipes = []
    recipes.extend(getRecipes(d))

    for i in recipes:
        if i.isProfitable():
            tab.text(str(i.genTR()), escape=False)

print page
