#!/usr/bin/python

from html import HTML
import gw2spidy

# bones
# claw
# fang
# scale
# totem
# venom sac

tierMats =[ [24342,24346,24352,24284,24296,24278,24290], # tier1
        [24343,24347,24353,24285,24297,24279,24291],
        [24344,24348,24354,24286,24298,24280,24292],
        [24345,24349,24355,24287,24363,24281,24293],
        [24341,24350,24356,24288,24299,24282,24294],
        [24358,24351,24357,24289,24300,24283,24295] ]   # tier 6

class mat:

    def __init__ (self, name, saleAvail, buyAvail, itemId, sellPrice, buyPrice,
            salePriceChangeLastHr, buyPriceChangeLastHr, tier):
        
        self.name = name
        self.saleAvail = saleAvail
        self.buyAvail = buyAvail
        self.itemId = itemId
        self.sellPrice = sellPrice
        self.buyPrice = buyPrice
        self.salePriceChangeLastHr = salePriceChangeLastHr
        self.buyPriceChangeLastHr = buyPriceChangeLastHr
        self.profit = (sellPrice - buyPrice) * 0.85
        self.margin = self.profit / float(sellPrice) * 100
        self.tier = tier

gw = gw2spidy.Gw2Spidy()

# Populate item dict
tier = 0
items = {}
for t in tierMats:
    tier += 1

    for ID in t:
        i = gw.getItemData(ID)
        newItem = mat(i['name'], i['sale_availability'], 
                i['offer_availability'], ID, i['min_sale_unit_price'],
                i['max_offer_unit_price'], i['sale_price_change_last_hour'],
                i['offer_price_change_last_hour'], tier)
        items[ID] = newItem
# Generate HTML
page = HTML('html')
tier = 0
for t in tierMats:
    tier += 1

    page.br()
    page.br()
    table = page.table(border='1')
    table.thead.th("Tier %d" % tier, colspan='3')
    head = table.thead()
    for s in ['Name','Min sell', 'Max buy']:
        head.th(s)

    for ID in t:
        tr = table.tr()
        for data in [items[ID].name, items[ID].sellPrice, items[ID].buyPrice]:
            tr.td(str(data))

print "Content-type: text/html\n"
print page


