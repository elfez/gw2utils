// ==UserScript==
// @name        gw2spidy pct
// @namespace   http://www.crashprone.net
// @include     http://www.gw2spidy.com/*
// @grant       none 
// @version     1
// ==/UserScript==

var tableNo = 0;
if (document.URL.indexOf("/recipe/") > -1 ) {
    tableNo = 1;
}
var table = document.getElementsByTagName("table")[tableNo];
var rows = table.getElementsByTagName("tr");
var pageType = "normal";

function log(str) {
    unsafeWindow.console.log(str);
}

function getCopper(data) {
    var arr = ["0", "0", "0"];
    var res = data.match(/(?:^| |-)(\d+)/g);

    if (data.indexOf("gold") > -1) {
        arr[0] = res.shift();
    }
    if (data.indexOf("silver") > -1) {
        arr[1] = res.shift();
    }
    if (data.indexOf("copper") > -1) {
        arr[2] = res.shift();
    }
    copper = (+arr[0] * 10000) + (+arr[1] * 100) + +arr[2];
    return copper;
}

function getProfitPct(revenue, profit) {
    if (profit == 0) {
        return 0;
    }
    return (((profit / revenue) * 100).toFixed(2));
}


if (document.URL.indexOf("crafting") > -1) {
    pageType = "crafting";
} else if (document.URL.indexOf("/recipe/") > -1) {
    pageType = "recipe";
} else if (document.URL.indexOf("/search/") > -1) {
    if (document.URL.indexOf("recipes=1") > -1) {
        pageType = "crafting";
    } else {
        pageType = "search";
    }
} else if (document.URL.indexOf("item") > -1) {
    pageType = "item";
}

if (pageType == "normal" || pageType == "crafting" || pageType == "search") {
    for (var i = 1; i < rows.length; i++) {
        log("Here");
        var row = rows[i].children;
        if (pageType == "crafting") {
            var buyPrice = getCopper(row[3].innerHTML);
            var sellPrice = getCopper(row[4].innerHTML);
            var margin = getCopper(row[5].innerHTML);
            profitIdx = 5;
        } else {
            var sellPrice = getCopper(row[4].innerHTML);
            var buyPrice = getCopper(row[5].innerHTML);
            var wanted = +row[6].innerHTML;
            var avail = +row[7].innerHTML;
            var margin = +getCopper(row[8].innerHTML);
            profitIdx = 8;
        }

        var profitPct = getProfitPct(sellPrice, margin);

        row[profitIdx].innerHTML += "&nbsp;(" + profitPct + "%)";
    }
} else if (pageType == "item") {

    var sellPrice = getCopper(rows[0].children[1].innerHTML);
    var buyPrice = getCopper(rows[1].children[1].innerHTML);
    var supply = rows[2].children[1].innerHTML;
    var demand = rows[3].children[1].innerHTML;
    var margin = (sellPrice * 0.85) - buyPrice;
    var profitPct = getProfitPct(sellPrice, margin);

    var newRow = rows[3].cloneNode(true);
    newRow.children[0].innerHTML = "Profit";
    newRow.children[1].innerHTML = margin + "c (" + profitPct + "%)";
    table.appendChild(newRow);
} else if (pageType == "recipe") {

    var sellPrice = getCopper(rows[2].children[1].innerHTML);
    var profit = getCopper(rows[4].children[1].innerHTML);
    var profitPct = getProfitPct(sellPrice, profit);
    field = rows[4].children[1];
    field.innerHTML = "foo";
}




