# -*- coding: utf-8 -*-

def key_in_dic(result, key, dictionary, default):
	if key in dictionary:
		result[key] = dictionary[key]
	else:
		result[key] = default
	return result


def prizm_default(shot):
	prizm = {}
	if 'prizm' in shot:
		if shot['prizm']:
			prizm = shot['prizm']
		else:
			prizm = {
				"ClubType": "",
				"DataList": [
					{'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0},
					{'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0},
					{'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0}
				]
			}
	else:
		prizm = {
			"ClubType": "",
			"DataList": [
				{'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0},
				{'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0},
				{'Value': 0}, {'Value': 0}, {'Value': 0}, {'Value': 0}
			]
		}
	return prizm


def shotdata(columns, shot, accounts):
	data = {}
	sm = shot['sm']
	prizm = prizm_default(shot)

	if "name" in columns:
		data["name"] = shot['name']
	if "platform" in shot:
		platform = shot['platform']
		if "username" in columns:
			user_id = shot['user_id']
			user = accounts.find_one({"user_id": user_id})
			if user:
				data["username"] = user["username"]
			else:
				data["username"] = ""
		if "description" in platform:
			description = platform["description"]
			if "club" in columns:
				data["club"] = description['club']
			if "score" in columns:
				data["score"] = description['score']
			if "postureScore" in columns:
				data = key_in_dic(data, "postureScore", description, 0)
			if "ballisticScore" in columns:
				data = key_in_dic(data, "ballisticScore", description, 0)
			if "studio" in columns:
				data = key_in_dic(data, "studio", description, "")
			if "sites" in columns:
				data = key_in_dic(data, "sites", description, "")

	if "前傾角度.address" in columns:
		data["前傾角度.address"] = round(sm['前傾角度']['address']['metrics'], 2)
	if "前傾角度.backswing" in columns:
		data["前傾角度.backswing"] = round(sm['前傾角度']['backswing']['metrics'], 2)
	if "前傾角度.top" in columns:
		data["前傾角度.top"] = round(sm['前傾角度']['top']['metrics'], 2)
	if "前傾角度.halfdown" in columns:
		data["前傾角度.halfdown"] = round(sm['前傾角度']['halfdown']['metrics'], 2)
	if "前傾角度.impact" in columns:
		data["前傾角度.impact"] = round(sm['前傾角度']['impact']['metrics'], 2)
	if "前傾角度.follow" in columns:
		data["前傾角度.follow"] = round(sm['前傾角度']['follow']['metrics'], 2)
	if "前傾角度.finish" in columns:
		data["前傾角度.finish"] = round(sm['前傾角度']['finish']['metrics'], 2)
	if "背骨の傾き.address" in columns:
		data["背骨の傾き.address"] = round(sm['背骨の傾き']['address']['metrics'], 2)
	if "背骨の傾き.backswing" in columns:
		data["背骨の傾き.backswing"] = round(sm['背骨の傾き']['backswing']['metrics'], 2)
	if "背骨の傾き.top" in columns:
		data["背骨の傾き.top"] = round(sm['背骨の傾き']['top']['metrics'], 2)
	if "背骨の傾き.halfdown" in columns:
		data["背骨の傾き.halfdown"] = round(sm['背骨の傾き']['halfdown']['metrics'], 2)
	if "背骨の傾き.impact" in columns:
		data["背骨の傾き.impact"] = round(sm['背骨の傾き']['impact']['metrics'], 2)
	if "背骨の傾き.follow" in columns:
		data["背骨の傾き.follow"] = round(sm['背骨の傾き']['follow']['metrics'], 2)
	if "背骨の傾き.finish" in columns:
		data["背骨の傾き.finish"] = round(sm['背骨の傾き']['finish']['metrics'], 2)
	if "首元の動き.address" in columns:
		data["首元の動き.address"] = round(sm['首元の動き']['address']['metrics'], 2)
	if "首元の動き.backswing" in columns:
		data["首元の動き.backswing"] = round(sm['首元の動き']['backswing']['metrics'], 2)
	if "首元の動き.top" in columns:
		data["首元の動き.top"] = round(sm['首元の動き']['top']['metrics'], 2)
	if "首元の動き.halfdown" in columns:
		data["首元の動き.halfdown"] = round(sm['首元の動き']['halfdown']['metrics'], 2)
	if "首元の動き.impact" in columns:
		data["首元の動き.impact"] = round(sm['首元の動き']['impact']['metrics'], 2)
	if "首元の動き.follow" in columns:
		data["首元の動き.follow"] = round(sm['首元の動き']['follow']['metrics'], 2)
	if "首元の動き.finish" in columns:
		data["首元の動き.finish"] = round(sm['首元の動き']['finish']['metrics'], 2)
	if "右腰の動き.address" in columns:
		data["右腰の動き.address"] = round(sm['右腰の動き']['address']['metrics'], 2)
	if "右腰の動き.backswing" in columns:
		data["右腰の動き.backswing"] = round(sm['右腰の動き']['backswing']['metrics'], 2)
	if "右腰の動き.top" in columns:
		data["右腰の動き.top"] = round(sm['右腰の動き']['top']['metrics'], 2)
	if "右腰の動き.halfdown" in columns:
		data["右腰の動き.halfdown"] = round(sm['右腰の動き']['halfdown']['metrics'], 2)
	if "右腰の動き.impact" in columns:
		data["右腰の動き.impact"] = round(sm['右腰の動き']['impact']['metrics'], 2)
	if "右腰の動き.follow" in columns:
		data["右腰の動き.follow"] = round(sm['右腰の動き']['follow']['metrics'], 2)
	if "右腰の動き.finish" in columns:
		data["右腰の動き.finish"] = round(sm['右腰の動き']['finish']['metrics'], 2)
	if "左腰の動き.address" in columns:
		data["左腰の動き.address"] = round(sm['左腰の動き']['address']['metrics'], 2)
	if "左腰の動き.backswing" in columns:
		data["左腰の動き.backswing"] = round(sm['左腰の動き']['backswing']['metrics'], 2)
	if "左腰の動き.top" in columns:
		data["左腰の動き.top"] = round(sm['左腰の動き']['top']['metrics'], 2)
	if "左腰の動き.halfdown" in columns:
		data["左腰の動き.halfdown"] = round(sm['左腰の動き']['halfdown']['metrics'], 2)
	if "左腰の動き.impact" in columns:
		data["左腰の動き.impact"] = round(sm['左腰の動き']['impact']['metrics'], 2)
	if "左腰の動き.follow" in columns:
		data["左腰の動き.follow"] = round(sm['左腰の動き']['follow']['metrics'], 2)
	if "左腰の動き.finish" in columns:
		data["左腰の動き.finish"] = round(sm['左腰の動き']['finish']['metrics'], 2)
	if "重心の動き_正面.address" in columns:
		data["重心の動き_正面.address"] = round(sm['重心の動き_正面']['address']['metrics'], 2)
	if "重心の動き_正面.backswing" in columns:
		data["重心の動き_正面.backswing"] = round(sm['重心の動き_正面']['backswing']['metrics'], 2)
	if "重心の動き_正面.top" in columns:
		data["重心の動き_正面.top"] = round(sm['重心の動き_正面']['top']['metrics'], 2)
	if "重心の動き_正面.halfdown" in columns:
		data["重心の動き_正面.halfdown"] = round(sm['重心の動き_正面']['halfdown']['metrics'], 2)
	if "重心の動き_正面.impact" in columns:
		data["重心の動き_正面.impact"] = round(sm['重心の動き_正面']['impact']['metrics'], 2)
	if "重心の動き_正面.follow" in columns:
		data["重心の動き_正面.follow"] = round(sm['重心の動き_正面']['follow']['metrics'], 2)
	if "重心の動き_正面.finish" in columns:
		data["重心の動き_正面.finish"] = round(sm['重心の動き_正面']['finish']['metrics'], 2)
	if "右膝の角度.address" in columns:
		data["右膝の角度.address"] = round(sm['右膝の角度']['address']['metrics'], 2)
	if "右膝の角度.backswing" in columns:
		data["右膝の角度.backswing"] = round(sm['右膝の角度']['backswing']['metrics'], 2)
	if "右膝の角度.top" in columns:
		data["右膝の角度.top"] = round(sm['右膝の角度']['top']['metrics'], 2)
	if "右膝の角度.halfdown" in columns:
		data["右膝の角度.halfdown"] = round(sm['右膝の角度']['halfdown']['metrics'], 2)
	if "右膝の角度.impact" in columns:
		data["右膝の角度.impact"] = round(sm['右膝の角度']['impact']['metrics'], 2)
	if "右膝の角度.follow" in columns:
		data["右膝の角度.follow"] = round(sm['右膝の角度']['follow']['metrics'], 2)
	if "右膝の角度.finish" in columns:
		data["右膝の角度.finish"] = round(sm['右膝の角度']['finish']['metrics'], 2)
	if "手元の浮き.address" in columns:
		data["手元の浮き.address"] = round(sm['手元の浮き']['address']['metrics'], 2)
	if "手元の浮き.backswing" in columns:
		data["手元の浮き.backswing"] = round(sm['手元の浮き']['backswing']['metrics'], 2)
	if "手元の浮き.top" in columns:
		data["手元の浮き.top"] = round(sm['手元の浮き']['top']['metrics'], 2)
	if "手元の浮き.halfdown" in columns:
		data["手元の浮き.halfdown"] = round(sm['手元の浮き']['halfdown']['metrics'], 2)
	if "手元の浮き.impact" in columns:
		data["手元の浮き.impact"] = round(sm['手元の浮き']['impact']['metrics'], 2)
	if "手元の浮き.follow" in columns:
		data["手元の浮き.follow"] = round(sm['手元の浮き']['follow']['metrics'], 2)
	if "手元の浮き.finish" in columns:
		data["手元の浮き.finish"] = round(sm['手元の浮き']['finish']['metrics'], 2)
	if "左膝の角度.address" in columns:
		data["左膝の角度.address"] = round(sm['左膝の角度']['address']['metrics'], 2)
	if "左膝の角度.backswing" in columns:
		data["左膝の角度.backswing"] = round(sm['左膝の角度']['backswing']['metrics'], 2)
	if "左膝の角度.top" in columns:
		data["左膝の角度.top"] = round(sm['左膝の角度']['top']['metrics'], 2)
	if "左膝の角度.halfdown" in columns:
		data["左膝の角度.halfdown"] = round(sm['左膝の角度']['halfdown']['metrics'], 2)
	if "左膝の角度.impact" in columns:
		data["左膝の角度.impact"] = round(sm['左膝の角度']['impact']['metrics'], 2)
	if "左膝の角度.follow" in columns:
		data["左膝の角度.follow"] = round(sm['左膝の角度']['follow']['metrics'], 2)
	if "左膝の角度.finish" in columns:
		data["左膝の角度.finish"] = round(sm['左膝の角度']['finish']['metrics'], 2)
	if "頭の動き.address" in columns:
		data["頭の動き.address"] = round(sm['頭の動き']['address']['metrics'], 2)
	if "頭の動き.backswing" in columns:
		data["頭の動き.backswing"] = round(sm['頭の動き']['backswing']['metrics'], 2)
	if "頭の動き.top" in columns:
		data["頭の動き.top"] = round(sm['頭の動き']['top']['metrics'], 2)
	if "頭の動き.halfdown" in columns:
		data["頭の動き.halfdown"] = round(sm['頭の動き']['halfdown']['metrics'], 2)
	if "頭の動き.impact" in columns:
		data["頭の動き.impact"] = round(sm['頭の動き']['impact']['metrics'], 2)
	if "頭の動き.follow" in columns:
		data["頭の動き.follow"] = round(sm['頭の動き']['follow']['metrics'], 2)
	if "頭の動き.finish" in columns:
		data["頭の動き.finish"] = round(sm['頭の動き']['finish']['metrics'], 2)
	if "両肩の傾き_正面.address" in columns:
		data["両肩の傾き_正面.address"] = round(sm['両肩の傾き_正面']['address']['metrics'], 2)
	if "両肩の傾き_正面.backswing" in columns:
		data["両肩の傾き_正面.backswing"] = round(sm['両肩の傾き_正面']['backswing']['metrics'], 2)
	if "両肩の傾き_正面.top" in columns:
		data["両肩の傾き_正面.top"] = round(sm['両肩の傾き_正面']['top']['metrics'], 2)
	if "両肩の傾き_正面.halfdown" in columns:
		data["両肩の傾き_正面.halfdown"] = round(sm['両肩の傾き_正面']['halfdown']['metrics'], 2)
	if "両肩の傾き_正面.impact" in columns:
		data["両肩の傾き_正面.impact"] = round(sm['両肩の傾き_正面']['impact']['metrics'], 2)
	if "両肩の傾き_正面.follow" in columns:
		data["両肩の傾き_正面.follow"] = round(sm['両肩の傾き_正面']['follow']['metrics'], 2)
	if "両肩の傾き_正面.finish" in columns:
		data["両肩の傾き_正面.finish"] = round(sm['両肩の傾き_正面']['finish']['metrics'], 2)
	if "重心の動き_後方.address" in columns:
		data["重心の動き_後方.address"] = round(sm['重心の動き_後方']['address']['metrics'], 2)
	if "重心の動き_後方.backswing" in columns:
		data["重心の動き_後方.backswing"] = round(sm['重心の動き_後方']['backswing']['metrics'], 2)
	if "重心の動き_後方.top" in columns:
		data["重心の動き_後方.top"] = round(sm['重心の動き_後方']['top']['metrics'], 2)
	if "重心の動き_後方.halfdown" in columns:
		data["重心の動き_後方.halfdown"] = round(sm['重心の動き_後方']['halfdown']['metrics'], 2)
	if "重心の動き_後方.impact" in columns:
		data["重心の動き_後方.impact"] = round(sm['重心の動き_後方']['impact']['metrics'], 2)
	if "重心の動き_後方.follow" in columns:
		data["重心の動き_後方.follow"] = round(sm['重心の動き_後方']['follow']['metrics'], 2)
	if "重心の動き_後方.finish" in columns:
		data["重心の動き_後方.finish"] = round(sm['重心の動き_後方']['finish']['metrics'], 2)
	if "グリップ位置.address" in columns:
		data["グリップ位置.address"] = round(sm['グリップ位置']['address']['metrics'], 2)
	if "グリップ位置.backswing" in columns:
		data["グリップ位置.backswing"] = round(sm['グリップ位置']['backswing']['metrics'], 2)
	if "グリップ位置.top" in columns:
		data["グリップ位置.top"] = round(sm['グリップ位置']['top']['metrics'], 2)
	if "グリップ位置.halfdown" in columns:
		data["グリップ位置.halfdown"] = round(sm['グリップ位置']['halfdown']['metrics'], 2)
	if "グリップ位置.impact" in columns:
		data["グリップ位置.impact"] = round(sm['グリップ位置']['impact']['metrics'], 2)
	if "グリップ位置.follow" in columns:
		data["グリップ位置.follow"] = round(sm['グリップ位置']['follow']['metrics'], 2)
	if "グリップ位置.finish" in columns:
		data["グリップ位置.finish"] = round(sm['グリップ位置']['finish']['metrics'], 2)
	if "手首軌道.address" in columns:
		data["手首軌道.address"] = round(sm['手首軌道']['address']['metrics'], 2)
	if "手首軌道.backswing" in columns:
		data["手首軌道.backswing"] = round(sm['手首軌道']['backswing']['metrics'], 2)
	if "手首軌道.top" in columns:
		data["手首軌道.top"] = round(sm['手首軌道']['top']['metrics'], 2)
	if "手首軌道.halfdown" in columns:
		data["手首軌道.halfdown"] = round(sm['手首軌道']['halfdown']['metrics'], 2)
	if "手首軌道.impact" in columns:
		data["手首軌道.impact"] = round(sm['手首軌道']['impact']['metrics'], 2)
	if "手首軌道.follow" in columns:
		data["手首軌道.follow"] = round(sm['手首軌道']['follow']['metrics'], 2)
	if "手首軌道.finish" in columns:
		data["手首軌道.finish"] = round(sm['手首軌道']['finish']['metrics'], 2)
	if "腰の開き.address" in columns:
		data["腰の開き.address"] = round(sm['腰の開き']['address']['metrics'], 2)
	if "腰の開き.backswing" in columns:
		data["腰の開き.backswing"] = round(sm['腰の開き']['backswing']['metrics'], 2)
	if "腰の開き.top" in columns:
		data["腰の開き.top"] = round(sm['腰の開き']['top']['metrics'], 2)
	if "腰の開き.halfdown" in columns:
		data["腰の開き.halfdown"] = round(sm['腰の開き']['halfdown']['metrics'], 2)
	if "腰の開き.impact" in columns:
		data["腰の開き.impact"] = round(sm['腰の開き']['impact']['metrics'], 2)
	if "腰の開き.follow" in columns:
		data["腰の開き.follow"] = round(sm['腰の開き']['follow']['metrics'], 2)
	if "腰の開き.finish" in columns:
		data["腰の開き.finish"] = round(sm['腰の開き']['finish']['metrics'], 2)
	if "肩の開き.address" in columns:
		data["肩の開き.address"] = round(sm['肩の開き']['address']['metrics'], 2)
	if "肩の開き.backswing" in columns:
		data["肩の開き.backswing"] = round(sm['肩の開き']['backswing']['metrics'], 2)
	if "肩の開き.top" in columns:
		data["肩の開き.top"] = round(sm['肩の開き']['top']['metrics'], 2)
	if "肩の開き.halfdown" in columns:
		data["肩の開き.halfdown"] = round(sm['肩の開き']['halfdown']['metrics'], 2)
	if "肩の開き.impact" in columns:
		data["肩の開き.impact"] = round(sm['肩の開き']['impact']['metrics'], 2)
	if "肩の開き.follow" in columns:
		data["肩の開き.follow"] = round(sm['肩の開き']['follow']['metrics'], 2)
	if "肩の開き.finish" in columns:
		data["肩の開き.finish"] = round(sm['肩の開き']['finish']['metrics'], 2)
	if "トータル" in columns:
		data["トータル"] = prizm['DataList'][0]['Value']
	if "トータルブレ" in columns:
		data["トータルブレ"] = prizm['DataList'][1]['Value']
	if "キャリー" in columns:
		data["キャリー"] = prizm['DataList'][2]['Value']
	if "キャリーブレ" in columns:
		data["キャリーブレ"] = prizm['DataList'][3]['Value']
	if "ヘッドスピード" in columns:
		data["ヘッドスピード"] = prizm['DataList'][4]['Value']
	if "ボール初速" in columns:
		data["ボール初速"] = prizm['DataList'][5]['Value']
	if "ミート率" in columns:
		data["ミート率"] = prizm['DataList'][6]['Value']
	if "打ち出し角 上下" in columns:
		data["打ち出し角 上下"] = prizm['DataList'][7]['Value']
	if "打ち出し角 左右" in columns:
		data["打ち出し角 左右"] = prizm['DataList'][8]['Value']
	if "バックスピン" in columns:
		data["バックスピン"] = prizm['DataList'][9]['Value']
	if "サイドスピン" in columns:
		data["サイドスピン"] = prizm['DataList'][10]['Value']
	if "ブロー角" in columns:
		data["ブロー角"] = prizm['DataList'][11]['Value']
	if "ヘッド軌道" in columns:
		data["ヘッド軌道"] = prizm['DataList'][12]['Value']
	if "フェイス角" in columns:
		data["フェイス角"] = prizm['DataList'][13]['Value']

	return data


def shots(aig, query, skip, limit, sort, columns):
	if aig is not None:
		shots = aig.shots
		accounts = aig.accounts
		if accounts is not None:
			df = []
			shots_cursor = shots.find(query).skip(skip).limit(limit).sort(sort, -1)
			for shot in shots_cursor:
				df.append(shotdata(columns, shot, accounts))
			return df, columns
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")


def generate_shots(aig, query, skip, limit, sort, columns):
	if aig is not None:
		shots = aig.shots
		accounts = aig.accounts
		if accounts is not None:
			shots_cursor = shots.find(query).skip(skip).limit(limit).sort(sort, -1)
			for shot in shots_cursor:
				yield (shotdata(columns, shot, accounts))
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")


'''
"name","username","club","score","postureScore","ballisticScore","studio","sites",
"前傾角度.address","前傾角度.backswing","前傾角度.top","前傾角度.halfdown","前傾角度.impact","前傾角度.follow","前傾角度.finish",
"背骨の傾き.address","背骨の傾き.backswing","背骨の傾き.top","背骨の傾き.halfdown","背骨の傾き.impact","背骨の傾き.follow","背骨の傾き.finish",
"首元の動き.address","首元の動き.backswing","首元の動き.top","首元の動き.halfdown","首元の動き.impact","首元の動き.follow","首元の動き.finish",
"右腰の動き.address","右腰の動き.backswing","右腰の動き.top","右腰の動き.halfdown","右腰の動き.impact","右腰の動き.follow","右腰の動き.finish",
"左腰の動き.address","左腰の動き.backswing","左腰の動き.top","左腰の動き.halfdown","左腰の動き.impact","左腰の動き.follow","左腰の動き.finish",
"重心の動き_正面.address","重心の動き_正面.backswing","重心の動き_正面.top","重心の動き_正面.halfdown","重心の動き_正面.impact","重心の動き_正面.follow","重心の動き_正面.finish",
"右膝の角度.address","右膝の角度.backswing","右膝の角度.top","右膝の角度.halfdown","右膝の角度.impact","右膝の角度.follow","右膝の角度.finish",
"手元の浮き.address","手元の浮き.backswing","手元の浮き.top","手元の浮き.halfdown","手元の浮き.impact","手元の浮き.follow","手元の浮き.finish",
"左膝の角度.address","左膝の角度.backswing","左膝の角度.top","左膝の角度.halfdown","左膝の角度.impact","左膝の角度.follow","左膝の角度.finish",
"頭の動き.address","頭の動き.backswing","頭の動き.top","頭の動き.halfdown","頭の動き.impact","頭の動き.follow","頭の動き.finish",
"両肩の傾き_正面.address","両肩の傾き_正面.backswing","両肩の傾き_正面.top","両肩の傾き_正面.halfdown","両肩の傾き_正面.impact","両肩の傾き_正面.follow","両肩の傾き_正面.finish",
"重心の動き_後方.address","重心の動き_後方.backswing","重心の動き_後方.top","重心の動き_後方.halfdown","重心の動き_後方.impact","重心の動き_後方.follow","重心の動き_後方.finish",
"グリップ位置.address","グリップ位置.backswing","グリップ位置.top","グリップ位置.halfdown","グリップ位置.impact","グリップ位置.follow","グリップ位置.finish",
"手首軌道.address","手首軌道.backswing","手首軌道.top","手首軌道.halfdown","手首軌道.impact","手首軌道.follow","手首軌道.finish",
"腰の開き.address","腰の開き.backswing","腰の開き.top","腰の開き.halfdown","腰の開き.impact","腰の開き.follow","腰の開き.finish",
"肩の開き.address","肩の開き.backswing","肩の開き.top","肩の開き.halfdown","肩の開き.impact","肩の開き.follow","肩の開き.finish",
"トータル","トータルブレ","キャリー","キャリーブレ","ヘッドスピード","ボール初速","ミート率","打ち出し角 上下","打ち出し角 左右","バックスピン","サイドスピン","ブロー角","ヘッド軌道","フェイス角",
'''
