import datetime
import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 1
src_game = api.search(dt.Game, {"name": "balan wonderworld"})[0]

user_command = 'AGS'
cat_list = []
for category in src_game.categories:
    cat_list.append(category.name)

cat_index = cat_list.index(user_command)

anypercent_user = src_game.categories[cat_index].records[0].runs[0]["run"].players[0].names["international"]
anypercent_time = src_game.categories[cat_index].records[0].runs[0]["run"].times["primary_t"]

anypercent = [anypercent_user]#, str(datetime.timedelta(seconds=anypercent_time))]

print(anypercent)

#print(f'The {src_game.categories[cat_index].name} record is {anypercent[1]} by {anypercent[0]}')

# cat_list = []
# for category in src_game.categories:
#     cat_list.append(category.name)

# print(cat_list)