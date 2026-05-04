# Setup 记录器
此命令用于构造实验装置记录器对象。它用于记录实验装置中的数据，例如试、输出、目标（控制）和测量（daq）响应量。

## 命令
```tcl
expRecorder Setup <-file $fileName> <-csv $fileName> <-xml $fileName> <-binary $fileName> <-database $tableName> <-time> <-dt> <-setup $setupTag $setupTag> <-setupRange $startTag $endTag> <-setup all> respType
```

| 参数 | 说明 |
|:----|:-----|
| -file | 以无标题的 ASCII 格式将数据记录到文件（可选：仅使用 -file、-csv、-xml、-binary、-database 之一） |
| -csv | 以无标题的 ASCII 逗号分隔格式将数据记录到文件（可选：仅使用 -file、-csv、-xml、-binary、-database 之一） |
| -xml | 以包含元数据的 ASCII 格式将数据记录到文件（可选：仅使用 -file、-csv、-xml、-binary、-database 之一） |
| -binary | 以二进制格式将数据记录到文件（可选：仅使用 -file、-csv、-xml、-binary、-database 之一） |
| -database | 将数据记录到数据库（可选：仅使用 -file、-csv、-xml、-binary、-database 之一） |
| $fileName | 存储结果的文件。文件的每一行包含实验测试提交状态的结果。 |
| $tableName | 存储结果的数据库表名。表的每一行包含实验测试提交状态的结果。 |
| -time | 将分析的时间或伪时间放在第一数据列中（可选） |
| -dt | 以不同于分析时间步长的时间增量记录数据（这应该是分析时间步长的倍数） |
| $setupTag | 要记录的实验装置的标签 |
| $startTag, $endTag | 要记录的实验装置范围的起始和结束标签 |
| all | 记录所有实验装置对象（注意：此选项仅建议用于 xml 文件输出，因为 OpenFresco 可能会更改实验装置对象的顺序） |
| respType | 定义要记录的响应类型。可能的参数如下所述。 |

创建 ExpSetupRecorder 对象时，对实验装置的有效查询为：
- 试位移：trialDisp、trialDisplacement、trialDisplacements   
- 试速度：trialVel、trialVelocity、trialVelocities   
- 试加速度：trialAccel、trialAcceleration、trialAccelerations   
- 试力：trialForce、trialForces   
- 试时间：trialTime、trialTimes   
- 输出位移：outDisp、outDisplacement、outDisplacements   
- 输出速度：outVel、outVelocity、outVelocities   
- 输出加速度：outAccel、outAcceleration、outAccelerations   
- 输出力：outForce、outForces   
- 输出时间：outTime、outTimes   
- 控制位移：ctrlDisp、ctrlDisplacement、ctrlDisplacements   
- 控制速度：ctrlVel、ctrlVelocity、ctrlVelocities   
- 控制加速度：ctrlAccel、ctrlAcceleration、ctrlAccelerations   
- 控制力：ctrlForce、ctrlForces   
- 控制时间：ctrlTime、ctrlTimes   
- daq 位移：daqDisp、daqDisplacement、daqDisplacements   
- daq 速度：daqVel、daqVelocity、daqVelocities   
- daq 加速度：daqAccel、daqAcceleration、daqAccelerations   
- daq 力：daqForce、daqForces   
- daq 时间：daqTime、daqTimes

## 示例
```tcl
# Define experimental setup
# expSetup OneActuator $tag <-control $ctrlTag> $dir -sizeTrialOut $t $o <-trialDispFact $f>
expSetup OneActuator 1 -control 1 1 -sizeTrialOut 1 1
expSetup OneActuator 2 -control 2 1 -sizeTrialOut 1 1
...

# Start of recorder generation

# expRecorder Setup -file Setup_trialDsp.out -time -setup 1 2 trialDisp
expRecorder Setup -file Setup_trialVel.out -time -setup 1 2 trialVel
expRecorder Setup -file Setup_trialAcc.out -time -setup 1 2 trialAccel
expRecorder Setup -file Setup_outDsp.out -time -setup 1 2 outDisp
expRecorder Setup -file Setup_outFrc.out -time -setup 1 2 outForce
expRecorder Setup -file Setup_ctrlDsp.out -time -setup 1 2 ctrlDisp
expRecorder Setup -file Setup_ctrlVel.out -time -setup 1 2 ctrlVel
expRecorder Setup -file Setup_ctrlAcc.out -time -setup 1 2 ctrlAccel
expRecorder Setup -file Setup_daqDsp.out -time -setup 1 2 daqDisp
expRecorder Setup -file Setup_daqFrc.out -time -setup 1 2 daqForce

# End of recorder generation 
```

此示例创建以无标题的 ASCII 格式将数据写入文件的实验装置记录器。记录先前创建的实验装置（标签为 1 和 2）的试位移、速度和加速度，输出位移和力，目标（控制）位移、速度和加速度以及测量（daq）位移和力。