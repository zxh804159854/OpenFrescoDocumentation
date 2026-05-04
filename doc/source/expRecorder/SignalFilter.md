# SignalFilter 记录器
此命令用于构造实验信号滤波器记录器对象。它用于记录实验信号滤波器中的数据。

## 命令
```tcl
expRecorder SignalFilter <-file $fileName> <-csv $fileName> <-xml $fileName> <-binary $fileName> <-database $tableName> <-time> <-dt> <-filter $filterTag ...> <-filterRange $startTag $endTag> <-filter all> respType
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
| $filterTag | 要记录的实验信号滤波器的标签 |
| $startTag, $endTag | 要记录的实验信号滤波器范围的起始和结束标签 |
| all | 记录所有实验信号滤波器对象（注意：此选项仅建议用于 xml 文件输出，因为 OpenFresco 可能会更改实验信号滤波器对象的顺序） |
| respType | 定义要记录的响应类型。由于这取决于实验信号滤波器的类型，可能的参数在信号滤波器命令中描述。 |