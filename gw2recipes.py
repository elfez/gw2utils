#!/usr/bin/python

import gw2spidy
from html import HTML
import cgitb
cgitb.enable()

'''
recipe:
    'result_item_min_sale_unit_price
    rating
    crafting_cost
    name
    data_id
    result_item_max_offer_unit_price
    result_item_data_id
    discipline_id
    result_count
'''

disc = ['Huntsman', 'Artificer', 'Weaponsmith', 'Armorsmith', 'Leatherworker',
        'Tailor', 'Jeweler', 'Cook']

class recipe:

    def __init__ (self, name, buyPrice, sellPrice, cost, itemId, disc):
        self.name = name
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice,
        self.cost = cost
        self.itemId = itemId
        self.disc = disc
        self.profit = buyPrice - cost

    def isProfitable(self):
        if self.profit > 50:
            return True

    def printData(self):
        print "%-30s: %5d %5d %.2f" % (self.name, self.cost, self.buyPrice,
                (self.profit * 0.85) / 100.0)

    def genTR(self):
        tr = HTML('tr')

        url = "http://www.gw2spidy.com/recipe/%d" % self.itemId
        tr.td.a(self.name, href=url, target="_blank")
        marginPct = self.profit / float(self.buyPrice)
        for i in (self.cost/100.0, self.buyPrice/100.0, 
                self.profit/ 100.0, "%.2f" % (marginPct * 100)):
            tr.td(str(i), align="right")
        tr.td(disc[self.disc])
        return (tr)

    def toS(self, val):
        return val / 100.0

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

  $("#recipes").tablesorter({widgets:['zebra'], sortList: [[3,1],],});

});
"""


    body.script(' ', src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js")
    script = body.script(scr, escape=False, type="text/javascript")
    body.link(' ', escape=False, rel="stylesheet", text="text/css", 
            href="http://www.magweb.net/static/js/tablesorter/themes/blue/style.css")
    body.script(" ", escape=False, type="text/javascript", 
            src="http://www.magweb.net/static/js/tablesorter/jquery.tablesorter.js")
    body.script(scr2, escape=False, type="text/javascript")
    


gw2 = gw2spidy.Gw2Spidy()

print "Content-type: text/html\n"

page = HTML('html')
body = page.body()
populateScripts(body)

form = body.form("Filter:", style="margin-left: 10px;")
form.input(' ', type="text", name="filtrpt", onkeyup="filter2(this,'recipes')")
tab = body.table(id="recipes", klass="tablesorter", border="1")
thead = tab.thead()
thead.th("Name")
thead.th("Cost")
thead.th("Buy")
thead.th("Profit")
thead.th("Margin %")
thead.th("Profession")

for d in range(len(disc)):
    #print "====== %s" % disc[d]
    recipes = []
    res = gw2.getRecipesOfDiscipline(d+1, allPages = True)
    for i in res:
        newItem = recipe(i['name'], i['result_item_max_offer_unit_price'],
                i['result_item_min_sale_unit_price'], i['crafting_cost'],
                i['data_id'], d)
        recipes.append(newItem)

    for i in recipes:
        if i.isProfitable():
            tab.text(str(i.genTR()), escape=False)

print page
