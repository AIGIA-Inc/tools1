# -*- coding: utf-8 -*-

import shutil
from typing import Any

from collections.abc import MutableSequence, Sequence, Iterable
from graphviz import Digraph

def traverse(data, relations, accounts, id, depth):
	depth = depth + 1
	user_cursor = relations.find({'to_id': id})
	for user_relation in user_cursor:
		user_id = user_relation['from_id']
		type = user_relation['type']
		user = accounts.find_one({'user_id': user_id})
		if user:
			data.append({'depth': depth, 'username': user['username']})
			traverse(data, relations, accounts, user_id, depth)


def relation_tree(aig, rootuser):
	data: list = []
	if aig:
		accounts = aig.accounts
		if accounts:
			relations = aig.relations
			if relations:
				system = accounts.find_one({'username': rootuser})
				system_id = system['user_id']
				data.append({'depth': 0, 'username': system['username']})
				traverse(data, relations, accounts, system_id, 0)
			else:
				raise Exception("cursor error")
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")
	return data

def nickname(account):
	result = ''
	if account:
		content = account['content']
		if content:
			result = content['nickname']
	#
	#
	return result

def subscribe_type(stripe, username):
	subscribe = stripe.is_subscribe(username)
	result: str = ""
	if subscribe == 1:
		result = "課金"
	elif subscribe == 0:
		result = "非課金"
	elif subscribe == -1:
		result = "不明"
	elif subscribe == -2:
		result = "未登録"
	elif subscribe == -3:
		result = "エラー"
	return result

def add_user_row(stripe, accounts, relations, user, data):
	if user['type'] == '':
		trainer = None
		studio = None
		company = None
		trainer_rel = relations.find_one({'from_id': user['user_id']})
		if trainer_rel:
			trainer = accounts.find_one({'user_id': trainer_rel['to_id']})
			if trainer:
				studio_rel = relations.find_one({'from_id': trainer['user_id']})
				if studio_rel:
					studio = accounts.find_one({'user_id': studio_rel['to_id']})
					if studio:
						company_rel = relations.find_one({'from_id': studio['user_id']})
						if company_rel:
							company = accounts.find_one({'user_id': company_rel['to_id']})
						#
					#
				#
			#
		#
		subscribe: str = subscribe_type(stripe, user['username'])
		data.append({'username': user['username'], "subscribe": subscribe, "date": user['create'],
					 'auth': int(user['auth']), 'type': user['type'], "user": nickname(user),
					 "trainer": nickname(trainer),
					 "studio": nickname(studio), "company": nickname(company)})

def add_trainer_row(stripe, accounts, relations, trainer, data):
	if trainer['type'] == 'trainer':
		studio = None
		company = None
		studio_rel = relations.find_one({'from_id': trainer['user_id']})
		if studio_rel:
			studio = accounts.find_one({'user_id': studio_rel['to_id']})
			if studio:
				company_rel = relations.find_one({'from_id': studio['user_id']})
				if company_rel:
					company = accounts.find_one({'user_id': company_rel['to_id']})
				#
			#
		#
		subscribe: str = subscribe_type(stripe, trainer['username'])
		data.append({'username': trainer['username'], "subscribe": subscribe, "date": trainer['create'],
					 'auth': int(trainer['auth']), 'type': trainer['type'], "user": nickname(trainer), "trainer": "",
					 "studio": nickname(studio), "company": nickname(company)})

def accounts(aig, skip, limit, stripe):
	data: list = []
	if aig:
		relations = aig.relations
		accounts = aig.accounts
		if accounts:

			user_cursor = accounts.find({"$or": [{"type": ""}, {"type": "trainer"}]}).skip(skip).limit(limit)
			for user in user_cursor:
				add_user_row(stripe, accounts, relations, user, data)
				add_trainer_row(stripe, accounts, relations, user, data)

		else:
			raise Exception("collection error")
	#
	else:
		raise Exception("database error")
	return data


# 逆数
def reciprocal(dev: int) -> float:
	result: float = 0.0
	if dev != 0:
		result = 1 / dev
	return result


def belongfromall(relations, user_id) -> Iterable:
	return relations.find({"$and": [{'from_id': user_id}, {"type": "belongs"}]})


def belongtoall(relations, user_id) -> Iterable:
	return relations.find({"$and": [{'to_id': user_id}, {"type": "belongs"}]})


def totalling(aig, studio_name, stripe) -> (int, Any):
	def subscribe_count(accounts, relations, stripe, user_id):
		count: int = 0
		account: Any = accounts.find_one({'user_id': user_id})
		subscribe: Any = stripe.is_subscribe(account['username'])
		if subscribe == 1:
			links: Iterable = belongfromall(relations, account['user_id'])
			if links:
				count = len(list(links))
			#
		#
		return count, account

	result = {"studio": "", "count": 0.0}
	if aig:
		relations: Any = aig.relations
		accounts: Any = aig.accounts
		if accounts:
			count: float = 0.0
			studio: Any = accounts.find_one({"username": studio_name})
			if studio:
				if studio['type'] == 'studio':
					result["studio"] = studio['username']
					for trainer_rel in belongtoall(relations, studio['user_id']):
						up_links, trainer = subscribe_count(accounts, relations, stripe, trainer_rel['from_id'])
						count += reciprocal(up_links)
						if trainer:
							for user_rel in belongtoall(relations, trainer['user_id']):
								up_links, user = subscribe_count(accounts, relations, stripe, user_rel['from_id'])
								count += reciprocal(up_links)
				#
				#
				#
				#
				else:
					raise Exception("not studio type")
			else:
				raise Exception("studio not found.")
		else:
			raise Exception("collection error.")
	else:
		raise Exception("database error.")

	result["count"] = count
	return result


def guest(aig, rootuser, type, skip, limit):
	data: list = []
	if aig:
		relations = aig.relations
		accounts = aig.accounts
		if accounts:
			account = accounts.find_one({'username': rootuser})
		if relations:
			aggrigation_stages = [
				{'$match': {'type': 'belongs'}},
				{'$match': {'to_id': account['user_id']}},
				{'$graphLookup': {
					'from': 'relations',
					'startWith': '$to_id',
					'connectFromField': 'from_id',
					'connectToField': 'to_id',
					'as': 'belongs',
					'depthField': 'depth'
				}},
				{'$unwind': {'path': '$belongs'}},
				{'$replaceRoot': {'newRoot': '$belongs'}},
				{'$lookup': {
					'from': 'accounts',
					'localField': 'to_id',
					'foreignField': 'user_id',
					'as': 'upper'
				}},
				{'$lookup': {
					'from': 'accounts',
					'localField': 'from_id',
					'foreignField': 'user_id',
					'as': 'lower'
				}},
				{'$project': {
					'type': 1,
					'enabled': 1,
					'depth': 1,
					'upper': 1,
					'upper': {
						'type': 1,
						'username': 1,
						'content': {
							'stripe_id': 1
						}
					},
					'lower': 1,
					'lower': {
						'type': 1,
						'username': 1,
						'content': {
							'stripe_id': 1
						}
					}
				}},
				{'$unwind': {'path': '$lower'}},
				{'$group': {
					'_id': '$lower.username',
					'type': {
						'$first': '$lower.type'
					},
					'stripe_id': {
						'$first': '$lower.content.stripe_id'
					}
				}},
				{'$match': {'type': type}},
				{'$skip': skip},
				{'$limit': limit}
			]


			relations_cursor = relations.aggregate(aggrigation_stages)
			for relation in relations_cursor:
				type = relation['type']
				if type == '':
					type = 'user'
				data.append({'username': relation['_id'], 'type': type, 'stripe_id': relation['stripe_id']})
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")
	return data


def valid_relation(aig, includevalid):
	data: list = []
	if aig:
		accounts = aig.accounts
		if accounts:
			#account = accounts.find_one({'username': rootuser})
			relations = aig.relations
			if relations:

				relations_cursor = relations.find({})
				for relation in relations_cursor:
					from_user_id = relation['from_id']
					from_user = accounts.find_one({'user_id': from_user_id})
					to_user_id = relation['to_id']
					to_user = accounts.find_one({'user_id': to_user_id})
					type = relation['type']
					if from_user and to_user:
						if includevalid:
							data.append({'from': from_user['username'], 'to': to_user['username'], "type": type})
					elif not from_user:
						data.append({'from': str(from_user_id), 'to': to_user['username'], "type": type})
					elif not to_user:
						data.append({'from': str(from_user_id), 'to': str(to_user_id), "type": type})

			else:
				raise Exception("cursor error")
		else:
			raise Exception("relation error")
	else:
		raise Exception("database error")
	return data


def color_and_shape(type):
	result = ("gray80", "parallelogram", "9")
	if type == 'manage':
		result = ("pink", "hexagon", "9")
	elif type == 'company':
		result = ("chocolate1", "octagon", "9")
	elif type == 'studio':
		result = ("aquamarine1", "house", "9")
	elif type == 'trainer':
		result = ("gold1", "diamond", "9")
	elif type == '':
		result = ("gray90", "oval", "9")
	return result


def relation_graph(aig, output, rootuser, maxDepth, engine):
	if aig:
		accounts = aig.accounts
		if accounts:
			account: Any = accounts.find_one({'username': rootuser})
			if account:
				relations = aig.relations
				if relations:
					aggrigation_stages: list = [
						{'$match': {'type': 'belongs'}},
						{'$match': {'to_id': account['user_id']}},
						{'$graphLookup': {
							'from': 'relations',
							'startWith': '$to_id',
							'connectFromField': 'from_id',
							'connectToField': 'to_id',
							'as': 'belongs',
							'maxDepth': maxDepth,
							'depthField': 'depth'
						}},
						{'$unwind': {'path': '$belongs'}},
						{'$replaceRoot': {'newRoot': '$belongs'}},
						{'$lookup': {
							'from': 'accounts',
							'localField': 'to_id',
							'foreignField': 'user_id',
							'as': 'upper'
						}},
						{'$lookup': {
							'from': 'accounts',
							'localField': 'from_id',
							'foreignField': 'user_id',
							'as': 'lower'
						}},
						{'$unwind': {'path': '$lower'}},
						{'$unwind': {'path': '$upper'}},
						{'$group': {
							'_id': '$_id',
							'type': {'$first': '$type'},
							'user_type': {'$first': '$lower.type'},
							'from_user_name': {'$first': '$upper.username'},
							'to_user_name': {'$first': '$lower.username'}
						}}
					]
					relations_cursor = relations.aggregate(aggrigation_stages)

					# レイアウト一覧
					# circo, dot, fdp, neato, nop, nop1, nop2, osage, patchwork, sfdp, twopi

					graph = Digraph(format="svg", engine=engine)
					graph.attr(fontname='MS Gothic')

					color, shape, fontsize = color_and_shape(account['type'])
					graph.node(account['username'], shape=shape, fontsize=fontsize, style="filled", color=color)

					for relation in relations_cursor:

						type = relation['type']
						from_user_name = relation['from_user_name']
						to_user_name = relation['to_user_name']

						if from_user_name and to_user_name:
							color, shape, fontsize = color_and_shape(relation['user_type'])

						graph.node(to_user_name, shape=shape, fontsize=fontsize, style="filled", color=color)
						graph.edge(to_user_name, from_user_name, fontsize="8", label=type)

					graph.render("aig")
					shutil.move('aig.svg', output)

				else:
					raise Exception("cursor error")
			else:
				raise Exception("account not found")
		else:
			raise Exception("accounts error")
	else:
		raise Exception("database error")


def repair(aig):
	if aig:
		accounts = aig.accounts
		if accounts:
			relations = aig.relations
			if relations:
				relations.delete_many({'$or': [{'from_id': None}, {'to_id': None}]})
			else:
				raise Exception("cursor error")
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")


def user_by_type(aig, type, skip, limit):
	data: list = []
	if aig:
		accounts = aig.accounts
		if accounts:

			users_cursor: Any = accounts.find({'type': type}).skip(skip).limit(limit)
			for user in users_cursor:
				username = user['username']
				content = user['content']
				nickname = content['nickname']
				data.append({'username': username, "nickname": nickname})
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")
	return data
