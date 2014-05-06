sql_insert_role = "INSERT INTO role(date, user_name, role_name, primary_key, paid_type, master_name, password, \
    group_key, guild_name, last_date, create_date, sex, x, y, gold_money, light, dark, in_power, out_power, \
    life, adaptive, revival, immunity, virtue, current_in_power, current_out_power, current_life, \
    current_health, current_satiety, current_poisoning, current_head_seek, current_arm_seek, current_leg_seek) VALUES ( \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

sql_insert_wear_item = "INSERT INTO wear_item(date,owner,`index`,item_id,item_name,count,color,durability,durabilityMax,smithingLevel,\
    attach,lockState,lockTime,dateTime,boident,startLevel,bBlueprint,specialExp,createName, \
    dummy1,dummy2,dummy3,dummy4,setting1,setting2,setting3,setting4) VALUES ( \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

sql_insert_bag_item = "INSERT INTO bag_item(date,owner,`index`,item_id,item_name,count,color,durability,durabilityMax,smithingLevel,\
    attach,lockState,lockTime,dateTime,boident,startLevel,bBlueprint,specialExp,createName, \
    dummy1,dummy2,dummy3,dummy4,setting1,setting2,setting3,setting4) VALUES ( \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

sql_insert_base_magic = "INSERT INTO base_magic(date,owner,`index`,name,exp) VALUES (%s, %s, %s, %s, %s)"
sql_insert_advanced_magic = "INSERT INTO base_magic(date,owner,`index`,name,exp) VALUES (%s, %s, %s,%s, %s)"
sql_insert_game_account = "INSERT INTO game_account VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"