# TangentStiff 记录器
此命令用于构造实验TangentStiff记录器对象。新增，暂无解释。

## 命令
```tcl
expRecorder TangentStiff
```


**✔ 输出控制**

```tcl
-time              # 输出时间
-dT 0.01           # 采样间隔
-precision 6       # 精度
-scientific        # 科学计数法
-closeOnWrite      # 每步关闭文件
```

---

**✔ 输出格式**

```tcl
-file output.out
-fileAdd output.out
-csv output.csv
-xml output.xml
-bin output.bin
-tcp ip port
```

---

**✔ 选择对象**

```tcl
-tangStif 1 2 3
-tangStifRange 1 10
```

---

**能记录哪些“物理量”**
查看源代码
ExperimentalTangentStiff::setResponse()
