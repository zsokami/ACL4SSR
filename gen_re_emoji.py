from pyperclip import copy


re_emoji = r'''
🇺🇸,USA?,美[国國]|华盛顿|波特兰|达拉斯|俄勒冈|凤凰城|菲尼克斯|费利蒙|弗里蒙特|硅谷|旧金山|拉斯维加斯|洛杉|圣何塞|圣荷西|圣塔?克拉拉|西雅图|芝加哥|哥伦布|纽约|阿什本,America|United[^a-z]*States|Washington|Portland|Dallas|Oregon|Phoenix|Fremont|Valley|Francisco|Vegas|Los[^a-z]*Angeles|San[^a-z]*Jose|Santa[^a-z]*Clara|Seattle|Chicago|Columbus|York|Ashburn
🇭🇰,HKG?|CMI|HGC|HKT|HKBN|WTT|PCCW,香港,Hong
🇯🇵,JPN?,日本|东京|大阪|名古屋|埼玉,Japan|Tokyo|Osaka|Nagoya|Saitama
🇸🇬,SGP?,新加坡|[狮獅]城,Singapore
🇹🇼,TWN?|CHT|HiNet,[台臺][湾灣]|新[北竹]|彰化,Taiwan
🇷🇺,RUS?,俄[国國]|俄[罗羅]斯|莫斯科|圣彼得堡|西伯利亚|伯力|哈巴罗夫斯克,Russia|Moscow|Petersburg|Siberia|Khabarovsk
🇬🇧,UK|GBR?,英[国國]|伦敦|加的夫,Kingdom|England|London|Cardiff
🇨🇦,CAN?,加拿大|[枫楓][叶葉]|多伦多|蒙特利尔|温哥华,Canada|Toronto|Montreal|Vancouver
🇫🇷,FRA?,法[国國]|巴黎|马赛,France|Paris|Marseille|Marselha
🇰🇵,KP|PRK,朝[鲜鮮],North[^a-z]*Korea
🇰🇷,KO?R,[韩韓][国國]|首尔|春川,Korea|Seoul|Chuncheon
🇩🇪,DEU?,德[国國]|法兰克福,Germany|Frankfurt
🇮🇳,IND?,印度|孟买|加尔各答|贾坎德|泰米尔纳德|海得拉巴,India|Mumbai|Kolkata|Jharkhand|Tamil|Hyderabad
🇮🇱,IL|ISR,以色列|耶路撒冷,Israel|Jerusalem|Yerushalayim
🇦🇺,AUS?,澳大利[亚亞]|澳洲|悉尼|墨尔本,Australia|Sydney|Melbourne
🇦🇪,AR?E|UAE,阿联酋|迪拜|阿布扎比,Emirates|Dubai|Dhabi
🇧🇦,BA|BIH,波黑|波[士斯]尼亚|[黑赫]塞哥维[纳那],Bosnia|Herzegovina
🇧🇷,BRA?,巴西|圣保罗|维涅杜,Brazil|Paulo|Vinhedo
🇲🇴,MO|MAC|CTM,澳[门門],Macao
🇿🇦,ZAF?,南非|约(翰内斯)?堡,Africa|Johannesburg
🇨🇭,CHE?,瑞士|苏黎世,Switzerland|Zurich
🇮🇪,IE|IRL,爱尔兰|都柏林,Ireland|Dublin
🇮🇩,IDN?,印尼|印度尼西亚|雅加达,Indonesia|Jakarta
🇬🇶,GN?Q,赤道几内亚,Equatorial[^a-z]*Guinea
🇫🇮,FIN?,芬兰|赫尔辛基,Finland|Helsinki
🇹🇭,THA?,泰国|曼谷,Thailand|Bangkok
🇲🇽,ME?X,墨西哥|克雷塔罗,Mexico|Queretaro
🇸🇪,SW?E,瑞典|斯德哥尔摩,Sweden|Stockholm
🇹🇷,TU?R,土耳其|伊斯坦布尔,Turkey|Istanbul
🇸🇦,SAU?,沙特|吉达,Arabia|J[eu]dda
🇱🇰,LKA?,斯里兰卡,Sri[^a-z]*Lanka
🇦🇹,AU?T,奥地利|维也纳,Austria|Vienna
🇴🇲,OMN?,阿曼|马斯喀特,Oman|Muscat
🇪🇸,ESP?,西班牙|马德里,Spain|Madrid
🇸🇮,SI|SVN,斯洛文尼亚,Slovenia
🇳🇱,NLD?,荷兰|阿姆斯特丹,Netherlands
🇪🇪,EE|EST,爱沙尼亚,Estonia
🇮🇹,ITA?,意大利|米兰,Italy|Milan
🇱🇺,LUX?,卢森堡,Luxembo?urg
🇵🇭,PHL?,菲律宾,Philippines
🇺🇦,UA|UKR,乌克兰,Ukraine
🇦🇿,AZE?,阿塞拜疆,Azerbaijan
🇰🇬,KGZ?,吉尔吉斯斯坦,Kyrgyzstan
🇰🇿,KA?Z,哈萨克斯坦,Kazakhstan
🇷🇸,RS|SRB,塞尔维亚,Serbia
🇺🇿,UZB?,乌兹别克斯坦,Uzbekistan
🇦🇷,ARG?,阿根廷,Argentina
🇲🇰,MKD?,前南斯拉夫|马其顿,Macedonia
🇸🇰,SV?K,斯洛伐克,Slovensko
🇻🇪,VEN?,委内瑞拉,Venezuela
🇬🇱,GR?L,格陵兰,Greenland
🇵🇸,PSE?,巴勒斯坦,Palestine
🇧🇬,BGR?,保加利亚,Bulgaria
🇨🇴,COL?,哥伦比亚,Colombia
🇬🇮,GIB?,直布罗陀,Gibraltar
🇬🇹,GTM?,危地马拉,Guatemala
🇦🇶,AQ|ATA,南极,Antarctica
🇲🇪,MN?E,黑山,Montenegro
🇿🇼,ZWE?,津巴布韦,Zimbabwe
🇰🇭,KHM?,柬埔寨,Cambodia
🇱🇹,LTU?,立陶宛,Lietuvos
🇲🇳,MNG?,蒙古,Mongolia
🇲🇾,MYS?,马来,Malaysia
🇵🇰,PA?K,巴基斯坦,Pakistan
🇵🇹,PR?T,葡萄牙,Portugal
🇸🇴,SOM?,索马里,Somalia
🇩🇰,DN?K,丹麦,Denmark
🇮🇸,ISL?,冰岛,Iceland
🇦🇱,ALB?,阿尔巴尼亚,Albania
🇧🇪,BEL?,比利时,Belgium
🇬🇪,GEO?,格鲁吉亚,Georgia
🇭🇷,HRV?,克罗地亚,Croatia
🇭🇺,HUN?,匈牙利,Hungary
🇲🇩,MDA?,摩尔多瓦,Moldova
🇳🇬,NGA?,尼日利亚,Nigeria
🇳🇿,NZL?,新西兰,Zealand
🇷🇴,ROU?,罗马[尼利]亚,Romania
🇧🇧,BR?B,巴巴多斯,Barbados
🇹🇳,TU?N,突尼斯,Tunisia
🇺🇾,UR?Y,乌拉圭,Uruguay
🇻🇳,VNM?,越南,Vietnam
🇪🇨,ECU?,厄瓜多尔,Ecuador
🇲🇦,MAR?,摩洛哥,Morocco
🇦🇲,AR?M,亚美尼亚,Armenia
🇲🇲,MMR?,缅甸,Myanmar
🇵🇱,PO?L,波兰,Poland
🇨🇾,CYP?,塞浦路斯,Cyprus
🇪🇺,EUE?,欧洲,Europe
🇬🇷,GRC?,希腊,Greece
🇯🇴,JOR?,约旦,Jordan
🇱🇻,LVA?,拉脱维亚,Latvia
🇳🇴,NOR?,挪威,Norway
🇵🇦,PAN?,巴拿马,Panama
🇵🇷,PRI?,波多黎各,Puerto
🇧🇩,BG?D,孟加拉,Bengal
🇧🇳,BR?N,[文汶]莱,Brunei
🇧🇿,BL?Z,伯利兹,Belize
🇧🇹,BTN?,不丹,Bhutan
🇨🇱,CH?L,智利,Chile
🇨🇷,CRI?,哥斯达黎加,Costa
🇨🇿,CZE?,捷克,Czech
🇪🇬,EGY?,埃及,Egypt
🇰🇪,KEN?,肯尼亚,Kenya
🇳🇵,NPL?,尼泊尔,Nepal
🇮🇲,IMN?,马恩岛|曼岛,Mann
🇻🇦,VAT?,梵蒂冈,Vatican
🇮🇷,IRN?,伊朗,Iran
🇵🇪,PER?,秘鲁,Peru
🇱🇦,LAO?,老挝|寮国,Lao
🇷🇼,RWA?,卢旺达,Rwanda
🇹🇱,TLS?,东帝汶,Timor
🇦🇴,AG?O,安哥拉,Angola
🇶🇦,QAT?,卡塔尔,Qatar
🇱🇾,LB?Y,利比亚,Libya
🇧🇭,BHR?,巴林,Bahrain
🇫🇯,FJI?,斐济,Fiji
'''.splitlines()

re_emoji = [line.split(',') for line in map(str.strip, re_emoji) if line]

for i, (emoji, code, zh, en) in enumerate(re_emoji):
    prefix = rf"emoji=^(?!.*{'(?!🇨🇳)' if emoji in ('🇭🇰', '🇹🇼', '🇲🇴') else ''}[🇦-🇿]{{2}}).*"
    rest = re_emoji[i + 1:]
    zh2 = rf"({zh}),"
    if rest:
        code_rest, zh_rest, en_rest = ('|'.join(rest) for rest in zip(*(x[1:] for x in rest)))
        zh = rf"({zh})(?!中[轉转])(?!.*({zh_rest})(?!中[轉转])),"
        en = rf"(?i:((?<![\da-z.])({code})(?!\d*[a-z])|{en})(?!.*((?<![\da-z.])({code_rest})(?!\d*[a-z])|{en_rest}))),"
    else:
        zh = rf"({zh})(?!中[轉转]),"
        en = rf"(?i:((?<![\da-z.])({code})(?!\d*[a-z])|{en})),"
    re_emoji[i] = [prefix + x + emoji for x in (zh, zh2, en)]

copy('\n'.join(line for lines in zip(*re_emoji) for line in lines))
print('Copied')
