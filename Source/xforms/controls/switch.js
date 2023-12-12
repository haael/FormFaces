// Copyright (c) 2000-2005 Progeny Systems Corporation.
//               2023 haael
//
// Consult license.html in the documentation directory for licensing
// information.


// Creates a new switch control.
//
// Parameters:
//     element: The element from which the switch control was created.
//     bind:    The control's bind.
//     cases:   The switch's cases.
function XFormSwitchControl(element, bind, cases) {
  XFormControl.call(this, element, bind, cases);
  
  this.cases = cases;
  
  var clen = cases.length;
  for (var i = 0; i < clen; i++) {
    this.cases[i].switchControl = this;
  }
  
  for (var i = 0; i < clen; i++) {
    // If we found a selected case, make all the ones after it unselected.
    if (this.cases[i].selected) {
      for (var j = +i + 1; j < clen; ++j) {
        this.cases[j].selected = false;
      }
      
      return;
    }
  }
  
  // We didn't find any selected cases, so select the first one.
  this.cases[0].selected = true;
};

XFormSwitchControl.inherits(XFormControl);


XFormParser.prototype.parseSwitchControl = function(element) {
  return new XFormSwitchControl(
    element,

    this.getBindFor      (element),
    this.parseSwitchCases(element)
  );
};

XFormParser.prototype.parseSwitchCases = function(element) {
  var cases        = [];

  for (var child = element.firstChild; child != null; child = child.nextSibling) {
    if (child.nodeName.replace(/^.*:/, "") == "case" && child.namespaceURI == XmlNamespaces.XFORMS) {
      cases.push(this.parseCaseControl(child));
    }
  }
  
  return cases;
};


XFormSwitchControl.prototype.createInstance = function(binding, htmlNode, outerBinding, position) {
  return new XFormSwitchControlInstance(this, binding, htmlNode, outerBinding, position);
};

function XFormSwitchControlInstance(control, binding, htmlNode, outerBinding, position) {
  XFormControlInstance.call(this, control, binding, htmlNode, outerBinding, position);
  
  this.container = this.htmlNode;

  var cases = control.cases.length;  
  for (var i = 0; i < cases; i++) {
    var caseControl = control.cases[i];
    this.valueChangedOn(caseControl, ["xforms-select"]);
  }
};

XFormSwitchControlInstance.inherits(XFormControlInstance);

XFormSwitchControlInstance.prototype.getValue = function() {
  var cases  = this.cases.length;
  
  for (var i = 0; i < cases; i++) {
    var caseControl = this.cases[i];
    
    if(caseControl.selected) {
      return caseControl.caseName;
    }
  }

  return null;
};

XFormSwitchControlInstance.prototype.setValue = function(value) {
  var cases  = this.cases.length;
  
  for (var i = 0; i < cases; i++) {
    var caseControl = this.cases[i];
    
    if(caseControl.caseName == value) {
      caseControl.toggle();
      return;
    }
  }

  this.cases[0].toggle();
};

XFormSwitchControlInstance.prototype.addInstantiatedLabel = function(label) {
};

XFormSwitchControl        .prototype.toString =
XFormSwitchControlInstance.prototype.toString = function() {
  return "switch";
};
