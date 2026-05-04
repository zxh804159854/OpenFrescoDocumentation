# Control 记录器
此命令用于构造实验控制记录器对象。它用于记录实验控制中的数据，例如控制（目标）和 daq（测量）响应量。

## 命令
```tcl
expRecorder Control <-file $fileName> <-csv $fileName> <-xml $fileName> <-binary $fileName> <-database $tableName> <-time> <-dt> <-control $ctrlTag $ctrlTag > <-controlRange $startTag $endTag> <-control all> respType
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
| $ctrlTag | 要记录的实验控制的标签 |
| $startTag, $endTag | 要记录的实验控制范围的起始和结束标签 |
| all | 记录所有实验控制对象（注意：此选项仅建议用于 xml 文件输出，因为 OpenFresco 可能会更改实验控制对象的顺序） |
| respType | 定义要记录的响应类型。由于这取决于实验控制的类型，可能的参数在控制命令中描述。 |

## 示例
```tcl
# Define experimental control
# expControl SimUniaxialMaterials $tag $matTags
expControl SimUniaxialMaterials 1 1
expControl SimUniaxialMaterials 2 2

# Start of recorder generation

expRecorder Control -file Control_ctrlDsp.out -time -control 1 2 ctrlDisp
expRecorder Control -file Control_ctrlVel.out -time -control 1 2 ctrlVel
expRecorder Control -file Control_daqDsp.out -time -control 1 2 daqDisp
expRecorder Control -file Control_daqVel.out -time -control 1 2 daqVel
expRecorder Control -file Control_daqFrc.out -time -control 1 2 daqForce

# End of recorder generation
```

此示例创建以无标题的 ASCII 格式将数据写入文件的实验控制记录器。记录先前创建的实验控制（标签为 1 和 2）的目标（控制）位移和速度以及测量（daq）位移、速度和力。