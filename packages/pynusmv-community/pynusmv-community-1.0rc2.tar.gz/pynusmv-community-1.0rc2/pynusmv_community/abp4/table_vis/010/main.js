d3.json("data/test.json", function(err, info){  
  
  /**************** SCENE SETUP *********************************************/
  var selection = d3.select("#selection")
                    .append("table")
                    .append("tr")
                    .selectAll("td")
                    .data(info.communities)
                    .enter()
                    .append("td")
                    .attr("class", function(e){ return "commu-"+e;} )
                    .text(function(e){ return e; });
  
  var table = d3.select("#table")
                .append("table");
  
  var thead = table.append("thead");
  thead.append("th").text("Variable");
  
  for( var i = -1; i <= info.bound; i++ ){
    thead.append("th").text(i);
  }
  
  var rows = table.append("tbody")
       .selectAll("tr")
       .data(  d3.entries(info.data) )
       .enter()
       .append("tr")
  
  var cells = rows.selectAll("td")
        .data( function(row){ 
          var key = [ row.key ];
          var cols= d3.values(row.value); 
          var all = key.concat(cols);
          return all;
        }  )
        .enter()
        .append("td")
        .attr("class", function(e){ 
          if( Array.isArray(e) ){
            return e.map(function(v){return "commu-"+v}).join(" ");
          } else {
            return ""
          }
        })
        .text( function(e) { return e; } );
  
  /**************** DYNAMIC BEHAVIOR ****************************************/
  selection.on("click", function(commu){
    
    var active   = d3.select(this).classed("active");
    d3.select(this).classed("active", !active);
    
    d3.selectAll(".commu-"+commu).attr("bgcolor", active ? "white" : "red" );
  });
  
});