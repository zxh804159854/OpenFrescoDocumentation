# Actor 实验站点
此命令用于构造 ActorSite 实验站点对象。Actor 实验站点与远程实验站点通信，并在服务器程序上运行。此对象可以使用已定义的实验装置或实验控制来定义。

## 命令
与已定义的实验装置一起使用（换句话说，装置在服务器端）：
```tcl
expSite ActorSite $tag -setup $setupTag $ipPort <-ssl>
```

与已定义的实验控制一起使用（换句话说，装置在客户端）：
```tcl
expSite ActorSite $tag -control $ctrlTag $ipPort <-ssl>
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一实验站点标签 |
| $setupTag | 如果装置在服务器端，则为先前定义的装置对象的标签 |
| $ipPort | ActorSite 的 IP 端口号 |
| -ssl | 使用 OpenSSL 进行安全事务（可选） |
| $ctrlTag | 如果装置在客户端，则为先前定义的控制对象的标签 |

## 示例
```tcl
# Define experimental setup
# expSetup OneActuator $tag <-control $ctrlTag> $dir <-trialDispFact $f>
expSetup OneActuator 1 -control 2 1  

# Define experimental site
expSite ActorSite 1 -setup 1 8090 
```

此示例使用先前定义的 OneActuator 实验装置和 IP 端口 8090。实验装置在服务器端定义。