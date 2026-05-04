# Local 实验站点
此命令用于构造 LocalSite 实验站点对象。它用于运行不需要客户端-服务器通信的本地测试。

## 命令
```tcl
expSite LocalSite $tag $setupTag
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一实验站点标签 |
| $setupTag | 先前定义的装置对象的标签 |

## 示例
```tcl
# Define experimental setup
# _____________
# expSetup OneActuator $tag <-control $ctrlTag> $dir <-trialDispFact $f> ...
expSetup OneActuator 2 -control 2 1
# Define experimental site
# _____________
expSite LocalSite 2 2 
```

此示例使用先前定义的 OneActuator 实验装置运行本地测试。