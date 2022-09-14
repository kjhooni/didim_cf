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

billing_api_server = "https://billingapi.apigw.ntruss.com"
getDemandCostList_api_url = "/billing/v1/cost/getDemandCostList"
getDemandCostList_api_url = (
    getDemandCostList_api_url
    + "?regionCode=KR&responseFormatType=json&startMonth={}&endMonth={}".format(
        yyyymm, yyyymm
    )
)

getProductDemandCostList_api_url = "/billing/v1/cost/getProductDemandCostList"
getProductDemandCostList_api_url = (
    getProductDemandCostList_api_url
    + "?regionCode=KR&startMonth={}&endMonth={}&responseFormatType=json".format(
        yyyymm, yyyymm
    )
)

mail_api_server = "https://mail.apigw.ntruss.com"
mail_api_url = "/api/v1/mails"
