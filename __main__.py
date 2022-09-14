##__main__.py
import call_api, var
import pip

def main(self):

    pip.main(["install", "pandas"])
    import pandas as pd
    from tkinter import CENTER

    ##################################################################   getDemandCostList

    res = call_api.func(
        var.apicall_method_get,
        var.billing_api_server,
        var.getDemandCostList_api_url,
        1,
    )

    totalUseAmount = res["getDemandCostListResponse"]["demandCostList"][0][var.uA]
    totalUseAmount = format(totalUseAmount, ",d")

    ##################################################################   getProductDemandCostList

    res = call_api.func(
        var.apicall_method_get,
        var.billing_api_server,
        var.getProductDemandCostList_api_url,
        1,
    )

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

    ##################################################################   mailSend

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
        "individual": True,
        "advertising": False,
        "recipients": [
            {"address": "hwany@didim365.com", "type": "R"},
            {"address": "hmjeon@didim365.com", "type": "R"},
            {"address": "jsbae@didim365.com", "type": "R"},
            {"address": "kimjh@didim365.com", "type": "R"},
            {"address": "choimp@didim365.com", "type": "R"},
            {"address": "ohsic@didim365.com", "type": "R"},
            {"address": "leehw@didim365.com", "type": "R"},
            {"address": "ygc@didim365.com", "type": "R"},
        ],
    }
    call_api.func(var.apicall_method_post, var.mail_api_server, var.mail_api_url, body)
    return {"payload": "true"}
