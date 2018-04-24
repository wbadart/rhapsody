/**
 * static/rhapsody_web/graph.js
 *
 * Construct the interactive graph of musical entites.
 *
 * Project Rhapsody
 * created: APR 2018
 */

// (function(global) {
// 'use strict';

var nodes = new vis.DataSet([
    {id: 2, label: 'node 2'},
    {id: 3, label: 'node 3'},
    {id: 4, label: 'node 4'}
]);

var edges = new vis.DataSet([
      {from: 2, to: 3},
      {from: 3, to: 4},
]);

var container = document.getElementById('graph');
var network = new vis.Network(container, {nodes, edges}, {});

// })(window);
