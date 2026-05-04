# ErrorSimRandomGauss 实验信号滤波器
此命令用于构造误差模拟随机高斯实验信号滤波器对象。使用 Box-Muller 方法生成高斯白噪声。均匀偏差由基于 Numerical Recipes in C++ 第 2 版中 NR::ran3 的特殊函数生成。

```tcl
expSignalFilter ErrorSimRandomGauss $tag $avg $std
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一实验信号滤波器标签 |
| $avg | 误差平均值 |
| $std | 误差标准差 |

滤波器输出端口的信号计算如下：
signal = signal + error(avg, std)

## 示例
```tcl
#Define experimental signal filter  
 
expSignalFilter ErrorSimRandomGauss 1 0.0 0.015 
```

此示例使用平均值 0.0 和标准差 0.015。

## 参考
Press, William H., et al., "Numerical Recipes in C++: The Art of Scientific Computing", 2nd ed., Cambridge University Press, 2002.
