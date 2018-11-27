import cookie_parser


cookie_file = 'cookie.cfg'
cookies = cookie_parser.Cookie(open(cookie_file).read()).cookie()

data_path = '/data/enzedeng/zhihu_data'
