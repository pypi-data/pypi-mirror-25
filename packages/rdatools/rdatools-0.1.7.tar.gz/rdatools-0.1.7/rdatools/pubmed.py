# -*- coding: utf-8 -*-
"""
PubMed.py

Written by Arno Simons

Released under GNU General Public License, version 3.0

Copyright (c) 2016-2017 Arno Simons

This file is part of RDAtools.

RDAtools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RDAtools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RDAtools.  If not, see <http://www.gnu.org/licenses/>.

"""
import re
import requests
import time
import urllib2
import xml.etree.ElementTree as ET
from Bio import Entrez
from Bio import Medline

from rdatools.functions import *


class PubMed(object):

	def __init__(self, email):
		Entrez.email = email
		self._search_results = None

	def __repr__(self):
		return u'<PubMed Connection({})>'.format(
			u'{} records, {} database'.format(
				self._search_results[u'count'],
				self._search_results[u'db'])
			if self._search_results else u'no search yet')

	def __len__(self):
		return self._search_results[u'count']

	def search(self, query, db=u'pmc'):
		'''
		Performs a search on PMC and saves results in self._search_results

		--> Also search PM?
		'''
		search = Entrez.read(
			Entrez.esearch(term=query, db=db, usehistory=u'y'))
		self._search_results = {
			u'db':db,
			u'query':query,
			u'count':int(search[u'Count']), 
			u'query_key':search[u'QueryKey'],
			u'webenv':search[u'WebEnv']}
		print u'Found {:.0f} records'.format(self._search_results[u'count'])
		return self._search_results

	def fetch_from(self, query=None, db=u'pmc', file=None,
		batch_size=100, maxfetch=75, rettype=u'medline', retmode=u'text'):
		'''
		Fetches records from 1) a query, 2) a saved search, or 3) a list of ids 
		and returns them in various formats
		
		--> Allow various output formats
		--> Noch für id list anpassen!
		'''
		print u'Fetching records from {} database'.format(db)
		if query:
			self.search(query, db)
		count = int(self._search_results[u'count'])
		if count <= maxfetch:
			print '\t...All {:.0f} records will be downloaded'.format(count)
		else:
			print '\t...maxfetch: {:.0f} (of {}) records will be downloaded'.format(maxfetch, count)
			count = maxfetch
		if maxfetch < batch_size:
			batch_size = maxfetch 
		for start in range(0, count,batch_size):
			end = min(count, start + batch_size)
			print(u'\t...Downloading record {} to {}'.format(start + 1, end))
			attempt = 0
			while attempt < 3:
				try:
					fetch_handle = Entrez.efetch(
						db=db,
						rettype=rettype,
						retmode=retmode,
						retstart=start,
						retmax=batch_size,
						webenv=self._search_results[u'webenv'],
						query_key=self._search_results[u'query_key'])
					attempt = 3
				except urllib2.HTTPError as err:
					if 500 <= err.code <= 599:
						print(u'Received error from server {}'.foramt(err))
						print(u'Attempt {} of 3'.format(attempt))
						attempt += 1
						time.sleep(15)
					else:
						raise
			data = fetch_handle.read()
			if file:
				mode = u'w' if start==0 else u'a'
				with open(file, mode) as out_handle:
					out_handle.write(data)
			fetch_handle.close()

	def fetch_pmc_xml(self, pmcids):
		'''
		Returns xml that contains all requested pmc records as nodes under <pmc-articleset>
		Each node/record starts with tag <article... 
		'''
		handle = Entrez.efetch(db='pmc', id=pmcids, rettype='medline', retmode='xml')
		return ''.join(handle)

	def fetch_pmc_metadata(self, pmcids):
		'''
		Returns metadata of pmc record or list of pmc records
		'''
		if isinstance(pmcids, list):
			pmcids = ','.join(pmcids)
		if not isinstance(pmcids,unicode):
			raise TypeError(u'pmcids must be string or list')
		handle = Entrez.efetch(db='pmc', id=pmcids, rettype='medline', retmode='text')
		metadata = list(Medline.parse(handle))
		for d in metadata:
			print '\n'
			print 'PMC ID: {}/ PMID: {}'.format(d['PMC'], d['PMID'])
			print 'Authors: {}'.format(d['FAU'])
			print 'Date: {}'.format(d['DP'])
			print 'Title: {}'.format(d['TI'])
			print 'Type: {}'.format(d['PT'])
		return metadata

	def webfetch_pmc(self, target, retmode=u'xml'):
		if re.match(u'\d+/?$', target):
			url = u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}'.format(target)
		elif re.match(u'PMC\d+/?$', target):
			url = u'https://www.ncbi.nlm.nih.gov/pmc/articles/{}'.format(target)
		elif re.match(u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC\d+/?$',target, ):
			url = target
		else:
			raise ValueError()
		hdr = {'User-Agent':'Mozilla/5.0'}
		req = urllib2.Request(url,headers=hdr)
		page = urllib2.urlopen(req)
		xml = page.read()
		if retmode == u'xml':
			return xml
		root = _xml_to_root(xml)
		if retmode == u'root':
			return root
		if retmode == u'text':
			text = u''
			for i in root.iter():
				if re.match(u'h\d$',i.tag):
					heading = u''.join(i.itertext())
					if not any(heading == i for i in [u'Formats:', u'PMC', 'Share']):
						text = u'\n\n'.join([text,heading])
				if i.tag == u'p':
					# if not u'class' in i.attrib 
					if not i.attrib.get(u'class') == u'address vcard':
						paragraph = u''.join(i.itertext())
						if not u'The NCBI web site requires JavaScript to function' in paragraph:
							text = u'\n\n'.join([text,paragraph])
			return text

	def id_converter(self, pid, from_type=u'pmcid', to_type=u'pmid'):
		'''
		Converts varius PubMed ID-types, e.g. PMID to PMCID

		--> Geht auch ID list?
		'''
		api = u'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
		params = {u'ids': pid, u'idtype': from_type} # 'tool':'RDAtools'
		r = requests.get(api, params)
		if r.status_code == 200:
			content = ET.fromstring(r.content)
			# print content
			for i in content.iter(tag=u'record'):
				if to_type in i.attrib.iterkeys():
					return i.attrib[to_type]
		else:
			print u'An Error occurred during id conversion! Status code: {}'.format(r.status_code)
		return u''

	def PMCID_to_PMID(self, PMCID):
		''' Converts PMCID to PMID
		'''
		return self.id_converter(PMCID, from_type=u'pmcid', to_type=u'pmid')

	def PMID_to_PMCID(self, PMID):
		''' Converts PMID to PMCID
		'''
		return self.id_converter(PMID, from_type=u'pmid', to_type=u'pmcid')

	def PMID_to_RID(self, PMID, xml):
		'''
		Returns ref ID used within xml for record with PMID

		--> also for Entrez type xmls!
		'''
		# improve by using XPath! https://docs.python.org/2/library/xml.etree.elementtree.html#elementtree-xpath
		root = xml_to_root(xml)
		for i in root.iter():
			if 'id' in i.attrib.iterkeys() and sum(map(
				lambda k: k == u'id',
				(k for j in i.iter() for k in j.attrib.iterkeys()))) == 1:
				for j in i.iter():
					if j.text == PMID: # for Entrez.xml
						return i.attrib['id']
					for v in j.attrib.itervalues(): # for web.xml
						if re.match(u'/pubmed/{}'.format(PMID),v):
							return i.attrib['id']
		return

	def citation_context(self, xml, RID, width=200, tags=[u'p',]):
		root = xml_to_root(xml)
		for i in root.iter():
			if any(i.tag == t for t in tags):
				context = ''
				precontexts = []
				if not isinstance(i.tag, basestring) and i.tag is not None:
					return # Wozu?
				if i.text:
					context = ''.join([context, i.text])
				for e in i:
					# if e.tag=='xref' and e.attrib['ref-type'] == 'bibr' and e.attrib['rid'] == RID:
					if e.attrib.get(u'rid') == RID:
						precontexts.append((len(context),context))
					for s in e.itertext():
						context = u''.join([context, s])
					if e.tail:
						context = u''.join([context, e.tail])
				contexts = [(p[1], context[p[0]:]) for p in precontexts]
				for i,c in enumerate(contexts):
					print u'\n{}\n{}<---{}--->{}'.format(i+1,c[0][-200:], RID, c[1][:200] )




# query = u'translational & research'
# query2 = u'clinician & scientists'
# file = u'test_papers.txt'

email = u'hallo@web.de'
p = PubMed(email)


PMID1 = u'23885955'
PMCID1 = u'PMC3733606'
PMCID2 = u'PMC24541'

print p.PMID_to_PMCID(PMID1)
print p.PMCID_to_PMID(PMCID1)

# print p.fetch_pmc_metadata([PMCID2,PMCID1])
xml_from_Entrez = p.fetch_pmc_xml([PMCID2,PMCID1])
xml_from_Entrez = p.fetch_pmc_xml([PMCID1])
xml_from_web = p.webfetch_pmc(PMCID1)
# print xml_from_web
# print xml_from_Entrez

print u'---------------'
RID = p.PMID_to_RID(u'4914589', xml_from_web)
print RID


dsfg
p.citation_context(xml_from_web, u'B46')
p.citation_context(xml_from_Entrez, u'B46')


asdf





# print p
# print p.id_converter(9843981)
# p.search(query)
# print p._search_results
# print p
# print len(p)
# # print p._search_results
# p.fetch_from(query2, file=file)
# print p


	

def webfetch_pmc(target, retmode=u'xml'):
	if re.match(u'\d+/?$', target):
		url = u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{}'.format(target)
	elif re.match(u'PMC\d+/?$', target):
		url = u'https://www.ncbi.nlm.nih.gov/pmc/articles/{}'.format(target)
	elif re.match(u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC\d+/?$',target, ):
		url = target
	else:
		raise ValueError()
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(url,headers=hdr)
	page = urllib2.urlopen(req)
	xml = page.read()
	if retmode == u'xml':
		return xml
	root = _xml_to_root(xml)
	if retmode == u'root':
		return root
	if retmode == u'text':
		text = u''
		for i in root.iter():
			if re.match(u'h\d$',i.tag):
				heading = u''.join(i.itertext())
				if not any(heading == i for i in [u'Formats:', u'PMC', 'Share']):
					text = u'\n\n'.join([text,heading])
			if i.tag == u'p':
				# if not u'class' in i.attrib 
				if not i.attrib.get(u'class') == u'address vcard':
					paragraph = u''.join(i.itertext())
					if not u'The NCBI web site requires JavaScript to function' in paragraph:
						text = u'\n\n'.join([text,paragraph])
		return text
	



### Open PMC Fulltext through Firefox (to bypass restrictions in Medlife API)
site1 = u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3733606/'
site2 = u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC24541/'
site3 = u'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC369722/'


print webfetch_pmc('PMC2829707', retmode=u'text')



def PMID_to_RID(PMID,xml):
	# improve by using XPath! https://docs.python.org/2/library/xml.etree.elementtree.html#elementtree-xpath
	root = _xml_to_root(xml)
	for i in root.iter():
		if 'id' in i.attrib.iterkeys() and sum(map(
			lambda k: k == u'id',
			(k for j in i.iter() for k in j.attrib.iterkeys()))) == 1:
			for j in i.iter():
				for v in j.attrib.itervalues():
					if re.match(u'/pubmed/{}'.format(PMID),v):
						return i.attrib['id']
	return
		
PMID = '12944573'
xml = webfetch_pmc('PMC2829707', retmode=u'xml')
print PMID_to_RID(PMID,xml)

cbxcv

def citation_context(xml, RID, width=200, tags=[u'p',]):
	root = _xml_to_root(xml)
	for i in root.iter():
		if any(i.tag == t for t in tags):
			context = ''
			precontexts = []
			if not isinstance(i.tag, basestring) and i.tag is not None:
				return # Wozu?
			if i.text:
				context = ''.join([context, i.text])
			for e in i:
				if e.tag=='xref' and e.attrib['ref-type'] == 'bibr' and e.attrib['rid'] == RID:
					precontexts.append((len(context),context))
				for s in e.itertext():
					context = ''.join([context, s])
				if e.tail:
					context = ''.join([context, e.tail])
			contexts = [(p[1], context[p[0]:]) for p in precontexts]
			for i,c in enumerate(contexts):
				print u'\n{}\n{}<---{}--->{}'.format(i,c[0][-200:], u'B2', c[1][:200] )



target = PMID_to_RID(PMID,xml)
citation_context(xml_from_Entrez,target)




ssfgsfc



def _citcon(self, target):
    context = ''
    precontexts = []
    tag = self.tag
    if not isinstance(tag, basestring) and tag is not None:
        return
    if self.text:
        context = ''.join([context, self.text])
    for e in self:
        if e.tag=='xref' and e.attrib['ref-type'] == 'bibr' and e.attrib['rid'] == target:
            precontexts.append((len(context),context))
        for s in e.itertext():
            context = ''.join([context, s])
        if e.tail:
            context = ''.join([context, e.tail])
    return [(p[1], context[p[0]:]) for p in precontexts]


def citcon(tree, target, width=200, tag='p'):
    for p in tree.iter(tag=tag):
        contexts = p._citcon(target)
        for i,c in enumerate(contexts):
            print u'\n{}\n{}<---{}--->{}'.format(i,c[0][-200:], u'B2', c[1][:200] )






sdfgsdf




sdfgsdf


#######


def _citcon(self, target):
    context = ''
    precontexts = []
    tag = self.tag
    if not isinstance(tag, basestring) and tag is not None:
        return
    if self.text:
        context = ''.join([context, self.text])
    for e in self:
        if e.tag=='xref' and e.attrib['ref-type'] == 'bibr' and e.attrib['rid'] == target:
            precontexts.append((len(context),context))
        for s in e.itertext():
            context = ''.join([context, s])
        if e.tail:
            context = ''.join([context, e.tail])
    return [(p[1], context[p[0]:]) for p in precontexts]


def citcon(tree, target, width=200, tag='p'):
    for p in tree.iter(tag=tag):
        contexts = p._citcon(target)
        for i,c in enumerate(contexts):
            print u'\n{}\n{}<---{}--->{}'.format(i,c[0][-200:], u'B2', c[1][:200] )


import types
ET.Element._citcon=_citcon


def reflist(tree):
    reflist = []
    for rl in tree.iter(tag='ref-list'):
        for r in rl.iter('ref'):
            ref = {'ref_id':r.attrib['id'], 'authors':[]}
            for m in r.iter('mixed-citation'):
                ref['u_type'] = m.attrib['publication-type']
                for i in m.iter():
                    if i.tag in ['mixed-citation', 'surname', 'given-names']:
                        continue
                    if i.tag == 'name':
                        name = {}
                        for n in i.iter():
                            if n.tag == 'surname':
                                name['lastname'] = n.text
                                continue
                            if n.tag == 'given-names':
                                name['firstname'] = n.text
                                continue
                        ref['authors'].append(name)
                        continue
                    if i.tag == 'year':
                        ref['date'] = i.text
                        continue
                    if i.tag == 'article-title':
                        ref['title'] = i.text
                        continue
                    if i.tag == 'pub-id':
                        if r.attrib['id'] == 'B37': # test
                            # pmc id not provided, e.g. in B37 of a = fetch_xml(['3733606'],retmode='html')
                            # But online it is! https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3733606/
                            print '\n\n--->',i.text
                            print '\n\n'
                        if i.attrib['pub-id-type'] == 'doi':
                            ref['doi'] = i.text
                            continue
                        if i.attrib['pub-id-type'] == 'pmid':
                            ref['pmid'] = i.text
                            continue
                    ref['med_{}'.format(i.tag)] = i.text
            yield ref


for r in reflist(a):
    print r
