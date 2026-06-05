

# 附录A 用于FC、SC和MC混合仿真的OpenFresco

OpenFresco最初由Takahashi和Fenves[26]开发。Schellenberg等人[20]对原始概念进行了进一步完善。它经历了几次改进，目前发布为2.6版本。OpenFresco提供了一种在计算驱动器和传输系统之间进行事务处理的标准方式。此软件框架使用C++编程，并利用面向对象编程范式。因此，它是灵活、可扩展和可适应的，支持许多不同类型的计算驱动器传输系统。OpenFresco还允许来自不同站点的用户通过其多层软件架构更轻松地协作。这有助于涉及多站点的分布式混合仿真。

## A.1 OpenFresco软件架构

OpenFresco基于三层和多层软件架构。这些软件架构是著名的客户端-服务器架构的变体。三层架构由客户端、中间层服务器和后端服务器组成。计算驱动器代表客户端。这是架构的顶层，在此对结构进行数值建模并执行分析。中间层服务器封装OpenFresco进程。在所有实际用途中，中间层服务器就是OpenFresco。中间层服务器调解客户端和后端服务器之间的交互。它处理从客户端到后端服务器以及 vice-versa 的数据通信和转换。后端服务器，最后一层，代表包括控制和DAQ系统的实验室。这是混合仿真的实验部分。

此架构提供了灵活性，使得各种计算驱动器和实验室设备可用于混合仿真。目前OpenFresco支持OpenSees、LS-Syna、Abacus和Matlab作为计算驱动器。它还支持各种实验室设备。

![](images/1102e68e77f39e1be21aad03200e02f10be2a4212e914aa1261f922a0efea047.jpg)  
(a)   
(b)   
图A.1：OpenFresco架构用于(a)本地部署和(b)分布式部署[20]。

### A.1.1 OpenFresco UML类图

![](images/79f2f492495a41180df589a00cac42743de0e9e9c23bf599e77e8c97d93002bb.jpg)  
：DC混合仿真的OpenFresco类图

![](images/e155f9d1875a4615c7849778ef43fdc02a01a0f0872912987047eb5093f5496.jpg)  
FC、SC、MC混合仿真的OpenFresco类图

## A.2 OpenFresco类

#### A.2.0.1 实验单元

实验单元代表有限元分析程序中的物理试件。它与分析单元有许多相似之处。它提供质量、阻尼和刚度矩阵；它还返回给定变形状态的力向量。因此，OpenFresco中的实验单元抽象类继承自OpenSees单元类。实验单元类执行从分析模型的全局坐标系到用于测试的局部或基本坐标系的变换。它还执行此变换的逆变换。此抽象类变换以下响应量：位移、速度、加速度和力。实验单元始终返回初始刚度矩阵，因为在测试期间难以准确确定物理试件的切线刚度矩阵。

以下是实验单元具体子类的列表：

• 桁架（1D、2D和3D）
• 梁柱（2D和3D）
• 两节点连杆（1D、2D和3D）
• 通用（1D、2D和3D）
• 倒V支撑

#### A.2.0.2 实验站点

实验站点代表实验室和计算驱动器运行的位置。这些站点不一定必须在同一位置。为了概括实验站点抽象类，实现了通信方法。此类还提供站点之间的安全通信。

以下是实验站点具体子类的列表：

• 本地
• 影子和参与者

#### A.2.0.3 实验设置

实验设置代表实验室中的传输系统，不包括控制和数据采集系统。实验设置抽象类执行从局部或基本系统到执行器坐标系的变换。它还执行反向变换。

-代表实验室中的传输系统 -变换 以下是实验设置具体子类的列表：

• 无变换

• 一个执行器
• 两个执行器
• 三个执行器
• 倒V支撑
• 聚合器

#### A.2.0.4 实验控制

实验控制抽象类提供与控制系统的接口。它允许OpenFresco与控制系统通信。它与实验设置类分离，以便在加载设置上工作的实验室技术人员不必关心控制和数据采集系统的IT方面。

以下是实验控制具体子类的列表：

• dSpace、xPC Target和SCRAMNet+
• MTS-CSI和LabVIEW
• 单轴材料和域仿真

## A.3 力控制混合仿真的OpenFresco代码

```cpp
class ESFTangForceConverter : public ExperimentalSignalFilter
{
public:
    // constructors
    ESFTangForceConverter(int tag, Matrix& initStif,
        ExperimentalTangentStiff* tangStif = 0);
    ESFTangForceConverter(const ESFTangForceConverter& esf);
    
    // destructor
    virtual ~ESFTangForceConverter();
    
    // method to get class type
    const char *getClassType() const {return "ESFTangForceConverter";};
    
    virtual int setSize(const int sz);
    virtual double filtering(double data);
    virtual Vector& converting(Vector* trialDisp);
    virtual Vector& converting(Vector* daqDisp, Vector* daqForce);
    virtual void update();
    
    virtual ExperimentalSignalFilter *getCopy();
    
    // public methods for output
    void Print(OPS_Stream &s, int flag = 0);

private:
    ExperimentalTangentStiff *theTangStiff;
    bool firstWarning;  // flag for updating the stiffness matrix
    int size;           // size of ctrl and daq vectors
    Vector dispPast, forcePast, convertFrc, incrDisp, incrForce;
    Matrix kInit, kPrev, thetangStiffMat;  // tangent stiffness matrix
    
    int setInitialStiff();
    int updateMatrix(const Vector* daqDisp, const Vector* daqForce);
};
```

图A.4：继承自ExperimentalSignalFilter类的ESFTangForceConverter具体类定义。

```cpp
class ESFKrylovForceConverter : public ExperimentalSignalFilter
{
public:
    // constructors
    ESFKrylovForceConverter(int tag, int ss, Matrix& initStif);
    ESFKrylovForceConverter(const ESFKrylovForceConverter& esf);
    
    // destructor
    virtual ~ESFKrylovForceConverter();
    
    // method to get class type
    const char *getClassType() const {return "ESFKrylovForceConverter";};
    
    virtual int setSize(const int sz);
    virtual double filtering(double data);
    virtual Vector& converting(Vector* trialDisp);
    virtual Vector& converting(Vector* daqDisp, Vector* daqForce);
    virtual void update();
    
    virtual ExperimentalSignalFilter *getCopy();
    
    // public methods for output
    void Print(OPS_Stream &s, int flag = 0);

private:
    bool firstWarning;	// flag for updating the stiffness matrix
    int size;			// size of ctrl and daq vectors
    int szSubspace;		// number of spaces vectors to use
    Vector dispPast, forcePast, convertFrc, incrDisp, incrForce, cn;
    Matrix kInit;	    // tangent stiffness matrix
    Matrix iDMatrix;	// the incremental displacement Matrix
    Matrix iFMatrix;	// the incremental force Matrix
    
    int setInitialStiff();
    int updateIncrMat(const Vector* daqDisp, const Vector* daqForce);
    int matTranspose(Matrix* kT, const Matrix* k);
};
```

图A.5：继承自ExperimentalSignalFilter类的ESFKylovForceConverter具体类定义。 

```cpp
class ECxPCtargetForce : public ExperimentalControl
{
public:
    // constructors
    ECxPCtargetForce(int tag, char *ipAddress, char *ipPort,
        char *appName, char *appPath = 0);
    ECxPCtargetForce(const ECxPCtargetForce &ec);
    // destructor
    virtual ~ECxPCtargetForce();
    // method to get class type
    const char *getClassType() const {return "ECxPCtargetForce";};
    // public methods to set and to get response
    virtual int setup();
    virtual int setSize(ID sizeT, ID sizeO);
    virtual int setTrialResponse(const Vector* disp,
        const Vector* vel, const Vector* accel, const Vector* force,
        const Vector* time);
    virtual int getDaqResponse(Vector* disp,
        Vector* vel, Vector* accel, Vector* force, Vector* time);
    virtual int commitState();
    virtual ExperimentalControl *getCopy();
    // public methods for experimental control recorder
    virtual Response *setResponse(const char **argv, int argc,
        OPS_Stream &output);
    virtual int getResponse(int responseID, Information &info);
    // public methods for output
    void Print(OPS_Stream &s, int flag = 0);
protected:
    // protected methods to set and to get response
    virtual int control();
    virtual int acquire();
private:
    void sleep(const clock_t wait);
    int port;
    char *ipAddress, *ipPort, *appName, *appPath, char errMsg[256];
    double newTarget, switchPC, atTarget;
    bool frcFeedbackMode;  // 0-converted frc or 1-daq frc feedback
    double *ctrlDisp, *ctrlForce, *daqDisp, *daqForce;
    int newTargetId, switchPCId, atTargetId;
    int ctrlForceId, *daqDispId, *daqForceId;
};
```

图A.6：ECxPCtargetForce具体类定义。

# 附录B µ-NEES实验设置的调谐

$\mu-NEES$实验设置是可用于验证混合仿真方法的实验设置。图3.13中所示的夹具提供可更换钢试件的可重复行为。它可以配置为提供不同的设置选项。两种实验设置配置用于力、切换和混合控制方法的测试。本附录显示了$\mu$-NEES实验设置的调谐。

## B.1 MTS-STS通道3的调谐：底部执行器

![](images/fa739bb9b3dbf70a6c5c973c847a5e0c8c3c6642d5c731595812288b93785afc.jpg)  
图B.1：使用振幅为0.1英寸、频率为0.25Hz的正弦波的1自由度$\mu$-NEES实验设置的位移控制调谐图。MTS-STS控制器的通道3针对位移控制进行调谐。

![](images/60195f2755d475482d970fa2893c768aa12d8c683a40eafc36733abb0d3b0cff.jpg)  
图B.2：图B.1上图的位移误差绝对值。平均误差为0.00154英寸。最小误差为4.04e-6英寸。最大误差为0.00470英寸。

![](images/644269877d58cff0bb737b0318d7da4ff617d19884d19c4bf49a4473a81e1aea.jpg)

![](images/6a821cd2780cf97c153cc7a6e5d29250f8df4a163f4fd64d7d6fa0a0607dcd8a.jpg)  
图B.3：左 - 使用MTS-STS控制器通道3在位移控制下的1自由度$\mu$-NEES实验设置的跟踪图。右 - 使用MTS-STS控制器通道3在位移控制下的1自由度$\mu$-NEES实验设置的滞回图。

![](images/b6c93736d4ebd351f4c2a5427c2e8c420d69f1f3ae0b1139769614fac28a83f9.jpg)  
图B.4：使用振幅为5千磅、频率为0.25Hz的正弦波的1自由度$\mu$-NEES实验设置的力控制调谐图。MTS-STS控制器的通道3针对力控制进行调谐。

![](images/d19985863b1f2afa690f783ab99db48d18153b712c13adf646ece69cee2d78d8.jpg)  
图B.5：图B.4上图的力误差绝对值。平均误差为0.0796千磅。最小误差为2.38e-6千磅。最大误差为0.261千磅。

![](images/6264ce246eddd6bc0a5366c6cd803612b9e22f315120f7250d3b8ce49a86cd1a.jpg)

![](images/6c382ec47d5da1218e91d1a5c7114d933292a750d3d00657c6b23bfe389c7f03.jpg)  
图B.6：左 - 使用MTS-STS控制器通道3在位移控制下的1自由度$\mu$-NEES实验设置的跟踪图。右 - 使用MTS-STS控制器通道3在位移控制下的1自由度$\mu$-NEES实验设置的滞回图。

表B.1：各种时间积分方案在控制系统水平上1自由度设置非线性混合仿真的绝对误差。显示最小值、平均值和最大值，以数值和量程百分比表示。

| 控制模式 | |误差| | |误差| (量程%) |
|---|---|---|
| DC-最小值 | 4.04×10⁻⁶英寸 | 0.00404% |
| DC-平均值 | 0.00154英寸 | 1.54% |
| DC-最大值 | 0.00470英寸 | 4.60% |
| FC-最小值 | 2.38×10⁻⁶千磅 | 4.76×10⁻⁵% |
| FC-平均值 | 0.0796千磅 | 1.59% |
| FC-最大值 | 0.261千磅 | 5.22% |

## B.2 MTS-STS通道4的调谐：顶部执行器

![](images/1150ef44b6aa348a5532829ad1457c6dcfb549fbd42ff3f05d9a198d5f147eb8.jpg)  
图B.7：使用振幅为0.3英寸、频率为0.25Hz的正弦波的2自由度$\mu$-NEES实验设置的位移控制调谐图。MTS-STS控制器的通道4针对位移控制进行调谐。

表B.2：各种时间积分方案在控制系统水平上1自由度设置非线性混合仿真的绝对误差。显示最小值、平均值和最大值，以数值和量程百分比表示。

| 控制模式 | |误差| | |误差| (量程%) |
|---|---|---|
| DC-最小值 | 1.10×10⁻⁸英寸 | 3.67×10⁻⁶% |
| DC-平均值 | 5.47×10⁻⁵英寸 | 0.0182% |
| DC-最大值 | 0.00357英寸 | 1.19% |

![](images/09454409ca51dd738dfd35858bb2fea1d12c9f3db3d89a538a044b1511846289.jpg)  
图B.8：图B.1上图的位移误差绝对值。平均误差为5.47e-5英寸。最小误差为1.10e-8英寸。最大误差为0.00357英寸。

![](images/357b6ae5dcb630185beb4f4f6eec5ad8b9bbeb23e281d677855be741efa3f482.jpg)

![](images/927dc42881678bd78a5ed6b0c77ab9690382c0fef7bd7aadb2572bc93d515db8.jpg)  
图B.9：左 - 使用MTS-STS控制器通道3在位移控制下的1自由度$\mu$-NEES实验设置的跟踪图。右 - 使用MTS-STS控制器通道3在位移控制下的1自由度$\mu$-NEES实验设置的滞回图。

# 附录C FC混合仿真实验结果

本章包含使用两种不同配置的$\mu$-NEES实验设置进行FC混合仿真的实验结果，即1自由度和2自由度设置。在每个两种设置上运行线性和非线性混合仿真。部署了NME、$\alpha$-OS、NMF和NMR，但并非所有仿真都成功完成。有些不完整，因为STS控制器变得不稳定或时间积分容差限制不满足。这些时间积分方案的分析结果比较在第3.4节中讨论。

## C.1 1自由度设置：线性混合仿真

第3.1.2节中的El Centro缩放到15%以保持试件在线性范围内。混合模型如图2.1所示。绘制了有限元分析水平软件中单元1（实验单元）的变形和抗力随时间的变化。这些响应量与OpenSees分析中的数值对应物进行比较。显示了DC混合仿真的STS控制器指令和测量位移。还绘制了CFC和EFC混合仿真的STS控制器指令和测量力随时间的变化。这些仿真的结果绘制在图C.1至C.13中。

![](images/7a9f2c5f4fe18783bc0bc674e3c96af8bca6f76fe61b9df9a22d8023b2972855.jpg)

![](images/c988cb97013333096acd3f6de9f78676259ea0a5e4c226a518a1ff74e28d51ac.jpg)

![](images/1936f844d812f0ff835d35bbc7a8f99b6805bce40cb30771349a7fc1f0493a87.jpg)

![](images/fd35e230a9c9e72f8096f1d469691e1e211da26f8c77f7ce96bda1f5ea778578.jpg)  
图C.1：FC混合仿真的单元1位移-时间历程图（上）和位移误差（中上）。单元1抗力-时间历程图（中下）和绝对抗力误差（下）。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NME与DC和CFC。

![](images/eb000e8c1837d6f5f14d8ad69811bf4d4dfa487dfb35c0716d437a13aa68891b.jpg)

![](images/b40bfc34a47eab47eb68844473e0234df0dbd8bfa4adfd2cd7b3087063cf8a7b.jpg)

![](images/d07cc7342e3aec996449cbe01d3bc061a2cd8c96d0484e409ed3b9a7a2edc8b3.jpg)  
图C.2：上：DC混合仿真的STS控制器指令和测量位移图。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NME。

![](images/77ed9ee61be28a535d1d11e2c13f9b65e3f27fb15336ac882dcfc26d632cf99b.jpg)  
图C.3：上：CFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NME。

![](images/518bc7a1ab4f97e640564d0ddce41f3778fcc45e208acec88e0fd7bb0200cd03.jpg)

![](images/6314291eca12af48a3c174e86967c6a72a8e86d18dd4d48be32c71b49ac75ee7.jpg)

![](images/811ed393b9b6561ce6df4d70cb64e006f2d576c5c941c59515a1f0f138d6d5a5.jpg)

![](images/e0852d11278a060470ed07bb90b71d1b53dc495a7abd9a6abdd4a067920d32aa.jpg)  
图C.4：FC混合仿真的单元1位移-时间历程图（上）和位移误差（中上）。单元1抗力-时间历程图（中下）和绝对抗力误差（下）。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用αOS与DC和CFC。

![](images/d4886826533199361c97f7839a242dfb31aeeaf58c929bd751c2f80454a088e8.jpg)

![](images/687669c13f381b3d81d914af2d1a105e3f2b0f9ae4f9dc884ca52a7eabb0c029.jpg)

![](images/c6f885228a3159f3eb2e54a9959b3c4c6f0d1fdc4798803fa44608642f0c160a.jpg)  
图C.5：上：DC混合仿真的STS控制器指令和测量位移图。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用αOS。

![](images/5cf5b5fdf0328335babf2c4fdbbde2ae4a13c1d7f7c031f855121b14904d8c50.jpg)  
图C.6：上：CFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用αOS

![](images/69aaba162d16110dc7b1552b016cc88b9c595101dcd7d47a0a3e94df57522f41.jpg)

![](images/e2343820004f1c7788364d50620e21fd8618e903280deadd75b5779a8493c745.jpg)

![](images/97abffadb923a8766c6c113dbad993d2fe9159ad19346c3d7ed8c0c85f67f9a5.jpg)

![](images/789534b2befb580c578026b4a5067335c9e69212516181d32a250e11d313255a.jpg)  
图C.7：FC混合仿真的单元1位移-时间历程图（上）和位移误差（中上）。单元1抗力-时间历程图（中下）和绝对抗力误差（下）。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMF与DC和CFC。

![](images/9b21e8d7518b3b97d6f2207a66f942c5cf40ceca086d9fbb5b1ab34a9a36128f.jpg)

![](images/61fff871ea549e8263893afd11cacd2119421b94ed020f10fe1b3e78f83db013.jpg)

![](images/3650c6ce2869f239d96c3a37183965dbb02dd3ddc2b1e9fadbcc734bfdc085fd.jpg)  
图C.8：上：DC混合仿真的STS控制器指令和测量位移图。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMF。

![](images/ebff7a7b2ed00d4da27af9a1135092bd72092a43592b006fb53cd9ed7a0c82c0.jpg)  
图C.9：上：CFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMF。

![](images/ee2b35d6a164fe243f57cbd918d550317517da457d3afa56549bdac5c11170a2.jpg)

![](images/21b6ca4fc3edbcf56d3825a74c1571434bbd1657ce2471e426bb6790dfbabad.jpg)

![](images/2304a5880a5a03b169db3936a5d7345d508204699213b2ba77b228a6ee9d6b98.jpg)

![](images/a6a0d70327b8f1bc5813bda7d3314a81fad6c4134c036cfac4710e477aa1d763.jpg)  
图C.10：FC混合仿真的单元1位移-时间历程图（上）和位移误差（中上）。单元1抗力-时间历程图（中下）和绝对抗力误差（下）。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMR与DC、CFC和EFC。

![](images/314bb187abe7be3527864da2ce5bed68073083436ec949bfd56c050d79c02f00.jpg)

![](images/b72f46b7d7f82a5442284644aaf723ea30f90bcd0f8037effce6400fcd771e0a.jpg)

![](images/5f42e91f82a0280eed9c7ceb3c4e877c559d7a45844f7f799912efe7cf8da5f0.jpg)  
图C.11：上：DC混合仿真的STS控制器指令和测量位移图。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMR。

![](images/8226fd1d18b91873b93c83b0985709860df9a8d0f39c54157bcc0a380d8c2513.jpg)  
图C.12：上：CFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMR。

![](images/81d9fd9ba6260cd4032ff0ffc89c481793a108791665740500ce02f56e708975.jpg)

![](images/ef3ec97a21d5d8b31e4ff05de590045e9d5807e73cf04dff97a8d3c1fcb9c18a.jpg)  
图C.13：上：EFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放15%以保持仿真在线性范围内。1自由度设置使用NMR。

## C.2 1自由度设置：非线性混合仿真

第3.1.2节中的El Centro缩放到40%。混合模型如图2.1所示。绘制了有限元分析软件中单元1（实验单元）的变形和抗力随时间的变化。这些响应量与OpenSees分析中的数值对应物进行比较。显示了DC混合仿真的STS控制器指令和测量位移。还绘制了CFC和EFC混合仿真的STS控制器指令和测量力随时间的变化。由于仅使用1自由度时所有CFC方法都退化为估计割线，因此CFC方法使用割线估计。这些仿真的结果绘制在图C.14至C.19中。

![](images/e12a6f628de20a0f50b2966ca47f9553496b422e920696b424a7ba19e542f305.jpg)

![](images/698aac3f5511a7003b5c0d946f95923e8bb99e68234f3d83b6d1556659ab753f.jpg)

![](images/e6220867d0b04a1ee5c2fa285065681e5b66fb1c6b84d2c13bada495c9a75952.jpg)

![](images/2cda11712c1c5840e5c2d003483a76f0a1c6e8a195e842fcd370cf1ce9ba6b06.jpg)  
图C.14：FC混合仿真的单元1位移-时间历程图（上）和位移误差（中上）。单元1抗力-时间历程图（中下）和绝对抗力误差（下）。地面运动缩放到40%以将试件推入非线性范围。1自由度设置使用NMF与DC和CFC。

![](images/ba66ca166b42afe61dabdbd8fd2149a34533b50d77f86d656bce2edcfc86c41c.jpg)

![](images/d1f71dcc79e1b158930918958d155cc71be34f484652f1903a3935929f263f76.jpg)

![](images/f43ff25d7630347c59ce072e19199caa90eaefb0a2cd6657ed07e39cdc29461f.jpg)  
图C.15：上：DC混合仿真的STS控制器指令和测量位移图。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放到40%以将试件推入非线性范围。1自由度设置使用NMF。

![](images/ef90d383b4f9403546216bb2d993ab2912de610db592aac4a89b2c903a64a884.jpg)  
图C.16：上：CFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放到40%以将试件推入非线性范围。1自由度设置使用NMF。

![](images/afbb119a47a7dd9e1b67cdc7850912a51df1b664f0611cc011b88a477e1e61c32.jpg)

![](images/eecccbd85482df01882ef11c103c52d1db6bc819c3b3c09549ec24a74209aec5.jpg)

![](images/426ba37fe4de4eeb932b57eec4e5c7263cd548c0a72053230c22cc4964ce7fcb.jpg)

![](images/b88b7b457790fca6596b6157dd80e175d47015768ece6ef48f14034fc1b06f83.jpg)  
图C.17：FC混合仿真的单元1位移-时间历程图（上）和位移误差（中上）。单元1抗力-时间历程图（中下）和绝对抗力误差（下）。地面运动缩放到40%以将试件推入非线性范围。1自由度设置使用NMR与DC和CFC。

![](images/7bdfd833dc63880fcc5f4fc4aa8bb983876690d00c6e886ca90d2e82717b02c3.jpg)

![](images/d2a106a8a3fb45f2a89bbffa74b7c54887a7435a1666c3a322a7be923fcdf645.jpg)

![](images/f9d8b1167ecf93959b9e759a050b25c52605ee3bbc8ce4b016ba466514b8d63d.jpg)  
图C.18：上：DC混合仿真的STS控制器指令和测量位移图。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放到40%以将试件推入非线性范围。1自由度设置使用NMR。

![](images/16341d316cffcf98c0e4ff26f5a5f805a1b05a7a0eb84a200bb4d63ad47d2854.jpg)  
图C.19：上：EFC混合仿真的STS控制器指令和测量力图。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放到40%以将试件推入非线性范围。1自由度设置使用NMR。

## C.3 2自由度设置：线性混合仿真

第3.1.2节中的El Centro缩放到10%以保持试件在线性范围内。混合模型如图3.21（右）所示。绘制了有限元分析软件中实验单元的节点位移和力随时间的变化。这些响应量与OpenSees分析中的数值对应物进行比较。显示了DC混合仿真的两个执行器的STS控制器指令和测量位移。还绘制了CFC和EFC混合仿真的STS控制器指令和测量力随时间的变化。即使测试了其他方法，也仅绘制CFC:BFGS结果。这是因为在线性仿真期间所有CFC方法都使用初始刚度矩阵，并且不更新刚度矩阵。这些仿真的结果绘制在图C.20至C.36中。

![](images/f9c76f8a1d02d969460faa4ca1075fed7cfeb239f8ec6ab9a575209194085712.jpg)

![](images/6b18371329055f65e8cea3916c9142cd593737893600c679bce8472e6b178939.jpg)

![](images/e68aa0179b5a92861dd4c860067c70cfa25eff46c70503de1780851f58c5767c.jpg)

![](images/71e8f7d13ab6e87b5acf52fc777c9362c83ec37926bea4709669088a59d04169.jpg)  
图C.20：FC混合仿真的节点1位移-时间历程图（上）、节点1绝对位移误差（中上）、节点2位移-时间历程图（中下）和节点2绝对位移误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NME与DC和CFC。

![](images/6c647587ce396127e249b08e537a4d98f7b8c4bd14667fb4f902daf40b28ef0d.jpg)

![](images/40b5979f974459d6357b30a95a97025540d7559d0b8df0c9eee9bc5097ecc582.jpg)

![](images/1bb5f38b503891dd9e9dafacbc9aa39ee53389caf7c3a411e2d63618d4b33c55.jpg)

![](images/a986e3af9f104753633e5f414ed9a8015ea777412b47c285d4f2087d07491133.jpg)  
图C.21：FC混合仿真的节点1力-时间历程图（上）、节点1绝对力误差（中上）、节点2力-时间历程图（中下）和节点2绝对力误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NME与DC和CFC。

![](images/ad4b53d9335b8c72b17e659ecbecde0d61d0c1487e7977539bfd7d0676a2bfbe.jpg)

![](images/b45f773dc0211d70d0cc2fe923f40583b0e9ba0daa3b727472c744920d0fccf3.jpg)

![](images/51f0c6f8784ab2daafaef8708b2628aa4f56177f693a63df8cc86a0d81dcfb1d.jpg)

![](images/3d4eaad0cbbddc6966d3a0c1a8cb7625711759991d41c9a84072e910425c11ce.jpg)  
MATLAB学生版图C.22：DC模式下底部执行器STS控制器的指令和测量位移图（上）。底部执行器STS控制器指令和测量位移之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量位移图（中下）。顶部执行器STS控制器指令和测量位移之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NME。

![](images/a046f3ecf715bc55b0d6d09ae35bde043e72abf87c4109cded120267ebee11a7.jpg)

![](images/578101b826e992b0bf29b2da41d81bb60edefe3ce9fa0d7178783618f89bb261.jpg)

![](images/47873e4bdceead1ba9096862f5bd5777fb2017a1e893adf39f0f25e6daab296e.jpg)

![](images/686a988007df81a3c3bf602c9dfc37eae17a88596fc7405a05bd6603da6d335e.jpg)  
MATLAB学生版图C.23：DC模式下底部执行器STS控制器的指令和测量力图（上）。底部执行器STS控制器指令和测量力之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量力图（中下）。顶部执行器STS控制器指令和测量力之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NME。

![](images/0727893e8ed5f3df2c49aa697771ef44e3f5f954454432b387ffabfdca95511b.jpg)

![](images/5782cc436b275f715b66318d0454aeffdf07ade0195bc1c2fb185fabd559fbfc.jpg)

![](images/f2f754f341b68a820345486b1c6aa2ce079a9b35df422b52affe570e853b851e.jpg)

![](images/cd14d5922f7d129f1c8b169b4034126db75254ca7834639fd68b06b38902ddc3.jpg)  
图C.24：FC混合仿真的节点1位移-时间历程图（上）、节点1绝对位移误差（中上）、节点2位移-时间历程图（中下）和节点2绝对位移误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用αOS与DC和CFC。

![](images/dc15be0facd8ef06fd758438ee1ffd10cf264ab47dee541e9cccc7bfb47d2572.jpg)

![](images/0fbf16cec9b8c52a3d4b1883d368fd9dd6c9c6eaba8443915d2ee89fe5f84113.jpg)

![](images/85a3a853ee121af9fef576c3f74000856b0b9c7dbacbd44da931ed9e32ca2c5.jpg)

![](images/d934d498f95eef5db50bb7c2d6102d0973fd04bbd6aefa232eaebdb1eb3be077.jpg)  
图C.25：FC混合仿真的节点1力-时间历程图（上）、节点1绝对力误差（中上）、节点2力-时间历程图（中下）和节点2绝对力误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用αOS与DC和CFC。

![](images/4a7d8231f52512d945d9bebfa6e645b8347ac5fcf69027b65395a78c4b778341.jpg)

![](images/5c8addc149507b541dca4bce8054e30e1b2f6ce047aa5392db7ae59998c70151.jpg)

![](images/6b258b2a83472d06fcbc1072e51f6bdeda5d8504c6d59beaa4a3efc8da656a5f.jpg)

![](images/be5bfbd410c82d41116cf8da854cecfe41b704930317f46c03bc5a48e0011a85.jpg)  
MATLAB学生版图C.26：DC模式下底部执行器STS控制器的指令和测量位移图（上）。底部执行器STS控制器指令和测量位移之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量位移图（中下）。顶部执行器STS控制器指令和测量位移之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用αOS。

![](images/425242a8411ea122a56c8234d5d38d8ba82d3cb3aeb53566bd934e1d0a2a05ac.jpg)

![](images/aed868bf06ea2591f89c7117b7c62c9b34f53be1933e78ba245af3bbf726c6cf.jpg)

![](images/d7d2e7e9addf814ae1b5818d5cee3da950f7a0bc49214f6a79b011858aa39cdf.jpg)

![](images/53ab6081d6e18b63d2de04aaf3eb7f839e0d9e42323b2a6f3ff4cd0c3d7916bb.jpg)  
MATLAB学生版图C.27：DC模式下底部执行器STS控制器的指令和测量力图（上）。底部执行器STS控制器指令和测量力之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量力图（中下）。顶部执行器STS控制器指令和测量力之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用αOS。

![](images/a9b6e928e1a3649875fc98d99e09ce29f9d70648eb36c62efbea4687ec5bfd59.jpg)

![](images/269fce87a32471d5dba422c9118c8bc06a5711f8383061e02a64e362a9a8b2e2.jpg)

![](images/7b7be682a8cf7c3b106465b84cfefbe8465b6cd2f126bec99b9eb702d9c616ab.jpg)

![](images/2bcc4345a07debe137bd212bdf5717366bf5c77149635a8c9c0783f32f148613.jpg)  
图C.28：FC混合仿真的节点1位移-时间历程图（上）、节点1绝对位移误差（中上）、节点2位移-时间历程图（中下）和节点2绝对位移误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMF与DC和CFC。

![](images/01342294ae07b881bf55dc3d3011801c77c33d1cb606b7f766386f323c8bb6eb.jpg)

![](images/2e29ceadcda4f4f0486ecd812b67db213d7141f7cb04355a3fa2e100407dec7a.jpg)

![](images/86784f1454379db62f19c19b2db1f434ca3f9561fedca03ac7d72032b06e30b4.jpg)

![](images/591654e7af63e1f709f5f2ed0fb8153a36c5058bc30ed0f6e42778c64996980d.jpg)  
图C.29：FC混合仿真的节点1力-时间历程图（上）、节点1绝对力误差（中上）、节点2力-时间历程图（中下）和节点2绝对力误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMF与DC和CFC。

![](images/54221fbb254b4fe232633b8b037ce5b1c91280111d910d5deabcc183dc9653dd.jpg)

![](images/602355d4387b10e27647130a4a6adda09fe7e4ff67262e9f82b80dd9ac83dd01.jpg)

![](images/ff635446d0455da9ce813b710d20edebdcef2822ec0974d02fcee8446477bbbb.jpg)

![](images/da25c194fee1b6d2e3670279927be88e472a73dd3a1faa6b9a227de1a231abba.jpg)  
MATLAB学生版图C.30：DC模式下底部执行器STS控制器的指令和测量位移图（上）。底部执行器STS控制器指令和测量位移之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量位移图（中下）。顶部执行器STS控制器指令和测量位移之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMF。

![](images/cfa58e2c4ae9b60baae90b3b23af678afc0e77972496a923011ae60782ce8573.jpg)

![](images/c038a83cd42f6742b8469102fbe50020bbc1d383b5fc409b61975d526ab6edb8.jpg)

![](images/9f236b74ec28a1a68c75de1cfd5843da8ab1389f46bb6ad2bfe17264c390f380.jpg)

![](images/815a987114449273eed73d3e0b18ed86c6ae74933f81bc9a58b3370a811ca7fe.jpg)  
MATLAB学生版图C.31：DC模式下底部执行器STS控制器的指令和测量力图（上）。底部执行器STS控制器指令和测量力之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量力图（中下）。顶部执行器STS控制器指令和测量力之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMF。

![](images/8d81d89f374427be8914b854e0318445fc9ea7c586ef6ecc06bbc7b33cd94eac.jpg)

![](images/13c2d90be3135a2bc7e37cc5d5bd8de23adf674955d802a1103c77a50292f33a.jpg)

![](images/cea2af2da031b1b9d52bab1a5b556acbe2551e06000537318a1d3e25aee92639.jpg)

![](images/c1388f74b4209f3dccbed1a9a7cd9c0bd3c884326fdcefec8ef46f58f325ca8c.jpg)  
图C.32：FC混合仿真的节点1位移-时间历程图（上）、节点 1绝对位移误差（中上）、节点2位移-时间历程图（中下）和节点2绝对位移误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMR与DC、CFC和EFC。

![](images/935b0e72a9beb92f1b27db2635f075f765415bc874ea6fd335a0f53b451649f8.jpg)

![](images/f7444edb3710b65ec68ee89c8fac9711307d28f0466859c9a88f0a3a024fd841.jpg)

![](images/ba01e2e999f79f2e4d719c7e34bfe0018bb8dc264b0e3a8f78b5592daffbe534.jpg)

![](images/a4bffc991d8a0afb3b2488ce63c7f38f9463ffad549c4ab36f1f4602b050ede8.jpg)  
图C.33：FC混合仿真的节点1力-时间历程图（上）、节点1绝对力误差（中上）、节点2力-时间历程图（中下）和节点2绝对力误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMR与DC、CFC和EFC。

![](images/a93043c078f4968decfebe171786932df1ce80f1c704c3db03a6d82337bcd748.jpg)

![](images/a676f0e8890234ac620a572ce1daa23c878c8fc38a7f05de0a46bcb64f70b62.jpg)

![](images/f8b126149ad6e2fa6ceb700a197b339c801eae111d063e7251730d96e975da8.jpg)

![](images/e71b50c680f6bc22b8242c7de185ae236e7ac74c96cfb608f244c6782d9f4969.jpg)  
MATLAB学生版图C.34：DC模式下底部执行器STS控制器的指令和测量位移图（上）。底部执行器STS控制器指令和测量位移之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量位移图（中下）。顶部执行器STS控制器指令和测量位移之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMR。

![](images/390d72375d57c18b563690c793b2afc2cb796035e78e0c8d2493af51928eddd9.jpg)

![](images/fdf54253ea84cacd852fccb90771010155147b02e7745686ee541267f2650fb5.jpg)

![](images/16a5a9ec87db3b65c3ab33c46c3bd14f8195a08cdd371528d6c28052cff8684.jpg)

![](images/2362bcdbfcafdd8f28db7055b98230333903f42fbe74c363d3a8d29929b25650.jpg)  
MATLAB学生版图C.35：DC模式下底部执行器STS控制器的指令和测量力图（上）。底部执行器STS控制器指令和测量力之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量力图（中下）。顶部执行器STS控制器指令和测量力之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NMR与CFC。

![](images/31e10a9cf2cc2721c4f61ec86d1dd828da4f4f09a1eaf9efa62ce461a05a7700.jpg)

![](images/adeb86e8f364e8ab10bac8bbd9950ad7db640d00679b43cddc8acc58ea28bbd9.jpg)

![](images/b1ae1238404c0a93c3a62f0681ae8d25bbfcda8ca529f6082850c3eb3ef79cec.jpg)

![](images/f8af414bc889e7f02a3f95240f95a4ec054458dc0e1c9f337801fc41083c042d.jpg)  
MATLAB学生版图C.36：DC模式下底部执行器STS控制器的指令和测量力图（上）。底部执行器STS控制器指令和测量力之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量力图（中下）。顶部执行器STS控制器指令和测量力之间的绝对误差（下）。地面运动缩放到10%以保持仿真在线性范围内。2自由度设置使用NME与EFC。

## C.4 2自由度设置：非线性混合仿真

第3.1.2节中的El Centro缩放到50%。混合模型如图3.21（右）所示。绘制了有限元分析软件中实验单元的节点位移和力随时间的变化。这些响应量与OpenSees分析中的数值对应物进行比较。显示了DC混合仿真的两个执行器的STS控制器指令和测量位移。还绘制了CFC和EFC混合仿真的STS控制器指令和测量力随时间的变化。虽然测试了所有方法，但仅显示成功的测试。当时间积分方案的容差限制未满足或STS控制变得不稳定时，某些测试不被认为是成功的。这些仿真的结果绘制在图C.37至C.54中。

![](images/c608eb313a46c3f3a0c04712a4e3f9fe98e359f98d4e0b91631fb713d3074753.jpg)

![](images/23fb7d95ddc0a7dbdd79e8c4f74dfaf032cfd12be104b241afc4d2c11d5e5ce1.jpg)

![](images/4d334d255e44d1139aac68b89580d3bf1f4de8b12aeddecf653daa1578d77251.jpg)

![](images/256b11f543b6d8ae0501379762a2ae45803c1972593651c9b32603e82a2f5746.jpg)  
图C.37：FC混合仿真的节点1位移-时间历程图（上）、节点1绝对位移误差（中上）、节点2位移-时间历程图（中下）和节点2绝对位移误差（下）。地面运动缩放到50%以保持仿真在非线性范围内。2自由度设置使用NME与DC和CFC:BFGS。

![](images/5b8efb2fe99db8eb2a12e60ecbe3499e969d9f99373311cf77a7397df4524d9e.jpg)

![](images/7eb9fb1c7f2fba1d325ecffd2cd49ccaf079fd3e75058b356493e6020f09fa59.jpg)

![](images/9b479fcb4b4d230b2e812b74485c4fcdb3c685503419be7f39f56e2b709c4f40.jpg)

![](images/5f674d8388d0b33da9e09b7e902396f92e130503670413c970a1f139d64b7bbf.jpg)  
图C.38：FC混合仿真的节点1力-时间历程图（上）、节点1绝对力误差（中上）、节点2力-时间历程图（中下）和节点2绝对力误差（下）。地面运动缩放到50%以保持仿真在非线性范围内。2自由度设置使用NME与DC和CFC:BFGS。

![](images/4504833b505d84ff34d9906fe9cb0392963b840a578a1b3874549dd5337a897e.jpg)

![](images/78dc1ace19b9b2ad8e26e1b6e8796332165629e8efaa29554af4b0e251954078.jpg)

![](images/0a45e8e4095b5e7906fb71b11e6ba4e52883d3cda9cf269d51494a7f364c9ca3.jpg)

![](images/23b5b7dcbe8428407e97b7573255abc63fbfe42009200ae1836e4339f7701aea.jpg)  
MATLAB学生版图C.39：DC模式下底部执行器STS控制器的指令和测量位移图（上）。底部执行器STS控制器指令和测量位移之间的绝对误差（中上）。DC模式下顶部执行器STS控制器的指令和测量位移图（中下）。顶部执行器STS控制器指令和测量位移之间的绝对误差（下）。地面运动缩放到50%以保持仿真在非线性范围内。2自由度设置使用NME与DC。

![](images/5722a19cf4b80b436f91cb75c5cff16e3fb0f03e21fe78714076c280df841ee7.jpg)

![](images/d6a78bfd3ff0009e74fd594bc2eb19d9a8577c5fa652a54222c84847035764ae.jpg)

![](images/1b37810eb76316d507db5959d7093ec7787e02302f17c2041518d1020419e125.jpg)

![](images/8cdad3173dec4b946ee21a535e5ebae85d5f9141ef2cf793e0564badb6d1fccd.jpg)  
MATLAB学生版图C.39：STS控制器在DC模式下底部作动器指令和测量位移曲线（上）。STS控制器底部作动器指令和测量位移之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量位移曲线（中下）。STS控制器顶部作动器指令和测量位移之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NME与DC。

![](images/40758908deafae01b13c985bc9a2b2fc60254abb4ae938589e2a8534c05e1ad9.jpg)

![](images/70597951d976f57160d34675a70fe496ee949297a8eec103c6fa7e7a7b866bf0.jpg)

![](images/50553054598e399e81dd79d460441ed3ca9226411226f707647a9cef4ec27051.jpg)

![](images/3bda34064f7735ac38e31484944d57d84075c99c4d774e6c9ce47d1f028ea9bf.jpg)  
MATLAB学生版图C.40：STS控制器在DC模式下底部作动器指令和测量力曲线（上）。STS控制器底部作动器指令和测量力之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量力曲线（中下）。STS控制器顶部作动器指令和测量力之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NME与CFC:BFGS。

![](images/0a86e171223030a1ab00cea90e06342faa7d9a4c638b48a92aedbd5b1ab7d2ba.jpg)

![](images/decc2afafecafcc2c842a975848dbee245b12d02afad422b62dfa2833056199e.jpg)

![](images/718757574196ce21088077d3788b7759b2fdcbc7d8c62d3d1d59ba0407c27b05.jpg)

![](images/dbd92cfe57233b69c4b427e09eded6f36c177a470d39286e8120ae88f62bd16f.jpg)  
图C.41：FC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC、CFC:BFGS和CFC:Intrinsic。

![](images/e6b2a4061bb978bac264cd1991f0c71ab4389840afe43a8621e59497826734f5.jpg)

![](images/bf641a09ce8bae9ac438c22e0eee13c54570070fc08a1a72ed9a76605bdfc042.jpg)

![](images/e726c603d0427e533fa7c595772c32c53a476aa813bd638de539ca97a4713bf0.jpg)

![](images/4ed02de654a80ff60c3998a66fb8ab267df37475cda7e4d33c820e9fbab145b2.jpg)  
图C.42：FC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC、CFC:BFGS和CFC:Intrinsic。

![](images/2c817fd57481c8ee1b587a6b04160cf0fb9a9688d7526ccf58baa7c2d4101354.jpg)

![](images/446b3d26ff6a7ed3cc4ea0c582531720b7028958a78dc18ac0c09604fc91dcf2.jpg)

![](images/ed85839190a4bf9b6a4fbb0c83ee6102b6bc615268b61c002168183613c207cf.jpg)

![](images/5f7a6590534b608237ebab0fda3889836c3088bc45e75d23ddf6aed618d7e80a.jpg)  
MATLAB学生版图C.43：STS控制器在DC模式下底部作动器指令和测量位移曲线（上）。STS控制器底部作动器指令和测量位移之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量位移曲线（中下）。STS控制器顶部作动器指令和测量位移之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC。

![](images/ad0590241f6032bdd8be67daef04465f52ed9275260f033e0f991d0d8b9ee2e1.jpg)

![](images/4ba3606d7b99b3044203d4082b28190279f09d5a1209b05dd31e7fe1e908d23c.jpg)

![](images/fbe87b86ec387e7983fdb633c70532c48c8bc6a5d5c7e0be368b891cb5b24ed4.jpg)

![](images/744052e62c450af6f90a69ce5c96931114304597797758d32e12b5f6d9d70ed7.jpg)  
MATLAB学生版图C.44：STS控制器在DC模式下底部作动器指令和测量力曲线（上）。STS控制器底部作动器指令和测量力之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量力曲线（中下）。STS控制器顶部作动器指令和测量力之间的绝对误差（下）。2自由度设置使用αOS-CFC:BFGS。

![](images/d592424693d79c7cc22f80338adc3d5415dd720a1280786feb477897630f0d69.jpg)

![](images/d4dfc801baefad3d8b1b6eb172f9ecf4025446ca6f93c6b4c8788ea15c013c4a.jpg)

![](images/59f2183237c76e327759c433160ea1f1cd8983cba746286b7a19bd5d630e7dd0.jpg)

![](images/f87fb636c683504e14de2b9e47b5648074fd097e9989426ac728e914dce73b5c.jpg)  
MATLAB学生版图C.45：STS控制器在DC模式下底部作动器指令和测量力曲线（上）。STS控制器底部作动器指令和测量力之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量力曲线（中下）。STS控制器顶部作动器指令和测量力之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS-CFC:Intrinsic。

![](images/e847d47994072f7eace7af22d8618d6d7d40f6342a95b8ec7ad42ab46b49694d.jpg)

![](images/50f733c758b09d0b519192a5aefc68c6e5eedf6a6d44ba8522cf22cef9164817.jpg)

![](images/5ddc19930b642b19c2f22d0ab9f4f58f61a55bb12183ca2c363701a3d5311a61.jpg)

![](images/c9f10fa4a6065892b60998cbd439bc3f11a3f869ffb9b0788d1bfbe25b42153b.jpg)  
图C.46：FC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC和CFC:BFGS。

![](images/702894298c57988ad960ea918f885243c9ce0846aef83c1ce44c6d55e2b6bc7a.jpg)

![](images/406c420a9458702939ea536c1806b07066ca64ee82e4c11297000ef1cf079f21.jpg)

![](images/7af1464bdcae943a2977f29e54535cd1e610e3154e0722a447216c61e7053ab8.jpg)

![](images/c1f97926fa2a016733c897d435752b0ed30f849fc168174a90961ec951a4c531.jpg)  
图C.47：FC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC和CFC:BFGS。

![](images/59c7d29fe4b4db6a63d833d4614350b7d280c4ec605331855178e2aff9b3761d.jpg)

![](images/da69a3651c9b470947c0cac87403900d0af7b7fbd0e384d50b1cfa39239c1421.jpg)

![](images/af063fe362e8d69e4d2043867a6bdf9326af65e82c3feca534c6b431bdc26843.jpg)

![](images/07b8fef89faaa447c46e6e0512c41461e8fc523d7526033e21e4d19d50f62634.jpg)  
MATLAB学生版图C.48：STS控制器在DC模式下底部作动器指令和测量位移曲线（上）。STS控制器底部作动器指令和测量位移之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量位移曲线（中下）。STS控制器顶部作动器指令和测量位移之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC。

![](images/31d43516acfaaf225e8643f941e0c470d5ef327a66c78a050e83ce8d3af7d107.jpg)

![](images/d14183a991506aada0cd72e9eae926ed76eb37ae5b08f69702e11a0e84cf7955.jpg)

![](images/a339c7d51521bffbc6a6ff6cbbaf2f7a086a8c3256a125d1ecc882678feed391.jpg)

![](images/b274b8b79a1d53069df47f4349e41ae639323c51853bf625ea99b8f4da5c7c5a.jpg)  
MATLAB学生版图C.49：STS控制器在DC模式下底部作动器指令和测量力曲线（上）。STS控制器底部作动器指令和测量力之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量力曲线（中下）。STS控制器顶部作动器指令和测量力之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与CFC:BFGS。

![](images/1d0f78d6fd25377884d73218f5b52633753a56d1f98767d6be1851fe8534d75d.jpg)

![](images/d12320466d53b7c37f8552deecf6d073e3013fe6c43d2223e8262bcbbfbcd350.jpg)

![](images/d02dd7ec5b8f3dfcad14d2c953141ad48c4f3934783d4a5259962d9c4d30ff18.jpg)

![](images/3401d9e968a6d939171b3633d9430a3510ffd4f5f68c6e02eb2d7d6fc234036d.jpg)  
图C.50：FC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC、CFC:BFGS和CFC:Intrinisic。

![](images/80c1f3eae33a236fa1ece46dff0c81a9c656e01a7187345f26ed8a49bdb5fb87.jpg)

![](images/4d05cd6ec02a9d9c0212ef322dace467fb8e1c244fe41e98d4446db6566205ae.jpg)

![](images/cbdfd5ee94fdcc46c5e6673e151686d3fd1449ab25e987679fcc5d7a3beaf89d.jpg)

![](images/9db83a44685c31aafb9e9b6ecbb762fa7eccb58c8fcc668496dd834c7817dbaa.jpg)  
图C.51：FC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC、CFC:BFGS和CFC:Intrinsic。

![](images/38ddbaa37b898564956a462d17b7261a48c1cff89ffe6edf066877e2991b0257.jpg)

![](images/319f208c9a7756e3975c306bc1e4ef9a4ac54340687bca518be9e3af46f81d0d.jpg)

![](images/e84d6b21e4960e00a4de0ab5af8111c6e2e8d0e96605eaf9c2e7eca5b44925a1.jpg)

![](images/140e74931b7550ec57e9515b64544d6f28ff05ad972e931cb3125fdcaf1589da.jpg)  
MATLAB学生版图C.52：STS控制器在DC模式下底部作动器指令和测量位移曲线（上）。STS控制器底部作动器指令和测量位移之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量位移曲线（中下）。STS控制器顶部作动器指令和测量位移之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC。

![](images/dd3e75bfd03bcf1a0d5269e3e4417af68f326c3fef30799620d7a78369de3527.jpg)

![](images/3b415b3b2f62d3b139c5b3d1070411cd936bee82a65268be832c5610754a5e4a.jpg)

![](images/9d4847f1abec2a37521d09f33c083fc4a7b3d13c52d1a7b4d73f49312305a051.jpg)

![](images/f77acbcb607ad1b0b849502d4cf3610c3e185c062e4ceb3d0895f4636b4bd3ea.jpg)  
MATLAB学生版图C.53：STS控制器在DC模式下底部作动器指令和测量力曲线（上）。STS控制器底部作动器指令和测量力之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量力曲线（中下）。STS控制器顶部作动器指令和测量力之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与CFC:BFGS。

![](images/927c37787db9673c51e083a936f139bb9906130a3ca6b3efaa64db59fa84c987.jpg)

![](images/4e5b856e13fb1f393bb34281fadebc9982f153b3dad30c10d5e36951367a6f8d.jpg)

![](images/2f22805213acceee5f34284b3ac4e0cfbd5c5ab7cf8d700fc7f82db183e31dd7.jpg)

![](images/5a870f70024e640ca9d46be6afef6d97e78adafccd3d0ccaf7d47604e5745ad0.jpg)  
MATLAB学生版图C.54：STS控制器在DC模式下底部作动器指令和测量力曲线（上）。STS控制器底部作动器指令和测量力之间的绝对误差（中上）。STS控制器在DC模式下顶部作动器指令和测量力曲线（中下）。STS控制器顶部作动器指令和测量力之间的绝对误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与CFC:Intrinsic。

# 附录D SC混合仿真实验结果

第3.1.2节中的El Centro波缩放至$40 \%$。混合模型如图XX所示。单元1为试验单元，其变形和抗力来自有限元软件层面，并随时间绘制。这些响应量与其OpenSees分析中的数值对应量进行比较。DC混合仿真中STS控制器的指令和测量位移也已给出。CFC:SP、CFC:SW、EFC:SP和EFC:SW混合仿真的STS控制器指令/测量位移和力也随时间绘制。这些仿真的结果绘制于图D.1至图XX中。

![](images/63208696a5235d1e05816364869dd1e273aa2a90d737130b38ff63c7873998fe.jpg)

![](images/13dd2831d85a1b088c74ae128d125aed87c61215bfb1789d1eb6e52ffc5eed7d.jpg)

![](images/4902fa33a617a56642b35fab4f32a24aa9dd08700d6f405a3aa80545a0755521.jpg)

![](images/d2a4548905f40ba715e3fb9e4a5498cdf2511446f7e491cf94f75f79f94252b4.jpg)  
MATLAB学生版图D.1：SC混合仿真单元1位移-时程曲线（上）和位移误差（中上）。单元1抗力-时程曲线（中下）和绝对抗力误差（下）。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NME与DC、PSC和SSC。

![](images/f1259ea84007adbe1351c2802ea2dcdfba16719da06bbb978d541ed77af0bebe.jpg)

![](images/ef8092a0c7367745d90f864145241cf56c435f79d479b50710a5f40bca0ce80a.jpg)  
图D.2：上：DC混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NME与DC。

![](images/b0e789b8afa432f0af289fd37cbec4decf4a556cedb5c797dc3a3d0b3fe3489b.jpg)

![](images/fccbc8c8abc6d9cae3382a12f1ea06cc43cfc33590f5ddf247c73c1f8d964def.jpg)

![](images/ea86137f45c123333f6e4258ab9bc2eaad34d2fbbb7047e0c13caad30517495f.jpg)

![](images/787712d66af403368fd07b809517eb6a4d1353de0cf0ede93940e3a1d60e9bd4.jpg)  
MATLAB学生版图D.3：上：PSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NME。

![](images/5e23c841988ecb769cb0708e0b4d9d15d7c6628b411309e8eda1b628e9f8e72d.jpg)

![](images/32cdc141fda33f1feda3fc87e784ed54a053378145f826bbbe6b04ba37897fd2.jpg)

![](images/f5dff89bb4de5113dca4dccd0f1a52c6d634bbf248d715874e7513bd1217eb8e.jpg)

![](images/20f61918b6d5f04319a6e9ad6d0dfe8b656b36f3181425f29bf4bf28517cdb87.jpg)  
MATLAB学生版图D.4：上：SSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NME。

![](images/4bb8711ba9808c48441b052cac3b55c0d27aa573dabfcbda7faa8355913a62bf.jpg)

![](images/2f9d223697ca5a19c2ce38ee995722d1783e6e7f32a84c6dcee03a5b7f406b0c.jpg)

![](images/64110c1e9e8383ce33cbdb967bee2b46bf2759a3c1d8813c627f36ba746a9730.jpg)

![](images/50147d2f1066f2e70530663b5b5482f920025da16af57cd5ea7641be75452444.jpg)  
MATLAB学生版图D.5：SC混合仿真单元1位移-时程曲线（上）和位移误差（中上）。单元1抗力-时程曲线（中下）和绝对抗力误差（下）。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用αOS与DC、PSC和SSC。

![](images/5fe0f44643951b803469019d18ce449a2bd331154fd99ce2b2aa3b5e52456247.jpg)

![](images/6da627c3a3bc5f85c40bb38a7f534598417b70d4cf4001fad7414ebf23016abd.jpg)  
图D.6：上：DC混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用αOS与DC。

![](images/c7ee643205a3a0aed00dcbc2266f5e3bc04d8793edb6ee8290308d4c8b0561ee.jpg)

![](images/8ae8af059cba85c629b33af9a8f04bff13d667e0335b8edf2e1e357190c81876.jpg)

![](images/f3c64cf8bfb58ed93384d728c5deafeaa4bd4fd1e1f125e0bbfb43fb451c2340.jpg)

![](images/51b3c4152f0d52f3c38ae8cc2fbc9e3f55a01a3a39a33c5aa49c05a52773469c.jpg)  
MATLAB学生版图D.7：上：PSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用αOS。

![](images/80f3954d791c71b7ed28d943472d2550a07454672c10b147e7187868029e6a51.jpg)

![](images/74502fed225efc61d896c85e4300d325f40aa08e6de7ca654547a7f7769479c5.jpg)

![](images/b4805b667e57b70c07772d902bdb345e10766c9d833a864635fc22336b6ab740.jpg)

![](images/9f7e4420f14ad8193ef79919e0558459d7be4d3d7fb6c8b95991d1fc270ab040.jpg)  
MATLAB学生版图D.8：上：SSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用αOS。

![](images/90b477e5e3d201fc888ea143b4f309fa33ae75fb0e3338f4191a8fa0759e23e6.jpg)

![](images/4a8edd22837a9aa041554e37fc0286b2395423456e5ff12989690b25c1b59346.jpg)

![](images/35f633363c7b361770b38ef14d876f8de2057d4c1b0f716da7439a75fa735558.jpg)

![](images/8fdc929cc3d263da70a2eda51fd2f65eb8ce74e510b503364b5ffb972fd83daf.jpg)  
MATLAB学生版图D.9：SC混合仿真单元1位移-时程曲线（上）和位移误差（中上）。单元1抗力-时程曲线（中下）和绝对抗力误差（下）。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMF与PSC和SSC。

![](images/3da02aa7d591c262f7f8e24ac5ffdd0b19dd94866ef900128e598da9c63d7b30.jpg)

![](images/0ef312b97153c00275f2e4314a7bed162cd179ec72ffc567066cd007ae498c33.jpg)

![](images/d78d2e900c79832b988cefad601c07cb9c01799f6d5b6f89401ea37b52bff7a8.jpg)

![](images/a713ff9b96ec262c1a5be8ae1e4c548e5fc27bde90d6773439adcc0b3c44bd4d.jpg)  
MATLAB学生版图D.10：上：PSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMF。

![](images/9ed96b8f6c5a091a44a7ddc39bd1bb815f00efb4e95d8fca8b8012a9f570229b.jpg)

![](images/9604e52315b17a29856b17fa090c7f594c2ee02c6d2966456925769725fa8a21.jpg)

![](images/50464588c11e1c18fbbc3a31331f901588e9cc39acee859885597874df9bafbd.jpg)

![](images/bb6bca437efb8cbea194d343eb30d1c1f709cd04025d710d79cb65951b8779bc.jpg)  
MATLAB学生版图D.11：上：SSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMF。

![](images/2d26d44d72c7af844fbed670cbb114bc59a9e79ccbbf19f5e360da835ec26f6d.jpg)

![](images/d7d6f1daebd6d39c196b91d793590c86de98a3445bd8c34ffadf11f0742cfc93.jpg)

![](images/685044821e5ab4f8509c7a76f8d688f595ec11b126f944d2788077af6e9c75f1.jpg)

![](images/e47c57f30eceb8321196da4cc7b51b993c604f36c980db10cc4330acd596fabb.jpg)  
MATLAB学生版图D.12：SC混合仿真单元1位移-时程曲线（上）和位移误差（中上）。单元1抗力-时程曲线（中下）和绝对抗力误差（下）。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMR与PSC、SSC、ESPC和ESSC。

![](images/840cf1c553f2f8e605c909918005d45433dfe0344ef2b116a57b860e2b439aa9.jpg)

![](images/a9bd01c1dba309eb50ec6245e1f8651ba55bbfa0103932b8b1c3f6650f19be74.jpg)

![](images/fcff3d5b9cdfd321b63cb58f08cd15f7b371536d22a8a4e243152615814072f1.jpg)

![](images/b4093d2c0be0a4666414ba17d2d06d43f2ca7d6daa5dc2a436f9bdd4147dd3fb.jpg)  
MATLAB学生版图D.13：上：PSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMR。

![](images/59fbb4ddffcdbbb709d99d58bf0074973d9f0599feb036d1c6c786aa16ab71ca.jpg)

![](images/491f4c9a0670af09821163b0dc7c30e42530e8a978614c9427e5509557d38869.jpg)

![](images/eb3fb08a1e2e9e4df53d47618763219c74a13346471d8d21c7666316309c05c2.jpg)

![](images/d947d54d07719fd9678f78f02b16e4f9ee4cc36e4a7b084a589934544ab712ed.jpg)  
MATLAB学生版图D.14：上：SSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMR。

![](images/98170fb7a7ae611674e605adb4f867a55004b482da3e4abd74c55f0891899bce.jpg)

![](images/5c13ae14f57c8d87f11f8f833715dcea560ff1e017369dead96816b8105cdc27.jpg)

![](images/4f967e89395f72fa5c5979cba2a9451ae4aebcbc5a311e5d100c4aa4409afb9b.jpg)

![](images/cd7a3ef7edb2ab741b8f801aafab5195efef23a4bc52b28a07619844398e1736.jpg)  
MATLAB学生版图D.15：上：EPSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：EPSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMR。

![](images/0195d4260b8279549d674ecb3472dc969b5ea7526197a86d7212e47c253b547d.jpg)

![](images/fd65690d906f97009916ddb52af6e14c78aa8d8410335d32dc6589e0d65ff858.jpg)

![](images/3b4484bec54f2478f8fae252b54f41a4140aa6f2701d06d6fdc52b0920880a31.jpg)

![](images/f47a57f6c24cd0fab23d4b51b8d6a983bbe8b44ac167ec02f47c903676851f2e.jpg)  
MATLAB学生版图D.16：上：ESSC混合仿真STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：ESSC混合仿真STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$40 \%$以将试件推入非线性范围。1自由度设置使用NMR。

# 附录E MC混合仿真实验结果

第3.1.2节中的El Centro波缩放至$40 \%$。混合模型如图XX所示。单元1为试验单元，其变形和抗力来自有限元软件层面，并随时间绘制。这些响应量与其OpenSees分析中的数值对应量进行比较。DC混合仿真中STS控制器的指令和测量位移也已给出。CFC:SP、CFC:SW、EFC:SP和EFC:SW混合仿真的STS控制器指令/测量位移和力也随时间绘制。这些仿真的结果绘制于图XX至图XX中。

## E.1 点切换混合仿真

### E.1.1 NME时间积分方案

![](images/1ac3c5713b9808814b9a6290927f8596102221b25da0a78d41f4a411e857e5df.jpg)

![](images/2274eec04f91d833f33d589951698ce36a2123027cf2c30b220379a3cbe78573.jpg)

![](images/800b5e7dfdf6fcde713fa504ccb51f51072c19db7c0cad50f086147beb67b431.jpg)

![](images/4bcb688b647e3c66c133d93b344abb2b2c23b8d3336d9ac1466d96cf78a4f7b6.jpg)  
MATLAB学生版图E.1：PMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NME与DC、CFC:BFGS、PMC:Broyden、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/b94b23a4f1e7f3db4a05922d792ce799c275c170020e3b408bf83a879fef40ef.jpg)

![](images/d3c3ec77261e7d64c96bf30c442fcc9ec248639d13af67901220e7d6735b7650.jpg)

![](images/e4a362b1c3593f21c62a62b3c29c3c861d2f6c35495f39b4452972d759fc2cfc.jpg)

![](images/d60bda6c2dcafd16f6c1f32d3f9dd10cc0dc8a399bfe10410ee029b3aa0874a3.jpg)  
MATLAB学生版图E.2：PMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NME与DC、CFC:BFGS、PMC:Broyden、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/8c72d56c70ee9c56510bee11c1a2ba250a2be259081286fee525a077c20dab08.jpg)

![](images/4b1ac6deefdaa3f9f3028ecc5c2fedaf7c565410ae747a22c2b37d83f8109b74.jpg)

![](images/8bf356c6309ac3077ca1580447876e384e9a6e9e4df8249f98f6c71a57f8035e.jpg)

![](images/565cf1f6969c047b8aef962b17a79686d2291e559ec7f914bafabd9fad0eb86b.jpg)  
图E.3：底部作动器STS控制器记录值。上：PMC:Broyden混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与PMC:Broyden。

![](images/3e8d8c9b40c97d444dd890ad866f330264fc58e182f55f3cf3282831620272a8.jpg)

![](images/de5e4520f760515289e9712eb87c9aa5a47833e79f62b45c0f7c88a20b0fdf39.jpg)  
图E.4：顶部作动器STS控制器记录值。上：PMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与PMC:Broyden。

![](images/147e354c49c2d8be48cbeebf6cde0beb0679bbd29cf3a5c45144dc9c90fe06d0.jpg)

![](images/bfde58144554fbc1683a860ba14792100bef1a6837f0b01ac1d7219823f2ffb4.jpg)

![](images/c8100e4af28cebde7c3362cefbf690c4b08abae83da5908995ab2097b67a9758.jpg)

![](images/a7d59a35d0b42c91973edca75cdbbaad7f3fbc0d174e4e9fc56aa002d9225bea7.jpg)  
图E.5：底部作动器STS控制器记录值。上：PMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与PMC:BFGS。

![](images/25179399502e730fccd3f0c3f15a8caa23ab3762f052643666e83d597a1f08b5.jpg)

![](images/f2a8592209cde989cdfd03c2562d685219b9adeac8530f4affdb094519e6181a.jpg)  
图E.6：顶部作动器STS控制器记录值。上：PMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与PMC:BFGS。

![](images/8dfb0148f984ab2a64b392148857dea0870a29f0aef129e92bf7b5c21570c1bf.jpg)

![](images/eb2b29a3aa61d840b6939016bebc680329c23e9d62a4891eda81635e1f8b67b9.jpg)

![](images/a8437ff6cfab6090e12a844b3940504f1c090bf36e4ca31f10a459f7e7202d27.jpg)

![](images/bd45eca2b7b2eeb7313debd787306e135a413649a821a1d17d7f98ce97deb59a.jpg)  
图E.7：底部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与PMC:Intrinsic。

![](images/416f2cfff18a7f5aecd92e5bb1dc26cc0f6c06059743c9e3becee9551cdd356f.jpg)

![](images/85aab20b06a61700b56a4a8c70064375b1283e7bb360d2ff37426de0232a732d.jpg)  
图E.8：顶部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与PMC:Intrinsic。

### E.1.2 α时间积分方案

![](images/73b0e36840c1a7a9cf9e04298ef030a0742b8558391c4babea3716d6e351c94a.jpg)

![](images/481bedb80a1f811310837f4723404369b18908b33fcd504e5768146c61c20e11.jpg)

![](images/5c84da210ded8c2aeb2a9c5fd307ad5cf05a284d2c5559bdfc92422254b352fb.jpg)

![](images/cf62e78fed16e6bfad0ba1197a4876bb9024d7720e145ae664a41b05850cce98.jpg)  
MATLAB学生版图E.9：PMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC、CFC:BFGS、PMC:Broyden、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/41e65cd73e611dd0f8ca14ee0604dbd813bb091edeaac68a54e46411bd6d5771.jpg)

![](images/92fc175f5ae5e5b39d58b460a6cb8eff7b0d9fb46f5e25f9fe110ccf24b14c2a.jpg)

![](images/13fd4894e91a7b301c66c2d01c920b6685d0a079734a17b9abaf217649ad273d.jpg)

![](images/9957a26b33bfdaf1cb49e5267d2f28d9dd708884f73c56c1e596c0e376a8287b.jpg)  
MATLAB学生版图E.10：PMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC、CFC:BFGS、PMC:Broyden、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/5fb094a66cd466e03df82e21e484603b8374c116bb038d2cfcb730446b9748bd.jpg)

![](images/6925946053a231376b4e118ea12f8924834dfee1955c83a90f0d78f0b572aed9.jpg)

![](images/1c70521b0066db4f2068f71e94ca0b122526636932757c632e1a5ae342ca8e0d.jpg)

![](images/0b191f1131bdd66fa0994b7ce22a153ac10c912d67c23f46834db62c7741a10f.jpg)  
图E.11：底部作动器STS控制器记录值。上：PMC:Broyden混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与PMC:Broyden。

![](images/cc35bdcc58b111fe0c23817b23e5d4b22c89dd820b0febc060428feba44aca6b.jpg)

![](images/3c355faae72844e8b0ef1627f92f962d4d322bd1c068b27846260076f63bc503.jpg)  
图E.12：顶部作动器STS控制器记录值。上：PMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与PMC:Broyden。

![](images/fbcfda2a94710772363ee4187a0671fd33eb3c8d917d8495337c3e520dbdaf9b.jpg)

![](images/260cf53ba0209a70fa921d6a79bb9ac33bdeca23c0597484367cb48ebaf3d1d7.jpg)

![](images/24283bba9f24fedf4e25687c19a7bd06cae098cdeaf2fd37abea2d2fb9639929.jpg)

![](images/977dafac2b7df755171cb45be1dcc07cd88a0aa2f0259532525e77b95f865693.jpg)  
图E.13：底部作动器STS控制器记录值。上：PMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与PMC:BFGS。

![](images/af14f16a42aa7d1cc2a4b2f0df0c6244830ab186f9783ed0ae8627627f1ffae0.jpg)

![](images/f7c4193e273555f77d9d452600320396132144ca9acb41bc3f650e9ebb03306e.jpg)  
图E.14：顶部作动器STS控制器记录值。上：PMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与PMC:BFGS。

![](images/1943ef8f8add704b59ed478b5ce1f33d49e8945193bb9b2f21aec408e21ee7f6.jpg)

![](images/73ee27714b67693e7de6a3136a398eb7514b98c43193fa2dddc444ea184be981.jpg)

![](images/7c3862bdb15d9a5b314b759b7fbea1ac32dbbc78ef3a12deee25064f90761ded.jpg)

![](images/979c76d04c89951e1f8c24ff7e43de0aaa41fd20b527b2d7a06939d0ca90a4ec.jpg)  
图E.15：底部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与PMC:Intrinsic。

![](images/94ce4343ac88dfc6b1ff35d45d161a70c06742b569a1b6d1699d22b090d224ac.jpg)

![](images/7f439c814265892cb3ed50e268e1ffd2c85f8d7aaac17a613801a97592cd292f.jpg)  
图E.16：顶部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与PMC:Intrinsic。

### E.1.3 NMF时间积分方案

![](images/7e4929ed6d6f3296f77da6fedcaf997c97a6c94698a523c0da0aa86b5fa09ae4.jpg)

![](images/233ead67e235aba3f7bcca69e4900d68457a6e8a05cd7a756b5476f41da89e0e.jpg)

![](images/a6a2cf8f596bd2ed7301db1e1799c342bf973cbef4a3ddca67c48559d99527e0.jpg)

![](images/5739fab0f899e86c656a2c0635da603683523807a70c4f30d229507ccf40aa84.jpg)  
MATLAB学生版图E.17：PMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC、CFC:BFGS、PMC:Broyden、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/d9234f9a7f04634d0a7323b0b9f1eaf1de23e7e151db22f7feaa258b15c466ff.jpg)

![](images/91a9a116752654163f429ac2bd82ecdfba820134fb9ca3134cdfb7e809ce9273.jpg)

![](images/617574581524fac3ae9e490e7734d9c416e151d0cc6378b92d0db9ab20af0dac.jpg)

![](images/2688268d91604ccf2266f4d9f8ced58d04736d0a37c5f2464443a42cb19deac6.jpg)  
MATLAB学生版图E.18：PMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC、CFC:BFGS、PMC:Broyden、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/8f625e4c48b06e6b4eb7de56ed5cdeec1f149c40ce51bc0862045a82d3dcad44.jpg)

![](images/0ffc50b0e8b7e7bbe980e1b756daf23b7a09ff275488c5631e87d53069935bf7.jpg)

![](images/c2da30bf88eb69abb667d699a972de1babfccfafa7a51d80393abbe50bf3c131.jpg)

![](images/66129dfe40be11316a15962a088f235ef9535cb1ae247c853e22c1323d780496.jpg)  
图E.19：底部作动器STS控制器记录值。上：PMC:Broyden混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与PMC:Broyden。

![](images/a2ec71b110911cf044ab5ec1d0d217974d11f6885b5666e44bd57fd7cc06edd5.jpg)

![](images/2194eed12be9f82709ab6dedf6e8efffdfa81d022857702bf14148597ae5fdff.jpg)  
图E.20：顶部作动器STS控制器记录值。上：PMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与PMC:Broyden。

![](images/c3ba58de40917e05ba428f97d409e5b5a460980dc931c418dcd20f71d9aad1ad.jpg)

![](images/b3478b92cb25faa13fcb9f4fc198d51c485d4aa1ca27f04419def64f9fd1daf0.jpg)

![](images/edbaff7c7e278aa84980ad85be06891086c34f6f3fa5e22154077112c9bf47fc.jpg)

![](images/cdf7f5762a2b9aa21e67df1b4d87fd6f8934c813b327e7e525ae21476a4db615.jpg)  
图E.21：底部作动器STS控制器记录值。上：PMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与PMC:BFGS。

![](images/e67972971ff74a3032f96a082da249d7caad4293a2cbcc2c73939d10be18596c.jpg)

![](images/6b625855c7461679c295579b872f94560804ad29f0a49a0b4d26ff926e6c7273.jpg)  
图E.22：顶部作动器STS控制器记录值。上：PMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与PMC:BFGS。

![](images/9adc8d5b44a2eeee51b25aa20a1b0356430cad0420ab3af46832ad6d7ff43e9b.jpg)

![](images/068bfb7d10f7415e9c0e98832d5cee76d76db3b88f7b0546bb6d046ad8674bca.jpg)

![](images/f9e36be36260b260d76ed40ef65637a56cd14b120f487d593010d9103bff19ea.jpg)

![](images/6a705c6cc3558cdc6200d6edf316408468850f488c44aca5e0f75fcc9b6ad501.jpg)  
图E.23：底部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与PMC:Intrinsic。

![](images/ed726e19a08a7767841c89f53d599a3ba3445131e8c5bba81d1a70ed0a240e05.jpg)

![](images/95843494d012c418c1a00ca35a686eb51d0b80f6bfe10b52701dfdd68b3a68e8.jpg)  
图E.24：顶部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与PMC:Intrinsic。

### E.1.4 NMR时间积分方案

![](images/f40e61c851c9432b1f2885aec4e01f374ebbab600759d9b3f3b247f30cd7823a.jpg)

![](images/682f0976b3311f7a21e80bbfd5c8060b24880ab8303e84014135b32a8054a31a.jpg)

![](images/b86597553aecdc3ebfb80dd84daef080501cb1fee40660367271852c905f747f.jpg)

![](images/4909ed1eb933960f6833c3d4c4d4c08a36a59d7220e66259f09cac646e940451.jpg)  
MATLAB学生版图E.25：PMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC、CFC:BFGS、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/ab2d91810014763376defd48c55e448bf9e197c891c19b54f3539cb8df47c71e.jpg)

![](images/5e8c388a5e6f9e8a8bf968720bc60df12efd49d22f680ca6751f185f142ff602.jpg)

![](images/e6a51c59cfc591cd012e749e7fd454941978fca08bd31f6f4813f5059673a2e6.jpg)

![](images/182887d99f71ca3a52d709d84607955f5150dc1282c19ff10b0f8a91b09f6769.jpg)  
MATLAB学生版图E.26：PMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC、CFC:BFGS、PMC:BFGS、PMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/40667b5b241d12667d542539edb54a8da160e5ca63921ed706b4e1c78400a3a1.jpg)

![](images/ea616b37d6d6804169057db969c24e3dfcfa2c15e073e6a71a5c95929d9f6abc.jpg)

![](images/01c0493ad4fb37c906e6bad98ad347c5923909cfc42f17df58e38081e245a8b8.jpg)

![](images/20637278698dca2dfb67e0fbbae059395d34d9b12a18e4780057adc3e31096d8.jpg)  
图E.27：底部作动器STS控制器记录值。上：PMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与PMC:BFGS。

![](images/629b492356ae1494d4c117a75ee41521c8c797e49b76b52b00814008e61efc8f.jpg)

![](images/22b32a33ff2af374cfa0beda498b0c2978796c15a2053dbc83749d22617a526f.jpg)  
图E.28：顶部作动器STS控制器记录值。上：PMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与PMC:BFGS。

![](images/1156e53d75a1d36ba6681d0619404de5b24345ca08e28424ea6411f0d531c561.jpg)

![](images/aea800d4a938a70a5f011601227833b1fb6645623ebde750180c000c2e1a8ada.jpg)

![](images/df81c705f4f80999c822497782e26813cf98821ff158f1b75578f38d97a251d.jpg)

![](images/dedae2797715557d41b12322deb88f88720fc0f8c419ad7ae6be512b5ef2c892.jpg)  
图E.29：底部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：PMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与PMC:Intrinsic。

![](images/44f0787e7a908519d9c6922d344a05082ddf4c4bb66e9e58081500c3fa0d2130.jpg)

![](images/9806a1e399695c258d4af5adb464ffa7fffed0761a28c96e761ef774fa4cb123.jpg)  
图E.30：顶部作动器STS控制器记录值。上：PMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与PMC:Intrinsic。

## E.2 割线切换混合仿真

### E.2.1 NME时间积分方案

![](images/a3e9bac6ff86d38ca3d5fcb07f559f3732422277569b8a8493998aeed16acae5.jpg)

![](images/2bbdb0362868dcb0a5015e0e98c75bb9e0f15e1df1b2ac3c607d34e8943488f8.jpg)

![](images/b0e4bc182860c555f64359d17b807d2c3977739903ab6573facec7b1f2e77d8c.jpg)

![](images/44f6b50deecb2d0ee56ee7f1bb8526f017d39583b9d7450e74afaf8d4e2e703e.jpg)  
MATLAB学生版图E.31：SMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NME与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/c43a0ad807287f6cc2663f9eb9dcd6db6219904f95644ac2b53b263b52bf6ad2.jpg)

![](images/21a5169d43c5d9d73f5a5d906ed9f677cb1bce9316f318b03638dc96a9d9e5d0.jpg)

![](images/0ff8e5a22fa7fc52e512383252386bb54f7928e7af96bff6d38e535ea0d92757.jpg)

![](images/4f7d03b182808cc0e91e172343be5caad13c3734d1f252c0e17e1e7ffb637b7d.jpg)  
MATLAB学生版图E.32：SMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NME与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/d7870ba553bf33a1f31d03d18bccdae2ac79be6577a079b08769ff1721e280e6.jpg)

![](images/8a5a16ac9651a184eeb0a5a434d049309a399d7b96b78b39cc8b7f359fcfa43f.jpg)

![](images/4ed014b72b501e3000eb5ffccc1de42c511a1e277567df83ee4f912a9e9f64b0.jpg)

![](images/bdbd1fb3c96ec2e8a4fae0484e6c7e4a79283e4758f020aed077a2e92fb24082.jpg)  
图E.33：底部作动器STS控制器记录值。上：SMC:Broyden混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与SMC:Broyden。

![](images/80868ad0d0f88c751aa366a453cf6160a2541de8eb3e2cc6df398a554873c4c2.jpg)

![](images/3e738156de649888e51f48aa86698d3bf2d6d57a314c6f3bad5e748f9f5b91b4.jpg)  
图E.34：顶部作动器STS控制器记录值。上：SMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与SMC:Broyden。

![](images/31ec4bd18a4049c7780f3b6effbc4687657023f222393b27ce760469d8474e96.jpg)

![](images/f8e30ffa59f0ff3e384551974c9aebfc539f28ad602783622a31b2050076dada.jpg)

![](images/0a44fd3d7de2c7c6056273d993f1651f783aae4c4ace89f477e444d541714cb4.jpg)

![](images/b1bab3dc0ad6010cb83d7577c30934b6075ac8b62fc1fe749995eca30a311e1a.jpg)  
图E.35：底部作动器STS控制器记录值。上：SMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与SMC:BFGS。

![](images/438de42924383e197fb9222be83023ed2805dad4fd265893cbaaa1329768c911.jpg)

![](images/cbd804c4c66d0f5e9d943bc4428adb472e426485c853719738a3fcf3a464629.jpg)  
图E.36：顶部作动器STS控制器记录值。上：SMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与SMC:BFGS。

![](images/0302a7cb1b086125b06b127fef3dafbe29abaa498648e1f515a465cf3c3f5b3c.jpg)

![](images/5fa3295480ea119d0a3060aef306ab109c661cd1d6c6563f9567e5e254c6abc7.jpg)

![](images/72e608987e31009563c76e3d6fbafa8f102775cbcc186537455d9e9275015ba6.jpg)

![](images/e79aae6cf279fa5aee01a9d65641afa0e4019a3c5bba62993969f6676c0cce02.jpg)  
图E.37：底部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与SMC:Intrinsic。

![](images/e72c8e0d6597edaac16d3b18d263e207f8829adca33580813195aeb0e75d3ca3.jpg)

![](images/249df55b2c0009c8ecadde6bd3498e6f4bfc2d0c1b7d4640a43ce2ca46234b0b.jpg)  
图E.38：顶部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NME与SMC:Intrinsic。

### E.2.2 α时间积分方案

![](images/420ca623f14e09f1126b1a7a789f9510cdfef704e8b360939dad180d51581a35.jpg)

![](images/a568a10805ac59ddc064d41f8705f653d93e858645ae953cec12b1b85e2129c8.jpg)

![](images/3868f8b27eb9056b71182791b548b1750c6fee3004604d862e531a741d731792.jpg)

![](images/ebd90d0f2a2fbf83031819e295c5a4db2c8a7271404ee616134bd7581634d9e0.jpg)  
MATLAB学生版图E.39：SMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/41131f3841435844397bb1ff04f6a8416df2c3333d10a0af01ef9df3dcd8e463.jpg)

![](images/40344213cfb3759d598541ac09de953951214c2e112d8aa25136522ee16065a8.jpg)

![](images/609d98fe3cfc1b348feacb1fe39779cb10904550c40ee32a1a052ff7b4a5c3bd.jpg)

![](images/b3567e815269b0da3c86541b9076331af2bc603646917ead14f882d2d8e7de31.jpg)  
MATLAB学生版图E.40：SMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用αOS与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/2efd1a7384d0b08027cbdaeccdce8e6ac89272636f77e42463e5d1888828a8f3.jpg)

![](images/f7c69a575fe0db15bf734e63ce213d073c7ee96726575dad2c16245a3526bd30.jpg)

![](images/12fb2ea9c9d3221e47ac8091a1b191eb9a38b76517be3c33bbecab10d93fed5b9.jpg)

![](images/467d5ead2b8641830214141cc7fb93c4afe3b64d37cf5734fc332cb62746320b.jpg)  
图E.41：底部作动器STS控制器记录值。上：SMC:Broyden混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与SMC:Broyden。

![](images/3e41fdf21ef3792ef7d8c989648f51be04ff50b526eccfec6513013df85cbf14.jpg)

![](images/97c95a4843723275011c284d84c76e42988675b01c2e0c30151864114ef01107.jpg)  
图E.42：顶部作动器STS控制器记录值。上：SMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与SMC:Broyden。

![](images/dbc2c04eaaabc1bb40ef396482039b50e12cb3435d40ffaa77270e89092aa78e.jpg)

![](images/a04473dbc0ac23680227c6f4a46da79c586541b348c3edc6249225395e001fc1.jpg)

![](images/55427662b917cbd6f0666bf40542d4b2fe0fd7d7896461706a86e4f69c983999.jpg)

![](images/23917b962b9ecba5c0395140b2b81b4211b50ef001da61697544594df6737bdb.jpg)  
图E.43：底部作动器STS控制器记录值。上：SMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与SMC:BFGS。

![](images/ed82a72270f38aff0f324fa185871c98ab2f042e176360a9162c88627b6f0511.jpg)

![](images/f63215e0fac603be1c6414d33cc2e3627019e64c0bc4041a13bfc2c879b79621.jpg)  
图E.44：顶部作动器STS控制器记录值。上：SMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与SMC:BFGS。

![](images/9ebffe33e80590ec2779abfeacf208b46d6c936c5f6403f59add7bc0afc80dd3.jpg)

![](images/487375679cd0a103d4d4851fee71df8bfc38628b4be93f14282356731dfa94a5.jpg)

![](images/3be101c1389b5971909d7d0e97a8b39913ba30032cf3bfc8963a6ffa8d3d14bb.jpg)

![](images/468d76434bc76ababc0030c88e3f68016e608ef3ab4da1bcb4f43d918e8a6516.jpg)  
图E.45：底部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与SMC:Intrinsic。

![](images/94c46cc75c5d1c15c0935b29a9d2a9107e9f4badff8b6f4d7b31f89baf2cf0a7.jpg)

![](images/337427f89c68ca0352c8e6dea68463e71cd33970b04fc7fc312a4149dfe8038e.jpg)  
图E.46：顶部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用αOS与SMC:Intrinsic。

### E.2.3 NMF时间积分方案

![](images/088241c534ad98390028b3e129762ae6a6e87f1ad14d45803afb4cae3f7f446d.jpg)

![](images/6d95b24aee03c7e983f4c9d6418b08df7020cc5242751893e67d267f6da5a180.jpg)

![](images/dc8eb1f3db11d78dd215fa2c2829c168433af69e1655b697709dc30c1969d6eb.jpg)

![](images/be8e1273cb35003c8f963a4cf782c36072ccdbb843487d828a72685f307af3eb.jpg)  
MATLAB学生版图E.47：SMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/51e664670daf2a335d6e9c97f193293ac97943f8e13d35647a5c519620b1f63e.jpg)

![](images/61f266c2cbe5390750d2caad035eba839228f188b6037f2aa70d6f66157b867a.jpg)

![](images/accde5f9e31c0279a70c31ded80fdf42f869f2723a1e2dd48c8b9a630ca7b2af.jpg)

![](images/431435d2a0a492da68230eafb69201f5f6f3b6cd58fc1584fbe015f01deea3f1.jpg)  
MATLAB学生版图E.48：SMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMF与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/2a6f24c18f026edf8cb56478deb90c0ab4cd258eeb0c60d4821ad7528594f722.jpg)

![](images/c820882850bf8f7edc4f4bf30a93339216b4bb8dc3d506150487c39beb3be751.jpg)

![](images/01a94808f01f34859638dded8178c89e209e40274751420eef772b929f193ee0.jpg)

![](images/f9138a8496d2d43269f518959fcf04f04941268db8e4f19c7fc0983d7c542fcd.jpg)  
图E.49：底部作动器STS控制器记录值。上：SMC:Broyden混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与SMC:Broyden。

![](images/754b09c27764d74ba498438627e6dcb35d27d83db573ba6a443f34e22961009d.jpg)

![](images/807d4952c3e995b7c2468e5cf1648bfa27a26a8efc49d936cb625739aefae9c5.jpg)  
图E.50：顶部作动器STS控制器记录值。上：SMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与SMC:Broyden。

![](images/0457ff1e1d7257f58818f03a72325786af1117dd4d6d760a8737de70e97479f6.jpg)

![](images/98408e5ca0881c315e89a7cf99228201c3f0b1c517b27eff3df9349fc2d3254b.jpg)

![](images/00171f420f43749c9cbf3e1e54ff64621a46c9fcef802e8e7fa7bfe486eb9b9fe.jpg)

![](images/802aca16e7a88ce9ce8f08dac3060e7788a638e53fb155c426cb7d05162fec06.jpg)  
图E.51：底部作动器STS控制器记录值。上：SMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与SMC:BFGS。

![](images/4009195a7e3c4941f487a143feb4ec8d79c3fa7c6212fa0191ee12fe8e009800.jpg)

![](images/d5c8423eae8698024d4b1c8a3285a8bd7e52853ce1aef67cb761572feacae95c.jpg)  
图E.52：顶部作动器STS控制器记录值。上：SMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与SMC:BFGS。

![](images/82dade22dfdfdd31242a3988d95736385516da583638aa39f886936a9ae8dde4.jpg)

![](images/32559e4f553893fcb3b38a07b125f7c787d0e9c809322c6da6e2ab2a9776e86a.jpg)

![](images/dee2a672b64a2a743f65ae30d73d5df5ac929f20ee8dfa154c255e02308627b0.jpg)

![](images/6ee328980de35d745b9dbaf718b3a3fac6ffa43a438ebec2398674957d31cec3.jpg)  
图E.53：底部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与SMC:Intrinsic。

![](images/0789789d9af191c65b3004abff94916f6cb9c2d3e91253be10c4c77f7379dc25.jpg)

![](images/1b6bfc531848e6cc32ba2b445fbf34734d63e1fad970d4e2c1f2038445a61e4.jpg)  
图E.54：顶部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMF与SMC:Intrinsic。

### E.2.4 NMR时间积分方案

![](images/165ddec5037f3c819e48cfdfba7ca5a6675266f6bbab4e17570affc1e74e637c.jpg)

![](images/4d796cce87eb1cd6951b8f99fae5a487c4401e071ed5621232579009798d9107.jpg)

![](images/abcf246e90987bbe79c1e7bae5c386c880830943bc5655fc55c0ff33ef944f5a.jpg)

![](images/1e618ad7012d9c5ad81214851f5b3cbd11e331cb61e584e9a2e3fe3f8f4ec40d.jpg)  
MATLAB学生版图E.55：SMC混合仿真节点1位移-时程曲线（上）、节点1绝对位移误差（中上）、节点2位移-时程曲线（中下）和节点2绝对位移误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/8b37b6571873212402a55ebb86461b39964a849da590d335c3e00e3772729de7.jpg)

![](images/87694546ebc345d2ebdb7d79c297fabd582a1600bef976e578b48bba93ea7a23.jpg)

![](images/05071af5be1255168b74e718a17949c0371abcbb073a4f7328907510cd0d781e.jpg)

![](images/3f9a92ffac6b8f1a61bc9cfce7e3af112fb376147ce0361d14d665bbfd2d5376.jpg)  
MATLAB学生版图E.56：SMC混合仿真节点1力-时程曲线（上）、节点1绝对力误差（中上）、节点2力-时程曲线（中下）和节点2绝对力误差（下）。地面运动缩放至$50 \%$以保持模拟在非线性范围内。2自由度设置使用NMR与DC、CFC:BFGS、SMC:Broyden、SMC:BFGS、SMC:Intrinsic。所有试验结果误差均使用NMI数值结果计算。

![](images/31d67cf9e34f0cee51493d17cd7e261868c96c2a6717b2de42c34433071873e6.jpg)

![](images/3c156969e25e6ca97ae7bb061600f6058a7311168def8753a700cb37784928fb.jpg)

![](images/60efbfeee087c746c60af11b022d18ad5523cfa1e05e8d07f508adb09cf7be7e.jpg)

![](images/56c152f6a69632bd9c8c31327b6d7f041abb65b3f0908c3981d5d53adc216e7d.jpg)  
图E.57：底部作动器STS控制器记录值。上：SMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Broyden混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与SMC:Broyden。

![](images/c0d6ab00444a0f019af6562e5b98c44ea05baf46293f1ea1110047557bc35779.jpg)

![](images/a96c6953f67e2d0fa5b6492b6285e32faf5ed25ea3e99a08c308a9c8b449a5b5.jpg)  
图E.58：顶部作动器STS控制器记录值。上：SMC:Broyden混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与SMC:Broyden。

![](images/e2029fedfea34a6edac15efa18a99a6a4a466755b843898325455f76eb8393a9.jpg)

![](images/e8f69e4dd512930367af171d54d7b1e6525afa7eaf7ba3553ca71b461a177457.jpg)

![](images/c89d688c22e095c9360ce8360069c437de5c0a1278921db995e4fbcf7595d1f7.jpg)

![](images/e2c3d444461d9e5304978090f7083a6d2f988094bff74455e5060e2bb57e9225.jpg)  
图E.59：底部作动器STS控制器记录值。上：SMC:BFGS混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:BFGS混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与SMC:BFGS。

![](images/1b33fb24ce93a84b0c05ed39d6e7216656a2ea5ee286c850a29860ae510a2f6f.jpg)

![](images/0f70ac2f1cd958b2e7eacde57ebcbe352813549fd81b71c32253e8d75f51ed7b.jpg)  
图E.60：顶部作动器STS控制器记录值。上：SMC:BFGS混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与SMC:BFGS。

![](images/3efd3f668082bf08a606a5fe1f41d92e2ce55d3c4d83de2a922b45d3131d9b00.jpg)

![](images/268745590e261d4659dd88509b1b73797d97bc9a8f2b4657b08e7c3bf4af42b0.jpg)

![](images/e3113d05c3f0d39b631331f26d7731889aa61fd8eee5c3372a0cfcc5ea3e598f.jpg)

![](images/12f8e5bcd58fe7ecd592c1b25922b196f2304bf2b29482c1c1dcc6ed91b04a4d.jpg)  
图E.61：底部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真DC模式下STS控制器指令和测量位移曲线。中上：STS控制器指令和测量位移之间的绝对误差。中下：SMC:Intrinsic混合仿真FC模式下STS控制器指令和测量力曲线。下：STS控制器指令和测量力之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与SMC:Intrinsic。

![](images/384c159c9d59c070898ff973498ff9518dbc239a6be683aa7a6c2e845e5ea49b.jpg)

![](images/a8c36997a119ce7250c6527c3102ff4d80cefc26bed6a91b5386db02627e666c.jpg)  
图E.62：顶部作动器STS控制器记录值。上：SMC:Intrinsic混合仿真STS控制器指令和测量位移曲线。下：STS控制器指令和测量位移之间的绝对误差。地面运动缩放至$50 \%$以将试件推入非线性范围。2自由度设置使用NMR与SMC:Intrinsic。


