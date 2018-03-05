# Rhapsody Development Plan

[Home] | [Repo]

[Project Demo URL]

## Project Technology

We will use MySQL, version 14.14 (which is available on `dsg1`) for our database. To interface between this database and our web-based application, we will implement a server-side API using the [Django] framework for Python. Facing the user will be a web-based client. We have identified a couple libraries which could drive our graph visualizations, and are primarily considering [D3.js].

Client routing will be handled by the server, but if it becomes evident by the end of the second milestone that this is an inappropriate architecture, we will factor routing into the client (supported by a SPA framework such as [Vue.js]).





[Home]: https://wbadart.github.io/rhapsody
[Repo]: https://github.com/wbadart/rhapsody

[Project Demo URL]: http://dsg1.crc.nd.edu/rhapsody
[D3.js]: https://d3js.org/
[Vue.js]: https://vuejs.org/
