## ACL4SSR_Online_Full_Mannix.ini

自定义 Clash 配置模板 https://dd.al/config

可作为 订阅转换 配置转换 规则转换 的远程配置

修改自 https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.ini

---

使用 mannix 的订阅转换反代（自动去除无节点的分组，项目地址：<https://github.com/zsokami/subcvt-mannix>）：

`https://sc-mannix.netlify.app?url={原订阅链接}`

短链：`https://dd.al/scm?url={原订阅链接}`

---

## ACL4SSR_Online_Mannix.ini

去除国家/地区 https://dd.al/config-nc

dler 订阅转换短链：`https://dd.al/dler-nc?url={原订阅链接}`

---

### V2

自带旗帜 emoji 添加逻辑，原名不包含旗帜 emoji 才添加，原名已包含旗帜 emoji 则不添加

**需去除订阅转换链接中的参数 `emoji=true/false` 才能生效**，参考例子：

`https://api.dler.io/sub?target=clash&udp=true&scv=true&config=https://dd.al/config&url={原订阅链接}`

短链：`https://dd.al/dler?url={原订阅链接}`

---

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
- 🤖 ‍OpenAI

url-test
- 延迟测试链接 http://www.gstatic.com/generate_204 -> https://i.ytimg.com/generate_204
- 间隔时间 300秒 -> 30秒
- 容差 50毫秒

📺 ‍B站 默认选择 🇨🇳 ‍中国

正则匹配大小写、简繁体，更好的匹配中转、IPLC节点

LocalAreaNetwork.list 使用 DIRECT
