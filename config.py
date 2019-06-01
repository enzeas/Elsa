import cookie_parser


cookie_file = 'cookie.cfg'
cookies = cookie_parser.Cookie(open(cookie_file).read()).cookie()

SLEEP_TIME = 0.4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
ALLOWED_DOMAINS = ['www.zhihu.com']
