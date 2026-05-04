# startSimAppSiteServer 命令
此命令用于启动模拟应用程序站点中间层服务器进程。当模拟应用程序或有限元软件使用其自己的实验单元时，使用 startSimAppSiteServer 命令，如图 6b 所示。

## 命令
```tcl
startSimAppSiteServer $siteTag $port <-ssl>
```

| 参数 | 说明 |
|:----|:-----|
| $siteTag | 先前定义的实验站点对象的标签 |
| $port | 中间层服务器的 IP 端口号 |
| -ssl | 使用 OpenSSL 进行安全事务（可选） |

## 示例

```tcl
# Define experimental site
# ___________
# expSite RemoteSite $tag <-setup $setupTag> $ipAddr $ipPort <$dataSize>
expSite RemoteSite 1 "127.0.0.1" 8091
# ___________
# Start the server process
# ___________
# startSimAppSiteServer $siteTag $port
#startSimAppSiteServer 1 8090 
```

此示例使用 RemoteSite，中间层服务器的端口号为 8090。