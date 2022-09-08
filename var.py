import datetime, time


space = " "
new_line = "\n"
date = datetime.date.today()
yyyymm = date.strftime("%Y%m")
mm = date.month

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

apicall_method_get = "GET"
apicall_method_post = "POST"


getproductde = "getProductDemandCostListResponse"
productde = "productDemandCostList"
uA = "useAmount"
