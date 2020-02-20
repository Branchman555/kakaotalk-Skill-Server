const express = require('express');
const app = express();
const logger = require('morgan');
const bodyParser = require('body-parser');

const apiRouter = express.Router();

var a = 0;
var b = 1;
var c = 2;

app.use(logger('dev', {}));
app.use(bodyParser.json());
app.use('/api', apiRouter);

apiRouter.post('/lastTest', function(req, res) {
    console.log(req.body);
    var responseBody;
    var platforms = new Array();


    var items = new Array();
    var caroselcount = 0;
    var lastcount = 0;
    var platformcount = 0;

    //스킬서버에서는 채널 서버에서 온 리퀘스트를 가지고 어떤 리퀘스트냐에 따라서
    //메시지를 구분하고 그에 맞는 리스폰스를 내보낼 것입니다
    //그래서 구분하는 방법중에 저는 전달되는 각 블록의 파라미터를 가지고 분류하기로 했어요



    //채널에 "배송"이라고 쳤을때 전달되는 파라미터
    if (req.body.action.params.testPara == "godel") {
        responseBody = {
            version: "2.0",
            template: {
                outputs: [{
                    "basicCard": {
                        "title": "보물상자",
                        "description": "보물상자 안에는 뭐가 있을까",
                        "buttons": [{
                                "action": "block",
                                "label": "배송하기",
                                "messageText": "배송하기를 누르셨습니다",
                                "blockId": "5e4d51a88192ac000136c558"
                            },
                            {
                                "action": "message",
                                "label": "취소하기",
                                "messageText": "취소하기"
                            }
                        ]
                    }
                }]
            },
            data: {
                temp1: "no"
            }
        };

        //배송요청 버튼을 눌렀을때 연결되는 파라미터
    } else if (req.body.action.params.testPara == "StartPoint") {

        //데이터 베이스에서 플랫폼에 대한 정보를 받아와서 내용을 넣을 부분
        //현재는 데이터베이스에서 안가져오고 임의로 값을 넣었습니다.
        platforms.push("TIP");
        platforms.push("비즈니스센터");
        platforms.push("종합관");
        platforms.push("A동");
        platforms.push("C동");
        platforms.push("E동");
        platforms.push("P동");
        platforms.push("산융관");

        //카로셀로 여러개의 카드형 버튼을 만들겁니다.
        //안타깝게도 한개의 카드에 버튼이 세개밖에 안들어가서 이런 번거로운 작업을 만들었습니다.
        //잘 모르시겠다면 건너 뛰셔도 좋은 코드입니다

        caroselcount = parseInt(platforms.length / 3);
        lastcount = platforms.length % 3;

        for (var i = 0; i < caroselcount; i++) {
            items.push({
                "title": "GoTo1",
                "description": "출발지를 눌러주세요",
                "buttons": [{
                        "action": "block",
                        "label": platforms[i * 3],
                        "messageText": "짜잔! 우리가 찾던 보물입니다",
                        "blockId": "5e4d54b0b617ea000109330e",
                        "extra": i * 3
                    },
                    {
                        "action": "block",
                        "label": platforms[i * 3 + 1],
                        "messageText": "짜잔! 우리가 찾던 보물입니다",
                        "blockId": "5e4d54b0b617ea000109330e",
                        "extra": i * 3 + 1
                    },
                    {
                        "action": "block",
                        "label": platforms[i * 3 + 2],
                        "messageText": "짜잔! 우리가 찾던 보물입니다",
                        "blockId": "5e4d54b0b617ea000109330e",
                        "extra": i * 3 + 2
                    }
                ]
            });
        }
        if (lastcount != 0) {
            items.push({
                "title": "GoTo1",
                "description": "출발지를 눌러주세요",
                "buttons": []
            });
            for (var i = 0; i < lastcount; i++) {
                items[items.length - 1].buttons.push({
                    "action": "block",
                    "label": platforms[i + (caroselcount * 3)],
                    "messageText": "짜잔! 우리가 찾던 보물입니다",
                    "blockId": "5e4d54b0b617ea000109330e",
                    "extra": i + (caroselcount * 3)
                });
            }
        }

        //여기까지 카로셀에 동적으로 정해진 플랫폼을 배열하는 코드입니다
        //디버깅은 마쳐서 아마 오류가 날 가능성은 거의 없을것니다

        //다음으로 카로셀로 basicCard를 지정해주고
        //카로셀 형태로 어떤 객체가 들어갈건지 대입해줬습니다
        //현재 상황을 예로 들면 총 8개의 객체가 버튼으로 들어가야하니까
        //3/3/2/ 이렇게 나눠져서 세개의 카로셀 카드메시지가 입력됩니다.
        responseBody = {
            version: "2.0",
            template: {
                outputs: [{
                    "carousel": {
                        "type": "basicCard",
                        "items": items
                    }
                }]
            },
            data: {
                temp1: "no"
            }
        };
        //배송 출발지를 입력했을 경우 연결되는 파라미터입니다
    } else if (req.body.action.params.testPara == "EndPoint") {
        stpoint = req.body.action.clientExtra.bnum


        responseBody = {
            version: "2.0",
            template: {
                outputs: [{
                    simpleText: {
                        text: "hello I'm JJ"
                    }
                }]
            },
            data: {
                temp1: "no"
            }
        };
    }
    res.status(200).send(responseBody);
});

app.listen(3000, function() {
    console.log('Example skill server listening on port 3000!');
});