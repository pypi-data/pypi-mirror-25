d3.queue()
  .defer(d3.json, "data/cluster_graph.json")
  .defer(d3.csv , "data/sequences.csv")
  .await(function(err, graph, sequences){  
  
  /**************** SCENE SETUP *********************************************/
  var width  = 800;
  var height = 600;

  var svg = d3.select("#graph")
              .append("svg")
              .attr("width", width)
              .attr("height",height)
              .append("g")
              .attr("width", "100%")
              .attr("height","100%");
  
  /**************** PLOTTING THE GRAPH **************************************/
  // NOTE: On ajoute les noeuds *APRES* les edges pour que les noeuds soient 
  //       au dessus des edges et pas l'inverse
  var edges= svg.selectAll("line")
              .data(graph.edges)
              .enter()
              .append("line")
              .attr("x1",   function(e){ return graph.nodes[e.src].x;      })
              .attr("y1",   function(e){ return graph.nodes[e.src].y;      })
              .attr("x2",   function(e){ return graph.nodes[e.dst].x;      })
              .attr("y2",   function(e){ return graph.nodes[e.src].y;      })
              .attr("style",function(e){ 
                return edge_style(graph.nodes[e.src], .1)(e); 
              })

  var nodes= svg.selectAll("circle")       // on selectionne tous les cercles
               .data(graph.nodes)          // on les joint avec les données
               .enter()                    // pr toutes les val sans node associe
               .append("circle")           // on ajoute un element dans le dom
               .attr("r", function(dta){   // et on en sette un attribut
                 return 4*dta.normal;
               })
               // nodes styling 
               .attr("stroke", "white")
               .attr("stroke-width", "2px")
               .attr("fill", function(vertex){
                 return d3.schemeCategory20b[vertex.id % 20];
               })


  /**************** DYNAMIC GRAPH LAYOUT ************************************/
  var force = d3.forceSimulation(graph.nodes)
                .force('charge', d3.forceManyBody().strength(-70))
                .force('center', d3.forceCenter(width / 2, height / 2))// l'objet layout (utilise tous les defaults)
                .on("tick", function(){   // mise a jour periodique du graphe
                    nodes.attr("cx", function(node){return node.x })                                       
                         .attr("cy", function(node){return node.y });
                         
                    edges.attr("x1", function(e){ return graph.nodes[e.src].x; })
                         .attr("y1", function(e){ return graph.nodes[e.src].y; })
                         .attr("x2", function(e){ return graph.nodes[e.dst].x; })
                         .attr("y2", function(e){ return graph.nodes[e.dst].y; });
                    });
  
  /**************** INTERACTIVE FEATURES ************************************/
  // support du drag and drop pour les noeuds
  nodes.call( d3.drag().on("drag", function(vertex){
    // update the object to reflect the dragged pos
    vertex.x = d3.event.x;
    vertex.y = d3.event.y;
    
    // update the node's element 
    d3.select(this).attr("cx", vertex.x).attr("cy", vertex.y);
    
    // update the afferent edges
    edges.filter(function(e) { return e.src == vertex.id; })
         .attr("x1", vertex.x)
         .attr("y1", vertex.y);
    edges.filter(function(e) { return e.dst == vertex.id; })
         .attr("x2", vertex.x)
         .attr("y2", vertex.y);
  }));

  // support du zoom unzoom pour le canvas svg
  d3.select("#graph").call(d3.zoom().on("zoom", function(){ 
    return svg.attr("transform", d3.event.transform) 
  }));
  
  /* ----- Highlighting/Fade out adjacent edges while hovering a node ---- */
  nodes.on("mouseenter", function(vertex){
    edges.filter(src_or_dst(vertex))
         .attr("style", edge_style(vertex,  1) )
  });
  nodes.on("mouseleave", function(vertex){
    edges.filter(src_or_dst(vertex))
         .attr("style", edge_style(vertex, .1) )
  });
  
  /* -------------- Display the elements details upon clicking  --------- */
  nodes.on("click", community_show_details);
  edges.on("click", edge_show_details);
  
  /**************** UTILITY FUNCITONS ************************************/
  
  /*----------------------------------------------------------------------
   * Displays the details of community `commu` inside the #info block
   *---------------------------------------------------------------------*/
  function community_show_details(commu){
    var text = "<h1>Comunity "+commu.community+"("+commu.size+" nodes)</h1>"
    // TODO REMOVE ME
    text    += "<div id='cloud'></div>"
    text    += "<div id='current-bubble' style='border: 1px solid red; display: inline-block; width: 95%; height:5em'></div>"
    text    += "<div>"
    text    += "<table>"
    text    += "<tr><th>Count</th><th>Sequence</th></tr>"
    text    += "</table>"
    text    += "</div>"
    
    d3.select("#info").html(text)
    
    var rows = d3.select("#info")
                 .select("table")
                 .selectAll("tr.current")
      .data(sequences)
      .enter()
      .filter(function(l){return l.CommunityNo == commu.community ; })
      .append("tr")
      .attr("class", "current");
      
    rows.append('td').html(function(l){ return l.Count    ;});
    rows.append('td').html(function(l){ return l.Sequence ;});
    
    // TODO REMOVE ME
    community_show_cloud(commu)
  }
  
  /*----------------------------------------------------------------------
   * Displays the details of edge `edge` inside the #info block
   *---------------------------------------------------------------------*/
  function edge_show_details(edge){
    var text = "<h1>Edge "+edge.src+" -- "+edge.dst+"</h1>";
    text    += "Weight : "+edge.weight
    
    d3.select("#info").html(text);
  }
  
  /*----------------------------------------------------------------------
   * Builds the style for an edge adjacent to some `vertex`. The style is
   * parameterized with `opacity` to highlight or fade it out.
   *
   * This function returns a function which can be passed to 'attr' to 
   * properly configure the style of an edge
   *---------------------------------------------------------------------*/
  function edge_style(vertex, opacity){
    // renvoie une fn currifiee
    return function(e){ 
       var e_color = "stroke:"+d3.schemeCategory20b[vertex.id % 20];
       var e_width = "stroke-width:"+( e.thickness / 2 );
       var e_opac  = "stroke-opacity:"+opacity;
       return e_color+";"+e_width+";"+e_opac;
    };
  }
  
  /*----------------------------------------------------------------------
   * Builds a filter testing whether vertex is adjacent to some edge.
   *
   * This function returns an other function which can be used as a filter
   *---------------------------------------------------------------------*/
  function src_or_dst(vertex){
    // renvoie une fn currifiee
    return function(edge){
      return edge.src == vertex.id || edge.dst == vertex.id;
    }
  }
  
  /* =========== EXPERIMENTAL ===============================================*/
  function community_show_cloud(node){
    
    var words = sequences.filter(function(l){ 
                    return l.CommunityNo == node.community 
                })
    
    // Spot the min and max of the array
    var w_min = Infinity;
    var w_tot = 0;                               // total mass
    for(var i = 0; i < words.length; i++){
      var word = words[i];
      i_cnt    = parseInt(word.Count);
      w_min    = Math.min(w_min, i_cnt);
      w_tot   += i_cnt;
    }
    
    // normalize the sizes of the words
    for(var i = 0; i < words.length; i++){
      var word    = words[i];
      word.normal = parseInt(word.Count) / w_tot;
    }
    
    
    var cloud_width = 430;
    var cloud_height= 430;
    
    var frame = d3.select("#cloud")
                  .append("svg")
                  .attr("width",  cloud_width)
                  .attr("height", cloud_height)
                  .append("g");
                    
    var bubbles = frame.selectAll("circle")
                  .data(words)
                  .enter()
                  .append("circle")
                  .attr("r",    function(w){ return Math.sqrt(w.normal)*cloud_width/2 })
                  .attr("fill", function(w){ return d3.schemeCategory20b[w.Count % 20] })
    
    d3.forceSimulation(words)
                .force('center', d3.forceCenter(cloud_width / 2, cloud_height / 2))
                .force('collide',d3.forceCollide().radius(function(w){return Math.sqrt(w.normal)*cloud_width/2 }))
                .on("tick", function(){   // mise a jour periodique du graphe
                    bubbles.attr("cx", function(w){return w.x })                                       
                         .attr("cy", function(w){return w.y });
                    });
    
    // the transform *must* be applied on a different node than the one who 
    // received the event        
    d3.select("#cloud").call(d3.zoom().on("zoom", function(){ 
      frame.attr("transform", d3.event.transform );
    }));
    
    
    bubbles.on("mouseenter", function(w){
      d3.select("#current-bubble")
        .html("<span style='position: absolute; width: 100%; height: 100%; text-align:center; font-size: 150%'>"+w.Sequence+"  ("+w.Count+" times)</span>")
    });
    
    bubbles.on("mouseleave", function(w){
      d3.select("#current-bubble").html("")
    });
    
  }
  
    
});