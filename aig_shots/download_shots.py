# -*- coding: utf-8 -*-

def shots(aig, columns):
	result: list = []
	if aig:
		shots = aig.shots
		accounts = aig.accounts
		if accounts:
			shots_cursor = shots.find({})
			for shot in shots_cursor:
				platform = shot['platform']
				sm = shot['sm']
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

				data = {}

				if "name" in columns:
					data["name"] = shot['name']
				if "username" in columns:
					data["username"] = platform['username']
				if "club" in columns:
					data["club"] = platform['description']['club']
				if "score" in columns:
					data["score"] = platform['description']['score']
				if "postureScore" in columns:
					data["postureScore"] = platform['description']['postureScore']
				if "ballisticScore" in columns:
					data["ballisticScore"] = platform['description']['ballisticScore']
				if "studio" in columns:
					data["studio"] = platform['description']['studio']
				if "sites" in columns:
					data["sites"] = platform['description']['sites']
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

				result.append(data)
		else:
			raise Exception("collection error")
	else:
		raise Exception("database error")
	return result
