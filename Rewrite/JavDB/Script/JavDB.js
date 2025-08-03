var body = $response.body;
var braum = JSON.parse(body);

const ada = '/ads';
const adb = '/startup';

//横幅广告
if ($request.url.indexOf(ada) != -1){
  braum.data.ads = {};
}

//公告，开屏
if ($request.url.indexOf(adb) != -1){
  braum.data.splash_ad.enabled = false;
  braum.data.splash_ad.overtime = 0;
  braum.data.splash_ad.ad = {};
  braum.data.feedback.placeholder = "";
  braum.data.settings.UPDATE_DESCRIPTION = "";
  braum.data.settings.NOTICE = "";
}

$done({body : JSON.stringify(braum)});
