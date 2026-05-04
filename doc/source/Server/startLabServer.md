# startLabServer 命令
此命令用于启动实验室服务器进程。运行分布式测试时启动实验室（或后端）服务器，如图 1b 所示。

## 命令
```tcl
startLabServer $siteTag
```

| 参数 | 说明 |
|:----|:-----|
| $siteTag | 先前定义的实验站点对象的标签 |

## 示例
```tcl
# Define experimental site
# ___________
# expSite ActorSite $tag -setup $setupTag $ipPort <$dataSize>
expSite ActorSite 1 -setup 1 8091
# ___________
# Start the server process
# ___________
# startLabServer $siteTag
startLabServer 1 
```

此示例使用 ActorSite 启动服务器。