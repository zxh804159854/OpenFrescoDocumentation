# Aggregator 实验装置
此命令用于构造 Aggregator 实验装置对象。Aggregator 实验装置对象将不同的实验装置组合成一个装置。

## 命令
```tcl
expSetup Aggregator $tag <-control $ctrlTag> -setup $setupTagi ... <-trialDispFact $f> <-trialVelFact $f> <-trialAccelFact $f> <-trialForceFact $f> <-trialTimeFact $f> <-outDispFact $f> <-outVelFact $f> <-outAccelFact $f> <-outForceFact $f> <-outTimeFact $f> 
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一装置标签 |
| $ctrlTag | 先前定义的控制对象的标签（可选） |
| $setupTag | 先前定义的装置对象的标签 |
| $f | 在变换之前应用于试（<-ctrl….Fact $f>）和采集（<-out….Fact $f>）数据的因子（可选，默认值 = 1.0） |

## 示例
```tcl
#Define experimental setup  
  
expSetup OneActuator 1 2  
expSetup TwoActuators 2 120 120 60  
expSetup Aggregator 3 -control 1 -setup 1 2 
```

上述 Aggregator 实验装置命令组合了先前定义的 OneActuator 装置和 TwoActuators 装置。在"-setup"字段中，OneActuator 装置列在第一位，TwoActuators 装置列在第二位。

有关 OneActuator 和 TwoActuators 装置的更多详细信息将在本节后面提供。