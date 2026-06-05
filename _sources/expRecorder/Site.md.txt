# Site 记录器
此命令用于构造实验站点记录器对象。它用于记录实验站点中的数据，例如试和输出响应量。

## 命令
```tcl
expRecorder Site <-file $fileName> <-csv $fileName> <-xml $fileName> <-binary $fileName> <-database $tableName> <-time> <-dt> <-site $siteTag ...> <-siteRange $startTag $endTag> <-site all> respType
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
| $siteTag | 要记录的实验站点的标签 |
| $startTag, $endTag | 要记录的实验站点范围的起始和结束标签 |
| all | 记录所有实验站点对象（注意：此选项仅建议用于 xml 文件输出，因为 OpenFresco 可能会更改实验站点对象的顺序） |
| respType | 定义要记录的响应类型。可能的参数如下所述。 |

创建 ExpSiteRecorder 对象时，对实验站点的有效查询为：
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

## 示例
```tcl
# Define experimental site
# expSite LocalSite $tag $setupTag
expSite LocalSite 1 1
expSite LocalSite 2 2
...

# Start of recorder generation

expRecorder Site -file Site_trialDsp.out -time -site 1 2 trialDisp
expRecorder Site -file Site_trialVel.out -time -site 1 2 trialVel
expRecorder Site -file Site_trialAcc.out -time -site 1 2 trialAccel
expRecorder Site -file Site_trialTme.out -time -site 1 2 trialTime
expRecorder Site -file Site_outDsp.out -time -site 1 2 outDisp
expRecorder Site -file Site_outVel.out -time -site 1 2 outVel
expRecorder Site -file Site_outAcc.out -time -site 1 2 outAccel
expRecorder Site -file Site_outFrc.out -time -site 1 2 outForce
expRecorder Site -file Site_outTme.out -time -site 1 2 outTime

# End of recorder generation

```

此示例创建以无标题的 ASCII 格式将数据写入文件的实验站点记录器。记录先前创建的实验站点（标签为 1 和 2）的试位移、速度、加速度和时间以及输出位移、速度、加速度、力和时间。