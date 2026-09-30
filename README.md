🎉**便宜实惠 AI 网关（API 中转站）推荐：[尚猫中心](https://shangmaozhongxin22.dpdns.org/) (基于开源项目 [New API](https://github.com/QuantumNous/new-api))**

🎉船新项目：[ACL4SSR Mannix 订阅转换极速版](https://github.com/zsokami/cvt)

## ACL4SSR_Online_Full_Mannix.ini

自定义 订阅转换 配置转换 规则转换 的远程配置：

https://raw.githubusercontent.com/zsokami/ACL4SSR/main/ACL4SSR_Online_Full_Mannix.ini

修改自 https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.ini

远程配置短链：`https://mnnx.cc/config`

订阅转换短链（原订阅链接需 URL 编码）：

- `https://mnnx.cc/v1?url={原订阅链接}` (api.v1.mk)
- `https://mnnx.cc/2c?url={原订阅链接}` (api.2c.lol)
- `https://mnnx.cc/0z?url={原订阅链接}` (api-suc.0z.gs)
- `https://mnnx.cc/{自定义后端地址}?url={原订阅链接}`

订阅转换反代（自动去除无节点的分组等功能，项目地址：<https://github.com/zsokami/subcvt-mannix>）：

`https://sc.mnnx.cc/{原订阅链接}`

## ACL4SSR_Online_Mannix.ini

去除国家/地区：

https://raw.githubusercontent.com/zsokami/ACL4SSR/main/ACL4SSR_Online_Mannix.ini

远程配置短链：`https://min.mnnx.cc/config`

订阅转换短链（原订阅链接需 URL 编码）：

- `https://min.mnnx.cc/v1?url={原订阅链接}` (api.v1.mk)
- `https://min.mnnx.cc/2c?url={原订阅链接}` (api.2c.lol)
- `https://min.mnnx.cc/0z?url={原订阅链接}` (api-suc.0z.gs)
- `https://min.mnnx.cc/{自定义后端地址}?url={原订阅链接}`

## ACL4SSR_Online_(Full_)Mannix_No_DNS_Leak.ini

无 DNS 泄漏：

https://raw.githubusercontent.com/zsokami/ACL4SSR/main/ACL4SSR_Online_Full_Mannix_No_DNS_Leak.ini

- `https://ndl.mnnx.cc/config`
- `https://ndl.mnnx.cc/v1?url={原订阅链接}` (api.v1.mk)
- `https://ndl.mnnx.cc/2c?url={原订阅链接}` (api.2c.lol)
- `https://ndl.mnnx.cc/0z?url={原订阅链接}` (api-suc.0z.gs)
- `https://ndl.mnnx.cc/{自定义后端地址}?url={原订阅链接}`

https://raw.githubusercontent.com/zsokami/ACL4SSR/main/ACL4SSR_Online_Mannix_No_DNS_Leak.ini

- `https://minndl.mnnx.cc/config`
- `https://minndl.mnnx.cc/v1?url={原订阅链接}` (api.v1.mk)
- `https://minndl.mnnx.cc/2c?url={原订阅链接}` (api.2c.lol)
- `https://minndl.mnnx.cc/0z?url={原订阅链接}` (api-suc.0z.gs)
- `https://minndl.mnnx.cc/{自定义后端地址}?url={原订阅链接}`

和原配置只有一行差异：

```diff
- ruleset=🛩️ ‍墙内,[]GEOIP,CN
+ ruleset=🛩️ ‍墙内,[]GEOIP,CN,no-resolve
```

原配置不在已知名单中的（国内外）域名会先通过当地 DNS 服务器解析一次。

添加 no-resolve 后，不在已知名单中的（国内外）域名将直接✈️ 起飞。

---

### 性能优化 2

🎉船新项目：[ACL4SSR Mannix 订阅转换极速版](https://github.com/zsokami/cvt)

后端：`https://arx.cc/{原订阅链接}`

前端：<https://sub.com.mp>

### 性能优化 1

原版订阅转换后端使用本配置时，若节点过多，转换速度很慢。

建议使用性能优化后端（<https://github.com/zsokami/subconverter>，暂无公共服务）

该后端通过预编译和缓存正则，大幅提升转换速度。

---

### V3

添加某些影视/动漫 APP 广告拦截规则：

https://raw.githubusercontent.com/zsokami/ACL4SSR/main/BanProgramAD1.list

附 hosts 文件（自动更新）：

https://raw.githubusercontent.com/zsokami/ACL4SSR/main/hosts

---

### V2

自带旗帜 emoji 添加逻辑，原名不包含旗帜 emoji 才添加，原名已包含旗帜 emoji 则不添加

**需去除订阅转换链接中的参数 `emoji=true/false` 才能生效**，参考例子：

`https://api.dler.io/sub?target=clash&udp=true&scv=true&config=https://raw.githubusercontent.com/zsokami/ACL4SSR/main/ACL4SSR_Online_Full_Mannix.ini&url={原订阅链接}`

---

⚠ 重要！每个组名的**空格**后面都添加了一个**隐藏字符 \u200d** 用于防止与节点重名，改名需谨慎

移除
- 📢 谷歌FCM
- Ⓜ️ 微软云盘
- Ⓜ️ 微软服务
- 🍎 苹果服务
- 📲 电报消息
- 🎶 网易音乐
- 🎮 游戏平台
- 📹 油管视频
- 🎥 奈飞视频
- 🌏 国内媒体
- 🌍 国外媒体
- 📺 巴哈姆特
- 🇰🇷 韩国节点

重命名
- 🚀 节点选择 -> ✈️ 起飞
- 🚀 手动切换 -> 👆🏻 指定
- ♻️ 自动选择 -> ⚡ 低延迟
- 📺 哔哩哔哩 -> 📺 B站
- 🎯 全球直连 -> 🛩️ 墙内
- 🐟 漏网之鱼 -> 🌐 未知站点
- 🇭🇰 香港节点 -> 🇭🇰 香港
- 🇨🇳 台湾节点 -> 🇹🇼 台湾
- 🇸🇬 狮城节点 -> 🇸🇬 新加坡
- 🇯🇵 日本节点 -> 🇯🇵 日本
- 🇺🇲 美国节点 -> 🇺🇸 美国

合并
- 🛑 广告拦截 + 🍃 应用净化 -> 💩 广告

新增
- 🇨🇳 中国 (含 🇭🇰 香港 🇹🇼 台湾)
- 🎏 其他
- 🤖 ‍AI

url-test
- 延迟测试链接 http://www.gstatic.com/generate_204 -> https://i.ytimg.com/generate_204
- 间隔时间 300秒 -> 15/30秒
- 容差 50/150毫秒 -> 100/300毫秒

正则匹配大小写、简繁体，更好地匹配中转、IPLC节点

LocalAreaNetwork.list 使用 DIRECT

移除 Download.list


## 🌐 Web Resources & Aesthetic Symbols Index
- [SYM 1D419](https://anime-sparkle-text-61.pages.dev/symbol/sym-1d419/)
- [SYM 267E](https://sleek-bio-symbols-40.pages.dev/symbol/sym-267e/)
- [SYM 26AF](https://minimal-star-symbols-31.pages.dev/symbol/sym-26af/)
- [SYM 2635](https://clean-space-text-47.pages.dev/symbol/sym-2635/)
- [SYM 1F49B](https://minimal-star-symbols-26.pages.dev/symbol/sym-1f49b/)
- [SYM 1F602](https://vintage-lace-symbols-65.pages.dev/symbol/sym-1f602/)
- [SYM 1D436](https://zen-aesthetic-fonts-87.pages.dev/symbol/sym-1d436/)
- [WHITE SUN WITH RAYS](https://vampiric-text-craft-82.pages.dev/symbol/white-sun-with-rays/)
- [SYM 26B0](https://sleek-bio-symbols-40.pages.dev/symbol/sym-26b0/)
- [FLORAL BRANCH BOUQUET](https://gothic-bio-fonts-14.pages.dev/symbol/floral-branch-bouquet/)
- [SYM 26E0](https://neon-gamer-symbols-64.pages.dev/symbol/sym-26e0/)
- [SYM 1D48E](https://zen-unicode-hub-94.pages.dev/symbol/sym-1d48e/)
- [SYM 265E](https://chibi-emoticon-lab-65.pages.dev/symbol/sym-265e/)
- [SYM 2671](https://mecha-hacker-kaomoji-26.pages.dev/symbol/sym-2671/)
- [SYM 2660](https://kawaii-kaomoji-hub-12.pages.dev/symbol/sym-2660/)
- [SYM 1D40E](https://mecha-glitch-fonts-82.pages.dev/symbol/sym-1d40e/)
- [TIKTOK CAPTIONS](https://mecha-glitch-fonts-82.pages.dev/ja/tiktok-captions/)
- [KAOMOJI](https://sleek-bio-symbols-40.pages.dev/es/kaomoji/)
- [SYM 2636](https://dolly-angel-fonts-14.pages.dev/symbol/sym-2636/)
- [SYM 1F499](https://classic-literature-symbols-64.pages.dev/symbol/sym-1f499/)
- [SYM 1F619](https://minimal-star-symbols-22.pages.dev/symbol/sym-1f619/)
- [SYM 1D497](https://mecha-hacker-kaomoji-26.pages.dev/symbol/sym-1d497/)
- [WATER BUBBLES](https://soft-pastel-unicode-78.pages.dev/symbol/water-bubbles/)
- [SYM 1D404](https://zen-unicode-hub-94.pages.dev/symbol/sym-1d404/)
- [SYM 26D9](https://balletcore-unicode-67.pages.dev/symbol/sym-26d9/)
- [SYM 1D459](https://mecha-hacker-kaomoji-26.pages.dev/symbol/sym-1d459/)
- [SYM 2763 FE0F](https://minimal-star-symbols-87.pages.dev/symbol/sym-2763-fe0f/)
- [SYM 26AE](https://glitch-matrix-fonts-28.pages.dev/symbol/sym-26ae/)
- [SYM 2611](https://glitch-matrix-fonts-28.pages.dev/symbol/sym-2611/)
- [SYM 1F60D](https://coquette-aesthetic-symbols-84.pages.dev/symbol/sym-1f60d/)
- [SYM 26F2](https://occult-aesthetic-symbols-26.pages.dev/symbol/sym-26f2/)
- [ROBLOX NAMES](https://anime-sparkle-text-81.pages.dev/vi/roblox-names/)
- [SYM 1D46E](https://occult-aesthetic-symbols-26.pages.dev/symbol/sym-1d46e/)
- [SYM 1F625](https://anime-sparkle-text-45.pages.dev/symbol/sym-1f625/)
- [DISCORD STATUS](https://glitch-matrix-fonts-28.pages.dev/es/discord-status/)
- [SYM 1D442](https://occult-aesthetic-symbols-26.pages.dev/symbol/sym-1d442/)
- [SYM 1F92C](https://vintage-runes-text-63.pages.dev/symbol/sym-1f92c/)
- [EIGHT POINTED BLACK STAR](https://cyber-clan-tags-75.pages.dev/symbol/eight-pointed-black-star/)
- [SYM 1F495](https://minimal-star-symbols-87.pages.dev/symbol/sym-1f495/)
- [SYM 2640](https://mecha-glitch-fonts-82.pages.dev/symbol/sym-2640/)
- [SYM 2677](https://zen-unicode-hub-94.pages.dev/symbol/sym-2677/)
- [SYM 1F61D](https://chibi-emoticon-vault-78.pages.dev/symbol/sym-1f61d/)
- [ZODIAC CELESTIAL](https://pink-bow-fonts-37.pages.dev/vi/zodiac-celestial/)
- [SYM 1D42E](https://neon-matrix-symbols-74.pages.dev/symbol/sym-1d42e/)
- [SYM 1D439](https://occult-aesthetic-symbols-26.pages.dev/symbol/sym-1d439/)
- [SYM 1D45A](https://zen-arrow-symbols-99.pages.dev/symbol/sym-1d45a/)
- [SYM 26D2](https://baroque-aesthetic-symbols-59.pages.dev/symbol/sym-26d2/)
- [ROTATED HEART BULLET](https://mecha-glitch-fonts-82.pages.dev/symbol/rotated-heart-bullet/)
- [JA](https://mecha-glitch-fonts-82.pages.dev/ja/)
- [NATURE FLOWERS](https://minimal-star-symbols-28.pages.dev/es/nature-flowers/)
- [SYM 268D](https://manga-speech-symbols-95.pages.dev/symbol/sym-268d/)
- [TRENDING](https://vintage-runes-text-63.pages.dev/trending/)
- [SYM 26F7](https://anime-sparkle-text-50.pages.dev/symbol/sym-26f7/)
- [SYM 1D46C](https://zen-unicode-hub-94.pages.dev/symbol/sym-1d46c/)
- [SYM 1F626](https://mecha-glitch-fonts-82.pages.dev/symbol/sym-1f626/)
- [TRENDING](https://soft-pastel-unicode-78.pages.dev/trending/)
- [SYM 274B](https://minimal-star-symbols-87.pages.dev/symbol/sym-274b/)
- [HEARTS](https://mecha-glitch-fonts-82.pages.dev/es/hearts/)
- [SYM 26DB](https://coquette-heart-text-40.pages.dev/symbol/sym-26db/)
- [SYM 1F606](https://chibi-emoticon-vault-78.pages.dev/symbol/sym-1f606/)
- [SYM 1D46A](https://pastel-manga-symbols-57.pages.dev/symbol/sym-1d46a/)
- [SYM 1D496](https://mecha-hacker-kaomoji-26.pages.dev/symbol/sym-1d496/)
- [SYM 26AA](https://clean-aesthetic-arrows-99.pages.dev/symbol/sym-26aa/)
- [SYM 1F61B](https://manga-speech-symbols-95.pages.dev/symbol/sym-1f61b/)
- [SYM 1F925](https://moe-kaomoji-vault-94.pages.dev/symbol/sym-1f925/)
- [SYM 2687](https://pastel-manga-symbols-57.pages.dev/symbol/sym-2687/)
- [SYM 1F47F](https://soft-angel-symbols-61.pages.dev/symbol/sym-1f47f/)
- [SYM 26BB](https://zen-space-symbols-89.pages.dev/symbol/sym-26bb/)
- [SYM 2731](https://pastel-manga-symbols-57.pages.dev/symbol/sym-2731/)
- [SYM 1D441](https://soft-angel-unicode-43.pages.dev/symbol/sym-1d441/)
- [GAMING WEAPONS](https://vintage-runes-text-63.pages.dev/es/gaming-weapons/)
- [SYM 1D493](https://minimal-star-symbols-63.pages.dev/symbol/sym-1d493/)
- [SYM 262F](https://archival-rune-symbols-42.pages.dev/symbol/sym-262f/)
- [SYM 1D46C](https://angelic-bio-symbols-90.pages.dev/symbol/sym-1d46c/)
- [SYM 1F648](https://coquette-aesthetic-symbols-78.pages.dev/symbol/sym-1f648/)
- [SYM 1F47D](https://minimal-star-symbols-87.pages.dev/symbol/sym-1f47d/)
- [SYM 26DC](https://neon-glitch-fonts-20.pages.dev/symbol/sym-26dc/)
- [RIGHT BLACK LENTICULAR BRACKET](https://pastel-moe-kaomoji-91.pages.dev/symbol/right-black-lenticular-bracket/)
- [SYM 1F92F](https://minimal-star-symbols-28.pages.dev/symbol/sym-1f92f/)
- [DISCORD STATUS](https://manga-bubble-symbols-94.pages.dev/ru/discord-status/)
- [SYM 1F61F](https://mecha-glitch-fonts-82.pages.dev/symbol/sym-1f61f/)
- [SYM 1F643](https://anime-sparkle-text-70.pages.dev/symbol/sym-1f643/)
- [SYM 1F639](https://clean-aesthetic-arrows-99.pages.dev/symbol/sym-1f639/)
- [ANTICLOCKWISE OPEN CIRCLE ARROW](https://anime-sparkle-text-24.pages.dev/symbol/anticlockwise-open-circle-arrow/)
- [SYM 2741](https://zen-unicode-hub-94.pages.dev/symbol/sym-2741/)
- [SYM 26B2](https://coquette-aesthetic-symbols-78.pages.dev/symbol/sym-26b2/)
- [SYM 1D44F](https://neon-matrix-symbols-74.pages.dev/symbol/sym-1d44f/)
- [SYM 2676](https://scholar-rune-symbols-77.pages.dev/symbol/sym-2676/)
- [SAGITTARIUS ZODIAC ARCHER](https://chibi-emoticon-vault-78.pages.dev/symbol/sagittarius-zodiac-archer/)
- [SYM 26B7](https://chibi-emoticon-vault-78.pages.dev/symbol/sym-26b7/)
- [SYM 1D40E](https://soft-angel-unicode-43.pages.dev/symbol/sym-1d40e/)
- [SYM 1D463](https://anime-sparkle-text-58.pages.dev/symbol/sym-1d463/)
- [SYM 1D482](https://neon-matrix-symbols-74.pages.dev/symbol/sym-1d482/)
- [BRACKETS](https://vintage-runes-text-63.pages.dev/brackets/)
- [ZODIAC CELESTIAL](https://gothic-bio-fonts-61.pages.dev/pt/zodiac-celestial/)
- [AQUARIUS ZODIAC WATER BEARER](https://mecha-glitch-fonts-82.pages.dev/symbol/aquarius-zodiac-water-bearer/)
- [WHITE SUN WITH RAYS](https://gothic-bio-fonts-87.pages.dev/symbol/white-sun-with-rays/)
- [SYM 1D428](https://coquette-heart-text-40.pages.dev/symbol/sym-1d428/)
- [ES](https://gothic-bio-fonts-90.pages.dev/es/)
- [SYM 267E](https://chibi-emoticon-vault-78.pages.dev/symbol/sym-267e/)
- [SYM 1D43C](https://matrix-hacker-fonts-85.pages.dev/symbol/sym-1d43c/)
- [SCORPIO ZODIAC SCORPION](https://zen-unicode-hub-94.pages.dev/symbol/scorpio-zodiac-scorpion/)
- [SYM 1D48F](https://soft-pink-fonts-41.pages.dev/symbol/sym-1d48f/)
- [SYM 1F60E](https://minimal-star-symbols-89.pages.dev/symbol/sym-1f60e/)
- [SYM 26EF](https://coquette-aesthetic-symbols-84.pages.dev/symbol/sym-26ef/)
- [SYM 1F97A](https://clean-aesthetic-arrows-99.pages.dev/symbol/sym-1f97a/)
- [SYM 1D4A0](https://gothic-bio-fonts-98.pages.dev/symbol/sym-1d4a0/)
- [SYM 1FA75](https://cyber-clan-tags-65.pages.dev/symbol/sym-1fa75/)
- [SYM 1F47B](https://mecha-glitch-fonts-82.pages.dev/symbol/sym-1f47b/)
- [LEFT HEAVY BRACKET BOX](https://soft-ribbon-fonts-77.pages.dev/symbol/left-heavy-bracket-box/)
- [KHANDA EMBLEM](https://minimal-star-symbols-43.pages.dev/symbol/khanda-emblem/)
- [ZODIAC CELESTIAL](https://gothic-bio-fonts-90.pages.dev/zodiac-celestial/)
- [SYM 1D46B](https://neon-matrix-symbols-74.pages.dev/symbol/sym-1d46b/)
- [SYM 1F627](https://scholar-rune-symbols-77.pages.dev/symbol/sym-1f627/)
- [SYM 1D4A2](https://angelic-ribbon-text-78.pages.dev/symbol/sym-1d4a2/)
- [SYM 1F636](https://coquette-aesthetic-symbols-78.pages.dev/symbol/sym-1f636/)
- [SYM 1D481](https://kawaii-kaomoji-hub-31.pages.dev/symbol/sym-1d481/)
- [SYM 262A](https://baroque-font-vault-96.pages.dev/symbol/sym-262a/)
- [SYM 1F480](https://mecha-glitch-fonts-82.pages.dev/symbol/sym-1f480/)
- [NATURE FLOWERS](https://minimal-star-symbols-43.pages.dev/es/nature-flowers/)
- [SYM 2670](https://lace-and-ribbon-text-61.pages.dev/symbol/sym-2670/)
- [SWIMMING FISH RIGHT](https://pastel-manga-symbols-57.pages.dev/symbol/swimming-fish-right/)
- [SYM 26F8](https://neon-matrix-symbols-74.pages.dev/symbol/sym-26f8/)
- [SYM 26FE](https://neon-matrix-symbols-74.pages.dev/symbol/sym-26fe/)
- [LEFT POINTING DOUBLE ANGLE QUOTATION](https://kawaii-kaomoji-hub-97.pages.dev/symbol/left-pointing-double-angle-quotation/)
- [SYM 1D420](https://soft-angel-unicode-43.pages.dev/symbol/sym-1d420/)
- [LEFT WHITE CORNER BRACKET](https://zen-unicode-hub-94.pages.dev/symbol/left-white-corner-bracket/)
- [SYM 26B8](https://zen-unicode-text-36.pages.dev/symbol/sym-26b8/)
- [SYM 1F97A](https://anime-sparkle-text-24.pages.dev/symbol/sym-1f97a/)
- [SYM 2628](https://minimal-star-symbols-28.pages.dev/symbol/sym-2628/)
