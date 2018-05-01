/**
 * static/rhapsody_web/graph.js
 *
 * Construct the interactive graph of musical entites.
 *
 * Project Rhapsody
 * created: APR 2018
 */

(function(global) {
'use strict';

global.onload = getjson.bind(null, 'api/2YZyLoL8N0Wb9xBt1NhZWg', mkgraph);

function mkgraph([names, links]) {
    var nodes = new vis.DataSet(names.map(n => ({id: n.pk, label: n.fields.name})))
      , edges = new vis.DataSet(links.map(([e1, e2]) => ({from: e1, to: e2})));
    new vis.Network(document.getElementById('graph'), {nodes, edges}, {});
}


function getjson(path, cb) {
    var req = new XMLHttpRequest();
    req.onload = function() {
        cb(JSON.parse(this.response));
    };
    req.open('GET', path);
    req.send();
    return req;
}

})(window);
