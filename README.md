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
