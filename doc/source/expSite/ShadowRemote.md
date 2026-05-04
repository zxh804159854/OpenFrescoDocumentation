# Shadow（或 Remote）实验站点
此命令用于构造 ShadowSite（或 RemoteSite）实验站点对象。Shadow（或远程）实验站点与 Actor 实验站点通信，并在客户端程序上运行。

## 命令
对于 Shadow 站点：
```tcl
expSite ShadowSite $tag <-setup $setupTag> ipAddr $ipPort <-dataSize $size>
```

对于 Remote 站点（此选项已过时，将在未来版本中删除，已经删除）：
```tcl
expSite RemoteSite $tag <-setup $setupTag> ipAddr $ipPort <-dataSize $size>
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一实验站点标签 |
| $setupTag | 先前定义的装置对象的标签（可选，如果装置在客户端则需要提供） |
| ipAddr | 相应 ActorSite 的 IP 地址 |
| $ipPort | 相应 ActorSite 的 IP 端口号 |
| -ssl | 使用 OpenSSL 进行安全事务（可选） |
| $size | 发送的数据大小（可选） |

## 示例
```tcl
#Define experimental site   
expSite ShadowSite 1 "169.229.203.152" 8090 
```

此示例使用 IP 地址 169.229.203.152 和端口号 8090。