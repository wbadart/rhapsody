/**
 * static/rhapsody_web/graph.js
 *
 * Construct the interactive graph of musical entites.
 * TEST CHANGE
 *
 * Project Rhapsody
 * created: APR 2018
 */

(function(global) {
'use strict';

global.onload = getjson.bind(null, 'test/10', mkgraph);


})(window);


function mkgraph([names, links]) {
    var nodes = new vis.DataSet(names.map((n, i) => ({id: n, label: n})))
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
