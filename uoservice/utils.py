def get_serial_by_name(item_dict, name):
  keys = list(item_dict.keys())
  for k, v in item_dict.items():
    if name in v[0]:
      return k, keys.index(k)

  return None, None


def isVendor(title):
  vendor_name_list = ['healer', 'armourer', 'banker']
  title_split = title.split(" ")
  for vendor_name in vendor_name_list:
    if vendor_name in title_split:
      index = title_split.index(vendor_name)
      return title_split[index]

  return None