# startSimAppElemServer 命令

此命令用于启动模拟应用程序单元中间层服务器进程。当模拟应用程序或有限元软件使用通用客户端单元**genericlient**时，使用 startSimAppElemServer 命令，如图 1a 和 1b 所示。

```tcl
startSimAppElemServer $eleTag $port <-ssl>
```

| 参数 | 说明 |
|:----|:-----|
| $eleTag | 先前定义的实验单元对象的标签 |
| $port | 中间层服务器的 IP 端口号 |
| -ssl | 使用 OpenSSL 进行安全事务（可选） |

## 示例

**有限元软件**
```tcl
# expElement twoNodeLink $eleTag $iNode $jNode -dir $dirs -server $ipPort <ipAddr> <-ssl> <-udp> <-dataSize $size> -initStif $Kij <-orient <$x1 $x2 $x3> $y1 $y2 $y3> <-pDelta Mratios> <-iMod> <-mass $m>
expElement twoNodeLink 1 1 3 -dir 2 -server 8090 -initStif 2.8;  # use with SimAppSiteServer
```
**中间层**
```tcl
# Define experimental element
# 
# left column
expElement twoNodeLink 1 1 3 -dir 2 -site 1 -initStif 2.8 -orient 0 1 0 -1 0
# 
# Start the server process
# 
# startSimAppElemServer $eleTag $port
startSimAppElemServer 1 8090 
```

此示例使用 twoNodeLink 实验单元，中间层服务器的端口号为 8090。