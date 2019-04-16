# read_book API protocol

All responses use the format below:

```json
{
	'err_code': <int, 0 means success, otherwise fail>,
	'message': <str, human-readable message replied from the server>,
	'data': <data, this part is different from api to api>
}
```

## Account

Apis related to user account.

### GET/accoutn_api/code2session
Get openId and session_key from wechat server with code got from app_front.

#### request
'code': <str,code from wx.login()>

#### response

```json
{
    'sessionId':<str, local userId>
}
```
### POST/account_api/update_user
Update local userInfo

#### request
```json
{
    'sessionId': <str, local userId>,
    'avatarUrl': <str>,
    'nickName': <str>,
    'city': <str>,
    'provience': <str>,
    'country': <str>,
    'gender': <int, 0 for unknown, 1 for male, 2 for female>
}
```
#### response
no data

### POST/account_api/check_with_session_key
check local session_key
```json
{
    'sessionId': <str, local userId>,
    'rawData': <str, string of userInfo>,
    'signature': <str, hash value of rawDate and valid session_key>
}
```

#### response
```json
{
    'valid_user': <True of False>
}
```





