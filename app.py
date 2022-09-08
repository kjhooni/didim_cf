##app.py
import call_api, var
import pandas as pd
from tkinter import CENTER


def main():

    global totalUseAmount, to_html

    # -----------------------------------------------------------------getDemandCostList

    api_server = "https://billingapi.apigw.ntruss.com"
    api_url = "/billing/v1/cost/getDemandCostList"
    api_url = (
        api_url
        + "?regionCode=KR&responseFormatType=json&startMonth={}&endMonth={}".format(
            var.yyyymm, var.yyyymm
        )
    )
    res = call_api.func(var.apicall_method_get, api_server, api_url, 1)

    totalUseAmount = res["getDemandCostListResponse"]["demandCostList"][0][var.uA]
    totalUseAmount = format(totalUseAmount, ",d")

    # -----------------------------------------------------------------getProductDemandCostList

    api_server = "https://billingapi.apigw.ntruss.com"
    api_url = "/billing/v1/cost/getProductDemandCostList"
    api_url = (
        api_url
        + "?regionCode=KR&startMonth={}&endMonth={}&responseFormatType=json".format(
            var.yyyymm, var.yyyymm
        )
    )
    res = call_api.func(var.apicall_method_get, api_server, api_url, 1)

    totalRows = res[var.getproductde]["totalRows"]

    codeName = []
    useAmount = []

    for i in range(0, totalRows):
        if res[var.getproductde][var.productde][i][var.uA] == 0:
            continue
        else:
            codeName.append(
                res[var.getproductde][var.productde][i]["productDemandType"]["codeName"]
            )
            useAmount.append(res[var.getproductde][var.productde][i][var.uA])

    a = []

    for i in range(0, len(codeName)):
        line = []
        for j in range(2):
            line.append(0)
        a.append(line)

    for i in range(0, len(codeName)):
        a[i][0] = codeName[i]
        a[i][1] = format(useAmount[i], ",d")

    df = pd.DataFrame(a, columns=["서비스", "사용금액(원)"])

    to_html = df.to_html(index=False, col_space=[250, 50], justify=CENTER, border=2)
    # ---------------------------------------------------------------------------------------mailSend

    api_server = "https://mail.apigw.ntruss.com"
    api_url = "/api/v1/mails"
    body = {
        "senderAddress": "noreply@tcping.kr",
        "title": "[네이버클라우드] 운영센터 2팀 테스트 계정 사용내역 보고",
        "body": """
        <br>
        {}월1일부터 {}월{}일까지의 총 이용금액과 내역은 아래와 같습니다.
        <br>
        <br>
        - 총 이용금액: {}원
        <br>
        <br>
        - 이용내역
        <br>
        {}
        <br>
        ※ 서비스 비용이 0원일 경우 표기하지 않습니다.
        <br>
        ※ 총 이용금액이 전일 발송 금액보다 큰 차이가 날 경우 콘솔에서 상세 내역을 확인해 주세요.
        <br>
        &nbsp;&nbsp;&nbsp;<a href= "https://www.ncloud.com/nsa/didim365se2test">[SubAccount 로그인]</a>
        """.format(
            var.date.month,
            var.date.month,
            (var.date.day) - 1,
            totalUseAmount,
            to_html,
        ),
        "individual": False,
        "advertising": False,
        "recipients": [
            {"address": "kimjh@didim365.com", "type": "R"},
            # {"address": "choimp@didim365.com", "type": "R"},
            # {"address": "ohsic@didim365.com", "type": "R"},
            # {"address": "hwany@didim365.com", "type": "R"},
        ],
    }
    call_api.func(var.apicall_method_post, api_server, api_url, body)
    return {"payload": "true"}


main()
