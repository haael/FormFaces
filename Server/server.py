#!/usr/bin/python3.11


from enum import Enum
from sys import argv
from asyncio import run, sleep, CancelledError
from lxml.etree import fromstring as xml_from_string, tostring as xml_to_string, ElementTree, Element, XMLSyntaxError
from xmltodict import unparse as xml_from_dict
from aiohttp import web
from aiopath import Path
from xmltodict import parse as xml_to_dict, unparse as xml_from_dict


class ModelError(Exception):
	pass


MethodType = Enum('MethodType', 'GET POST')


def get(path):
	def decor(method):
		method.route = MethodType.GET, path
		return method
	return decor


def post(path):
	def decor(method):
		method.route = MethodType.POST, path
		return method
	return decor


class WebApp:
	def __init__(self, host, port):
		routes = web.RouteTableDef()
		for method in self.__class__.__dict__.values():
			if not hasattr(method, 'route'): continue
			meth, path = method.route
			if meth == MethodType.GET:
				routes.get(path)((lambda _method: lambda *args: _method(self, *args))(method))
			elif meth == MethodType.POST:
				routes.post(path)((lambda _method: lambda *args: _method(self, *args))(method))
			else:
				raise ValueError(f"Unknown method type {meth}.")
		
		self.app = web.Application()
		self.app.add_routes(routes)
		
		self.host = host
		self.port = int(port)
		
		self.post_namespace = 'https://github.com/haael/FormFaces'
		
		self.values = {'one':"First", 'two':"Second", 'tree':"Third"}
	
	@get('/')
	async def root(self, request):
		return web.Response(body=await Path('root.html').read_bytes(), content_type='application/xhtml+xml')
	
	@get('/{page}.html')
	async def page_html(self, request):
		page = Path('html/' + request.match_info['page'] + '.html')
		
		if not await page.exists():
			return web.Response(status=404, body=await Path('error/404.html').read_bytes(), content_type='application/xhtml+xml')
		
		return web.Response(body=await page.read_bytes(), content_type='application/xhtml+xml')
	
	@get('/formfaces.js')
	async def formfaces_js(self, request):
		return web.Response(body=await Path('../formfaces.min.js').read_bytes(), content_type='text/javascript')
	
	@get('/formfaces.css')
	async def xforms_css(self, request):
		return web.Response(body=await Path('../formfaces.min.css').read_bytes(), content_type='text/css')
	
	@get('/favicon.svg')
	async def favicon_svg(self, request):
		return web.Response(body=await Path('favicon.svg').read_bytes(), content_type='image/svg+xml')
	
	@post('/model.xml')
	async def model_xml(self, request):
		try:
			in_tree = ElementTree()
			in_tree._setroot(xml_from_string(await request.read()))
			
			add_values = {}
			del_values = set()
			
			for value in in_tree.xpath('/ns:model/ns:value', namespaces={'ns':self.post_namespace}):
				if value.attrib['id'] in add_values:
					raise ModelError(f"Duplicate id {value.attrib['id']}.")
				
				if value.attrib.get('delete', 'false') == 'true':
					if value.attrib['id'] not in self.values:
						raise ModelError(f"Could not delete nonexistent value: {value.attrib['id']}.")
					del_values.add(value.attrib['id'])
				else:
					add_values[value.attrib['id']] = dict(kv for kv in xml_to_dict(xml_to_string(value))['value'].items() if kv[0][0] != '@')
			
			for id_ in del_values:
				del self.values[id_]
			
			for id_, value in add_values.items():
				self.values[id_] = value
			
			out_tree = ElementTree()
			out_tree._setroot(Element('model'))
			out_tree.getroot().attrib['xmlns'] = self.post_namespace
			out_tree.getroot().text = "\n"
			
			for id_, value in self.values.items():
				if isinstance(value, str):
					child = xml_from_string(xml_from_dict({'value':{'@id':id_, '#text':value}}, full_document=False))
				else:
					child = xml_from_string(xml_from_dict({'value':value | {'@id':id_}}, full_document=False))
				
				child.tail = "\n"
				out_tree.getroot().append(child)
		
		except (XMLSyntaxError, ModelError) as error:
			err_tree = ElementTree()
			err_tree._setroot(Element('error'))
			err_tree.getroot().attrib['xmlns'] = self.post_namespace
			err_tree.getroot().text = error.__class__.__name__ + ": " + str(error)
			return web.Response(status=400, body=xml_to_string(err_tree.getroot()), content_type='application/xml')
		
		else:		
			return web.Response(body=xml_to_string(out_tree.getroot()), content_type='application/xml')
	
	async def start(self):
		runner = web.AppRunner(self.app)
		await runner.setup()
		self.site = web.TCPSite(runner, self.host, self.port)
		await self.site.start()
	
	async def stop(self):
		await self.site.stop()
	
	async def __aenter__(self):
		await self.start()
		return self
	
	async def __aexit__(self, *args):
		await self.stop()
	

async def main(*args):
	async with WebApp(*args) as webapp:
		while True:
			await sleep(3600)


if __name__ == '__main__':
	try:
		run(main('localhost', 5005))
	except KeyboardInterrupt:
		print()

