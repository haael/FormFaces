// Copyright (c) 2000-2005 Progeny Systems Corporation.
//
// Consult license.html in the documentation directory for licensing
// information.

new EventListener(window, "load", "default", async function() {
  if (!document.body) {
    document.body = document.getElementsByTagName("body")[0];
  }
  
//  // Display a loading message while the page is loading.
//  while (document.body.hasChildNodes()) {
//    document.body.removeChild(document.body.firstChild);
//  }
//  
//  var message = document.createElement("p");
//  
//  message.style.font  = "large sans-serif";
//  message.style.color = "#CCC";
//  
//  message.appendChild(document.createTextNode("Loading..."));
//  
//  document.body.appendChild(message);
  
  await async_monitor(XForm.initialize);
});
