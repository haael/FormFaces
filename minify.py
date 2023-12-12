#!/usr/bin/python3


from rjsmin import jsmin
from pathlib import Path


scripts = [
  "js/userAgent.js",
  "js/inheritance.js",
  "js/stackTrace.js",
  "js/assert.js",
  "js/monitor.js",
  "js/methodCall.js",
  "js/uniqueId.js",
  
  "xml/exception.js",
  "xml/loadDocument.js",
  "xml/importNode.js",
  "xml/namespaces.js",
  "xml/serialize.js",
  "xml/regexes.js",
  "xml/qualifiedName.js",
  
  "events/listener.js",
  "events/xmlEvent.js",
  "events/dispatch.js",
  
  "xpath/token.js",
  "xpath/tokenizer.js",
  "xpath/parser.js",
  "xpath/exception.js",
  
  "xpath/xpath.js",
  "xpath/qName.js",
  "xpath/nodeSet.js",
  "xpath/context.js",
  "xpath/axis.js",
  "xpath/nodeTest.js",
  "xpath/expression.js",
  "xpath/locationPath.js",
  "xpath/step.js",
  "xpath/predicate.js",
  "xpath/function.js",
  "xpath/functionResolver.js",
  "xpath/coreFunctions.js",
  
  "xforms/exception.js",
  "xforms/parser.js",
  "xforms/initialize.js",
  "xforms/xform.js",
  "xforms/object.js",
  "xforms/submission.js",
  "xforms/instance.js",
  "xforms/binding.js",
  "xforms/model.js",
  "xforms/dependencyGraph.js",
  
  "xforms/xpathFunctions.js",
  
  "xforms/controls/control.js",
  "xforms/controls/container.js",
  "xforms/controls/label.js",
  "xforms/controls/input.js",
  "xforms/controls/textArea.js",
  "xforms/controls/secret.js",
  "xforms/controls/output.js",
  "xforms/controls/select.js",
  "xforms/controls/trigger.js",
  "xforms/controls/group.js",
  "xforms/controls/repeat.js",
  "xforms/controls/switch.js",
  "xforms/controls/case.js",
  "xforms/controls/submit.js",

  "xforms/actions/action.js",
  "xforms/actions/series.js",
  "xforms/actions/load.js",
  "xforms/actions/message.js",
  "xforms/actions/setvalue.js",
  "xforms/actions/insert.js",
  "xforms/actions/delete.js",
  "xforms/actions/toggle.js",
  "xforms/actions/dispatch.js",
  "xforms/actions/rebuild.js",
  "xforms/actions/recalculate.js",
  "xforms/actions/revalidate.js",
  "xforms/actions/refresh.js",
  "xforms/actions/send.js",
  
  "xforms/loaded.js"
]


if __name__ == '__main__':
	content = []
	for js_file in scripts:
		content.append((Path('Source') / Path(js_file)).read_text('utf-8'))
	
	with Path('formfaces.min.js').open('w') as dst:
		dst.write(jsmin("\n\n".join(content)))
	
	with Path('formfaces.min.css').open('w') as dst:
		dst.write(Path('Examples/Test Pages/xforms.css').read_text('utf-8'))


