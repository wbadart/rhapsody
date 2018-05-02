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

// global.onload = getjson.bind(null, 'api/2YZyLoL8N0Wb9xBt1NhZWg', mkgraph);
global.getrec = function() {
    var {value} = document.getElementById('entry');
    function alert_recs(recs) {
        console.dir(recs);
        alert(JSON.stringify(recs.tracks));
    }
    getjson(`recommend/${value}`, alert_recs);
    return false;
}


function mkgraph([names, links]) {
    var colors = {
        'rhapsody_web.artist': '#d35e60',
        'rhapsody_web.song':   '#7293cb',
        'rhapsody_web.album':  '#84ba5b'
        }
    var name = {
        'rhapsody_web.artist': 'name',
        'rhapsody_web.song':   'title',
        'rhapsody_web.album':  'name'
    }
    var nodes = new vis.DataSet(names.map(n => ({id: n.pk, label: n.fields[name[n.model]], color: colors[n.model]})))
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
