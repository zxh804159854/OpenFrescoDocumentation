# ErrorSimUndershoot 实验信号滤波器
此命令用于构造误差模拟欠调实验信号滤波器对象。

## 命令
```tcl
expSignalFilter ErrorSimUndershoot $tag $error
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一实验信号滤波器标签 |
| $error | 欠调误差 |

滤波器输出端口的信号计算如下：
if (signal_{i+1} > signal_i)
$$\operatorname {signal}_{i + 1} = \operatorname {signal}_{i + 1} - \operatorname {error}$$
elseif (signal_{i+1} < signal_i)
$$\operatorname {signal}_{i + 1} = \operatorname {signal}_{i + 1} + \operatorname {error}$$
else
$$signal_{i + 1} = signal_{i + 1}$$

## 示例
```tcl
#Define experimental signal filter   
expSignalFilter ErrorSimUndershoot 1 0.167 
```

此示例使用误差 0.167。