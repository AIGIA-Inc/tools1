import pandas as pd

stripe = pd.read_csv('stripe.csv')
fromAccount = pd.read_csv('from.csv')
relation = pd.read_csv('relation.csv')
toAccount = pd.read_csv('to.csv')
studio = pd.read_csv('studio.csv')

# 繰り返し処理
def Inc(key, total):
    if key in total:
        total[key] += 1
    else:
        total[key] = 1

#stripeの課金している人のメールアドレスからスタジオ名を取得、紐付け
def StudioList():
    result = {}
    for stripe_index in range(len(stripe)):
        stripe_username = stripe.at[stripe_index, 'Customer Email']
        for fromAccount_index in range(len(fromAccount)):
            fromAccount_username = fromAccount.at[fromAccount_index, 'username']
            if stripe_username == fromAccount_username:
                fromAccount_id = fromAccount.at[fromAccount_index, 'user_id']
                for relation_index in range(len(relation)):
                    target_fromAccount_id = relation.at[relation_index, 'from_id']
                    if fromAccount_id == target_fromAccount_id:
                        target_toAccount_id = relation.at[relation_index, 'to_id']
                        for toAccount_index in range(len(toAccount)):
                            toAccount_id = toAccount.at[toAccount_index, 'user_id']
                            if toAccount_id == target_toAccount_id:
                                toAccount_username = toAccount.at[toAccount_index, 'username']
                                for studio_index in range(len(studio)):  # スタジオ名と連携
                                    studio_name = studio.at[studio_index, 'username']
                                    if studio_name == toAccount_username:
                                        target = studio.at[studio_index, 'studio']
        result[stripe_username] = target


    return result


#スタジオごとの数をまとめる
def Unique(studio_total):
    studio_count = {}
    #print(studio_total)
    #print(studio_total.values())
    for studio in list(studio_total.values()): #valuesでキーの値のみ取得
        Inc(studio, studio_count)
    print(studio_count)
    return studio_count


#studioとcountのリスト化
def Transpose(studio_count):
    studio_array = {}
    studio_array["studio"] = list(studio_count.keys())
    studio_array["count"] = list(studio_count.values())
    return studio_array

# ......
#print(StudioList())
studio_total = StudioList()                 #.....
#print(studio_total)
studio_count = Unique(studio_total)         #.....
studio_array =Transpose(studio_count)

output = pd.DataFrame(data=studio_array)    #csvへ出力
output.to_csv("count2.csv")




