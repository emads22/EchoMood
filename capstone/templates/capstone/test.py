from internetarchive import get_item, search_items



search = search_items('crazy in love-beyonce')
print(type(search), search.num_found, search)
for result in search:
    print(result['identifier'])
    break


# item = get_item('LoseYourselfClean')

# for k,v in item.metadata.items():
#     print(print(k,":",v))