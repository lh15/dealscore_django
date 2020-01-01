$( ".upvote" ).click(function(event) {
  alert( "Handler for .click() called." );
  var linkID = event.target.parentNode.id;
  $.post( "/engine/upvote/"+linkID, {  })
  .done(function( data ) {
    alert( "Data Loaded: " + data );
  });
});

$( ".downvote" ).click(function(event) {
    var linkID = event.target.parentNode.id;
  alert( "Handler for .click() called." );
  $.post( "/engine/downvote/"+linkID , {  })
  .done(function( data ) {
    alert( "Data Loaded: " + data );
  });
});
