# OpenFresco其他命令
其他OpenFresco专有的命令。源代码位置SRC/interpreter/tcl/TclWrapper.cpp

* wipeExp  
* removeExp
* version
* recordExp


## wipeExp 

此命令用于销毁所有已创建的实验对象。此命令用于重新开始建模，无需退出并重启解释器。

退出解释器命令一般如下
``` tcl
wipeExp
wipe
exit
```

## removeExp

删除某个OpenFresco对象

如
```tcl
loadConst -time 0.0
remove recorders
removeExp recorders
```

## version
返回OpenFresco版本号

## recordExp
开始实验记录


## OpenFresco专有命令汇总
expControlPoint
expSignalFilter
expControl
expSetup
expSite
setSizeExpSite
expTangentStiff
expElement
expRecorder
recordExp
startLabServer
startLabServerInteractive
setupLabServer
stepLabServer
stopLabServer
startSimAppSiteServer
startSimAppElemServer
wipeExp
removeExp
version