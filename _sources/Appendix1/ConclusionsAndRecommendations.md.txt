# 7 结论和建议

## 7.1 总结和结论

本研究的总体目标是探索、开发和验证先进技术，以促进研究界更广泛地使用本地和地理分布混合模拟，并使混合模拟能够解决研究者当前感兴趣的一系列复杂问题。为实现这一目标，进行了调查以解决以下目标：

1. 审查和评估混合模拟中的现有概念和框架，并设计实现改进的对象导向软件框架用于实验测试。   
2. 调查现有时间步进积分方法，评估其对混合模拟的适用性，并为几种方法开发和实现改进版本。   
3. 检查用于同步的现有预测-校正算法和事件驱动策略，并构思和实现新的和改进的方法来同步积分和传动系统过程。

为完成这些目标，研究工作安排为以下活动。第一项活动是进行广泛的文献综述，以确定混合模拟实验测试技术的优势以及过去和当前的挑战。此外，全面讨论了基本概念和混合模拟的不同执行模式。结论是，缺乏用于混合模拟实施和部署的通用框架已成为那些考虑利用混合模拟的人的主要障碍。此外，它也限制了该领域专家之间的合作。因此，第二项活动是设计并实现对象导向实验测试软件框架（Takahashi和Fenves 2006）的一些重要扩展，以支持各种有限元分析软件、结构测试方法、试样类型、测试配置、控制和数据采集系统以及网络通信协议。由于在混合模拟中，半离散运动方程的逐步数值积分充当计算驱动器，第三项活动是检查现有的混合模拟专用积分方案，并为其中几种方法开发改进版本。虽然第三项活动侧重于混合模拟的有限元分析方面，但第四项活动涉及调查混合模拟技术实验室方面的控制和数据采集系统的方法和策略。具体而言，开发和比较了用于同步积分和传动系统过程的改进事件驱动策略和预测-校正算法。第五项也是最后一项活动是开发和执行一些新颖和示范性的混合模拟，以验证软件框架、积分方法和事件驱动同步策略。下面提供了每项活动的简短总结以及关键发现。

### 7.1.1 混合模拟基础

为开始调查，表明在目前公认的实验测试技术中，混合模拟能够提供一系列重要优势，但仍面临若干重要挑战。解释了通过混合模拟获得的一些主要优势是解析定义的加载、子结构能力、测试大尺度试样的能力、使用经济实惠测试设备的选项、可变的执行速度以及地理分布数值和物理子组件的可能性。另一方面，讨论了一些仍需要解决的关键挑战。这些包括实现与环境无关的混合模拟开发和部署框架、探索力和混合力/位移控制策略、处理地理分布测试中的网络延迟和中断、开发评估混合模拟优劣的方法，以及在高性能计算（HPC）环境中执行混合模拟。

以全面的方式列出了执行混合模拟所需的四个关键组件。它们包括结构的离散模型，包括静态和动态加载；包括控制器和静态或动态执行器的传动系统；在实验室中测试的物理试样，包括执行器可以反作用的支撑；以及包括仪器设备的數據采集系统。

总结并讨论了混合模拟最常见的部署模式，如本地与地理分布测试以及慢速与快速与实时测试。本地混合模拟由所有必需组件在一个测试设施中的并置定义。相比之下，对于地理分布测试，一些或所有参与站点是分散的，需要通过广域网连接。此外，注意到由时间步进积分方法求解的运动方程将根据混合模拟的执行速度而采用略有不同的形式。

### 7.1.2 实验软件框架

从文献综述中发现，尽管执行混合模拟只需要少量基本操作和通信协议，但迄今为止很少有人努力实现通用的、与环境无关的软件框架，用于开发和部署能够执行混合模拟的系统。解释了软件框架是系统或子系统的可重用设计，并定义了此类系统的整体架构，即其基本组件以及它们之间的关系。

根据此定义，重新设计、扩展并实现了现有的实验测试软件框架（OpenFresco），以支持各种计算驱动器、结构测试方法、试样类型、测试配置、控制和数据采集系统以及通信协议。此外，为加速混合模拟的开发和改进，OpenFresco被实现为与环境无关、稳健、透明、可扩展且易于扩展。描述了软件框架的原始开发如何基于结构分析方法，其中混合模拟可以被视为传统有限元分析，其中结构的物理子组件嵌入在数值模型中。使用对象导向方法和对混合模拟期间执行的操作的严格系统分析来确定OpenFresco软件框架的基本构建块。

先前已引入四个主要软件抽象（类）来表示执行混合模拟所需的实际组件（Takahashi和Fenves 2006）。这些类是ExperimentalElement，代表在实验室中物理测试的结构部分；ExperimentalSite，代表进行测试的实验室或进行分析的计算站点；ExperimentalSetup，代表传动系统的可能配置；以及ExperimentalControl，提供与各种控制和数据采集系统通信的接口。

这里提出的研究的关键贡献之一是多层客户端/服务器架构的应用，该架构包裹在基本OpenFresco构建块周围。作为这项工作的一部分，在将OpenFresco核心组件与多层客户端/服务器架构组合之前，对其进行了重新设计和新实现。展示了新设计如何支持任何有限元分析软件作为计算驱动器，并促进各种本地和地理分布测试配置。此外，详细解释了这些不同的部署模式。因此，可以得出结论，OpenFresco新的三层和四层架构模式提供了将一台或多台机器上运行的任何计算代理与一个或多个实验室中物理测试的试样相连接的模块性和灵活性。

使用类图、类API和序列图（软件开发的常见做法）总结了对象导向设计阶段产生的最终OpenFresco软件设计。之后，讨论了作为此处工作的一部分实现的所有具体类和分布式计算和测试协议。OpenFresco源代码、文档和示例可在http://openfresco.neesforge.nees.org获取。最后，展示了如何使用OpenSees作为计算框架。发现可以实现比其他有限元分析软件更好的性能，因为两个软件框架可以直接集成，而无需利用网络连接。

总体而言，可以得出结论，重新设计、扩展和新实现的实验测试软件框架非常灵活、可扩展，并且能够与各种有限元分析软件接口并支持大量测试设备。因此，它将能够促进混合模拟的开发和部署，并促进该领域专家之间的合作。

### 7.1.3 积分方法

在成功重新设计允许任何有限元分析软件连接到实验室的OpenFresco中间件之后，目标是调查执行混合模拟所需的另一个关键组件；即，充当计算驱动器并需要由有限元分析软件提供或实现的时间步进积分方法。

从直接积分方法类和Runge-Kutta方法类中广泛调查了一系列积分方案，并根据其对混合模拟的适用性进行了评估。这些调查的第一步确定并总结了混合模拟可靠、准确和快速执行所需的特殊积分方案特性。结论是，显式非迭代方法非常适合混合模拟且易于实现，只要能够以合理的时间步大小满足其稳定性限制。相比之下，证明无条件稳定迭代隐式方法应仅在以下两个条件之一用于混合模拟：要么在平衡求解算法中使用固定的用户指定迭代次数，要么需要另一部分中介绍的事件驱动算法自动调整施加位移增量的时间间隔。对于前一种方法，开发了现有算法的改进版本，在迭代过程中实现了卓越的收敛。第三，证明算子分裂方法和Rosenbrock方法，它们无条件稳定、相对易于实现且计算效率几乎与显式方法相当，是混合模拟期间求解运动方程的绝佳选择。对于算子分裂方案，提出了两种新方法，广义-alpha-OS和修正广义-alpha-OS方法。对它们进行了详细描述，并得出结论，只要混合模型不表现出严重的几何非线性，这两种方法就是混合模拟非常有吸引力的积分方案。这项工作的另一个关键组成部分是对Runge-Kutta方法对混合模拟适用性的彻底调查。

还根据两种度量评估了所考虑的直接积分方法类和Runge-Kutta方法类的精度：数值耗散和色散。结论是，对于混合模拟，积分方案最好提供高频模态中一些用户可调的算法能量耗散，以抑制可能由实验误差激发的任何虚假振荡。相比之下，结论是数值色散，即相对周期延长，应尽可能小以获得积分方法的最大精度。

最后，以伪代码形式总结了所有引入的积分方法，以协助其在有限元软件中的实现。此外，大多数方法已在OpenSees中实现。

### 7.1.4 事件驱动策略

接下来调查了提供积分和传动系统过程同步的预测-校正算法，这两个过程本质上以不同的速率运行，需要在实时环境中的控制和数据采集系统端实现。首先讨论了先前的发展，如连续和实时测试方法以及使连续地理分布测试成为可能的三环硬件架构（Mosqueda 2003）。

然后介绍了几种改进的预测-校正算法，这些算法将最后预测的位移命令纳入校正公式。证明这些算法在生成连续位移命令信号而不存在切换间隔不一致方面实现了改进的性能。此外，提出了两种基于速度以及加速度的新预测-校正算法，并证明它们在保持生成的位移命令信号连续性的同时实现了改进的精度。详细涵盖了所有引入的同步算法的理论，并根据振幅变化和相移以图形方式评估了其性能和精度。因此，可以得出结论，以C编程语言实现并可供用户使用的新的和改进的同步算法提供了执行更准确连续混合模拟的手段，因此应替代原始算法使用。

接下来研究了采用上述算法进行预测和校正的事件驱动求解策略。首先再次评估了现有策略，然后根据确定的缺陷建议了新的和改进的求解策略。大多数新策略基于自适应控制概念，根据某些合适的性能标准自动调整事件驱动控制器的参数，如时间步、执行器速度等。证明其中一种改进策略成功生成连续的速度过渡（每当需要减慢或加快测试执行时），而不是原始策略的不连续过渡。另一种新求解策略是专门为与隐式Newmark直接积分方法（否则不适合混合模拟）配合使用而开发的，通过调整施加位移命令的时间间隔。最后，除了仍需要在真实物理环境中测试和评估的自适应模拟时间步策略和自适应积分时间步策略外，所有其他事件驱动策略都已在Simulink/Stateflow（Mathworks）中实现，可供用户执行混合模拟。

因此，可以得出结论，新的和改进的预测-校正算法和事件驱动策略为执行连续混合模拟提供了一套重要且有用的工具，其中为控制系统生成了一致且更准确的命令。

### 7.1.5 新型混合模拟示例

为确认扩展的OpenFresco软件框架的稳健性、灵活性和可用性，并验证引入的积分方法和事件驱动同步策略，执行了两个新的、有趣的且具有挑战性的混合模拟示例。

第一个应用展示了历史上首次以软实时执行的连续地理分布混合模拟。证明OpenFresco新实现的Shadow和Actor实验站点与网络技术的最新进步（Abilene网络）相结合，使这种实时地理分布混合模拟成为可能。此外，可以得出结论，改进的预测-校正算法和事件驱动策略成功保证了测试的连续执行，以及在网络延迟情况下实验的平滑减速和加速。

讨论了在过去几年中，实时混合模拟已经获得了相当大的重要性，因为许多新型高性能结构装置，如基础隔震支座、耗能装置和高性能材料，表现出固有的速率依赖行为。因此，得出结论，即使混合模拟是地理分布的，对包含此类装置的结构系统进行测试时以正确的加载速率进行也是至关重要的。成功证明，重新设计、扩展和新实现的实验测试软件框架提供了执行此类混合模拟的手段。

第二个应用介绍了一种利用混合模拟进行结构倒塌研究的新方法。证明OpenFresco软件框架提供了一套有效的模块，特别是新型实验梁柱构件，用于执行准确、安全且经济有效的结构倒塌混合模拟。此外，证明具有10个子步的修正隐式Newmark积分方案能够在显著几何非线性的情况下生成门式框架的准确响应。

最后，得出结论，与常规测试方法相比，结构倒塌的混合模拟提供了三个重要优势：（1）重力荷载和由此产生的几何非线性在混合模型的解析部分中用计算机表示，消除了对复杂主动或被动重力荷载设置的需求；（2）不需要保护昂贵的测试设备免受倒塌期间试样冲击的影响，因为执行器控制系统将限制测试试样的移动；（3）只有结构的关键的、对倒塌敏感的元素需要物理测试，允许在相同预算下大幅增加不同倒塌测试的数量。

## 7.2 未来工作建议

本研究涵盖的主题构成了宝贵的贡献，为研究界提供了一套广泛的工具，如稳健灵活的软件框架以及时间步进积分技术和同步策略的全面汇编，以执行先进的混合模拟来实验研究复杂结构的行为。在开发和实施许多讨论主题的过程中，确定了几个可以从进一步研究中受益的研究领域。

** OpenFresco软件框架：**

1. 增强混合模拟软件框架在干运行模式下模拟测试试样和传动系统（包括控制器、执行器、液压供应系统和仪器）的能力。在实际测试之前进行实验干运行的此类能力对于确定控制参数以及确认各种分析参数输入正确以确保混合模拟可以安全运行至关重要。OpenFresco软件框架目前允许在干运行模式下模拟试样，但功能不足以模拟包括控制器、液压控制系统等关键方面的完整系统，以评估整体稳定性和安全性。   
2. 改进对快速和软实时地理分布混合模拟的支持，并验证OpenFresco软件框架是否提供硬实时混合模拟所需的功能。这是一个快速增长的研究领域，几个NEES设备站点和个别研究项目正在进行需要实时或快速测试执行的项目。应包括以下活动：在OpenFresco软件框架中实现补偿在混合模拟的快速或实时执行期间在物理测试部分产生的惯性和粘滞阻尼力的方法（见第2章）。扩展OpenFresco软件框架，使其可用于通过执行混合模拟来执行智能振动台测试，其中模拟器平台被实时控制。调查进一步改进地理分布混合模拟的速度和可靠性的方法，并充分利用下一代互联网的能力。   
3. 几个NEES设备站点和研究人员目前正在努力实现力和混合力/位移控制混合模拟的能力。因此，与这些设备站点和研究人员合作，对OpenFresco软件框架进行任何必要的更改以实现力和混合力/位移控制，以及在模拟期间在力和位移控制之间切换，这一点很重要。   
4. OpenFresco软件框架的主要功能之一是允许用户选择使用任何有限元分析软件。目前，与OpenSees、Matlab、LS-Dyna和SimCor的实现运行良好。然而，应调查并为其他广泛使用的有限元软件包（如Abaqus和SAP2000）实现额外的接口。

5. NEES的目标之一是通过共享的、可网络访问的存储库促进研究人员和执业工程师之间的数据和信息的开放交换。因此，为OpenFresco软件框架中的所有对象实现记录功能并研究将所有记录数据自动上传到NEES数据存储库的方法至关重要。

**积分方法：**

1. 调查在OpenSees中实现所有讨论的Runge-Kutta积分方法（特别是实时兼容的Rosenbrock方法）所需的更改或补充。由于对于Runge-Kutta方法，二阶微分方程被转换为一阶常微分方程组，分析期间需要求解的线性方程组的大小加倍。这将需要在OpenSees中进行一些新的补充，以组装和求解这些独特的线性方程组。   
2. 应调查混合时间隐式-显式积分方案（Liu和Belytschko 1982）在混合模拟中的应用。与隐式-显式积分方法（Hughes和Liu 1978）相反，后者由Dermitzakis和Mahin（1985）用于混合模拟，Liu和Belytschko（1982）的分区程序允许在有限元网格的不同部分同时使用具有不同时间步的不同时间积分算法。

**事件驱动策略：**

1. 许多模拟结果但仅有限数量的实际测试被执行以验证新引入的预测-校正算法。因此，应执行额外的真实混合模拟以加强算法在更广泛条件下的验证。具体而言，如果积分方法提供速度和加速度（特别是Runge-Kutta方法一旦在OpenSees中实现），应进一步调查基于速度和加速度的算法。

2. 为了使自适应模拟和积分时间步策略可供混合模拟用户和研究人员使用，应在Simulink/Stateflow（Mathworks）中实现它们，以便在发布之前通过真实实时环境中的实际测试进行验证。

**应用：**

1. 有一系列混合模拟应用由于以下已知问题而难以执行。由于执行器的运动学相互作用，利用执行器阵列控制三维系统很困难。此外，控制具有大物理质量的实验子组件非常具有挑战性，因为惯性力相互作用。如果由于结构装置的速率依赖性需要高加载速率，这变得更加困难。因此，应设计示例应用来执行混合模拟以调查这些问题并研究处理这些困难的方法。

# 参考文献

Ahmadizadeh, M., et al. [2008]. "Compensation of actuator delay and dynamics for real-time hybrid structural simulation." Earthquake Engineering & Structural Dynamics 37(1): 21-42.   
Bathe, K.-J. [1996]. Finite element procedures. Englewood Cliffs, NJ, Prentice Hall.   
Bayer, V., et al. [2005]. "On real-time pseudo-dynamic sub-structure testing: algorithm, numerical and experimental results." Aerospace Science and Technology 9(3): 223-232.   
Belytschko, T. and Hughes, T. J. R. [1983]. Computational methods for transient analysis. Amsterdam; New York, NY, North-Holland.   
Blakeborough, A., et al. [2001]. "The development of real-time substructure testing." Philosophical Transactions of the Royal Society: Mathematical, Physical and Engineering Sciences 359(1786): 1869-1891.   
Bonelli, A. and Bursi, O. S. [2004]. "Generalized-alpha methods for seismic structural testing." Earthquake Engineering & Structural Dynamics 33(10): 1067-1102.   
Bonnet, P. A., et al. [2008]. "Evaluation of numerical time-integration schemes for real-time hybrid testing." Earthquake Engineering & Structural Dynamics 37(13): 1467-1490.   
Booch, G., et al. [2005]. The unified modeling language user guide. Upper Saddle River, NJ, Addison-Wesley.   
Burden, R. L. and Faires, J. D. [2001]. Numerical analysis. Pacific Grove, CA, Brooks/Cole-Thomson Learning.   
Bursi, O. S., et al. [2008]. "Novel coupling Rosenbrock-based algorithms for real-time dynamic substructure testing." Earthquake Engineering & Structural Dynamics 37(3): 339-360.   
Bursi, O. S., et al. [1994]. "Pseudodynamic testing of strain-softening systems with adaptive time steps." Earthquake Engineering & Structural Dynamics 23(7): 745-760.   
Bursi, O. S. and Shing, P. S. B. [1996]. "Evaluation of some implicit time-stepping algorithms for pseudodynamic tests." Earthquake Engineering & Structural Dynamics 25(4): 333-355.   
Butcher, J. C. [2003]. Numerical methods for ordinary differential equations. Chichester, West Sussex, England ; Hoboken, NJ, J. Wiley.   
Campbell, S. and Stojadinovic, B. [1998]. A system for simultaneous pseudodynamic testing of multiple substructures. Proceedings, Sixth U.S. National Conference on Earthquake Engineering. Seattle, WA.   
Carnegie Mellon SEI. [2008]. "Software technology roadmap." from http://www.sei.cmu.edu/str.   
Chang, S.-Y. [2002]. "Explicit pseudodynamic algorithm with unconditional stability." Journal of Engineering Mechanics 128(9): 935-947.   
Chang, S. Y. and Sung, Y. C. [2006]. An enhanced explicit pseudodynamic algorithm with unconditional stability. Proceedings, Eighth U.S. National Conference on Earthquake Engineering. San Francisco, CA.   
Chopra, A. K. [2001]. Dynamics of structures: theory and applications to earthquake engineering. Upper Saddle River, NJ, Prentice Hall.   
Chung, J. and Hulbert, G. M. [1993]. "A time integration algorithm for structural dynamics with improved numerical dissipation: the generalized-alpha method." Journal of Applied Mechanics, ASME 60(2): 371-375.   
Combescure, D. and Pegon, P. [1997]. "Alpha-operator splitting time integration technique for pseudodynamic testing error propagation analysis." Soil Dynamics and Earthquake Engineering 16(7-8): 427-443.   
Cook, R. D. [2002]. Concepts and applications of finite element analysis. New York, NY, Wiley.

Darby, A. P., et al. [1999]. "Real-time substructure tests using hydraulic actuator." Journal of Engineering Mechanics 125(10): 1133-1139.   
Darby, A. P., et al. [2001]. "Improved control algorithm for real-time substructure testing." Earthquake Engineering & Structural Dynamics 30(3): 431-448.   
de Souza, R. M. [2000]. Force-based finite element for large displacement inelastic analysis of frames, University of California, Berkeley. Ph.D.: 205.   
Deitel, H. M. and Deitel, P. J. [2003]. $\mathrm { C } { + + }$ how to program. Upper Saddle River, NJ, Prentice Hall.   
Dermitzakis, S. N. and Mahin, S. A. [1985]. Development of substructuring techniques for on-line computer controlled seismic performance testing. Berkeley, CA, Earthquake Engineering Research Center: 153 pages.   
Dorka, U. E. [2002]. Hybrid experimental - numerical simulation of vibrating structures. International Conference WAVE2002. Okayama, Japan.   
Dorka, U. E. and Heiland, D. [1991]. Fast online earthquake utilizing a novel PC supported measurement and control concept. 4th Conference on Structural Dynamics. Southampton, UK.   
dSpace Inc. [2008]. "dSPACE." from http://www.dspaceinc.com/ww/en/inc/home.cfm.   
Elkhoraibi, T. and Mosalam, K. M. [2007]. "Towards error-free hybrid simulation using mixed variables." Earthquake Engineering & Structural Dynamics 36(11): 1497-1522.   
Erlicher, S., et al. [2002]. "The analysis of the generalized-α method for non-linear dynamic problems." Computational Mechanics 28(2): 83-104.   
Fenves, G. L. [1990]. "Object-oriented programming for engineering software development." Engineering with Computers 6(1): 1-15.   
Fenves, G. L., et al. [2004]. An object-oriented software environment for collaborative network simulation. Proceedings, 13th World Conference on Earthquake Engineering. Vancouver, BC, Canada.   
Filippou, F. C. and Fenves, G. L. [2004]. Methods of analysis for earthquake-resistant structures. Earthquake Engineering: From Engineering Seismology to Performance-Based Engineering. Boca Raton, FL, CRC Press.   
Gamma, E., et al. [1995]. Design patterns: elements of reusable object-oriented software. Reading, MA, Addison-Wesley.   
Gawthrop, P. J., et al. [2007]. "Robust real-time substructuring techniques for under-damped systems." Structural Control and Health Monitoring 14(4): 591-608.   
Gourley, D. and Totty, B. [2002]. Http: the definitive guide. Beijing; Cambridge, MA, O'Reilly.   
Hairer, E., et al. [2000]. Solving ordinary differential equations I, nonstiff problems. Berlin; New York, NY, Springer-Verlag.   
Hairer, E. and Wanner, G. [2002]. Solving ordinary differential equations II, stiff and differential-algebraic problems. Berlin; New York, NY, Springer-Verlag.   
Harris, H. G., et al. [1999]. Structural modeling and experimental techniques. Boca Raton, FL, CRC Press.   
Heun, K. [1900]. "Neue Methoden zur approximativen Integration der Differentialgleichungen einer unabhängigen Veränderlichen." Zeitschrift für Mathematik und Physik 45: 23-38.   
Hilber, H. M. and Hughes, T. J. R. [1978]. "Collocation, dissipation and 'overshoot' for time integration schemes in structural dynamics." Earthquake Engineering and Structural Dynamics 6(1): 99-117.   
Hilber, H. M., et al. [1977]. "Improved numerical dissipation for time integration algorithms in structural dynamics." Earthquake Engineering and Structural Dynamics 5(3): 283-292.

Horiuchi, T., et al. [2000]. Development of a real-time hybrid experimental system using a shaking table. Proceedings, 12th World Conference on Earthquake Engineering. Auckland, New Zealand.   
Horiuchi, T., et al. [1999]. "Real-time hybrid experimental system with actuator delay compensation and its application to a piping system with energy absorber." Earthquake Engineering & Structural Dynamics 28(10): 1121-1141.   
Horiuchi, T. and Konno, T. [2001]. "A new method for compensating actuator delay in real-time hybrid experiments." Philosophical Transactions of the Royal Society: Mathematical, Physical and Engineering Sciences 359(1786): 1893-1909.   
Horiuchi, T., et al. [1996]. Development of a real-time hybrid experimental system with actuator delay compensation. Proceedings, 11th World Conference on Earthquake Engineering. Acapulco, México.   
Hubbard, P., et al. [2004]. Protocol specification for the LabView NTCP plugin. San Diego, CA, NEESit Technical Report.   
Hughes, T. J. R. [2000]. The finite element method: linear static and dynamic finite element analysis. Mineola, NY, Dover Publications.   
Hughes, T. J. R. and Liu, W. K. [1978]. "Implicit-explicit finite elements in transient analysis: implementation and numerical examples." Journal of Applied Mechanics, ASME 45(2): 375-378.   
Hughes, T. J. R. and Liu, W. K. [1978]. "Implicit-explicit finite elements in transient analysis: stability theory." Journal of Applied Mechanics, ASME 45(2): 371-374.   
Hughes, T. J. R., et al. [1979]. "Implicit-explicit finite elements in nonlinear transient analysis " Computer Methods in Applied Mechanics and Engineering 17(18): 159-182.   
Hulbert, G. M. and Chung, J. [1996]. "Explicit time integration algorithms for structural dynamics with optimal numerical dissipation." Computer Methods in Applied Mechanics and Engineering 137(2): 175-188.   
Humar, J. L. [2002]. Dynamics of structures. Exton, PA, A.A. Balkema Publishers.   
Igarashi, A., et al. [1993]. Development of the pseudodynamic technique for testing a full scale 5-story shear wall structure. U.S. - Japan Seminar, Development and Future Dimensions of Structural Testing Techniques. Honolulu, HI.   
Jung, R.-Y. and Shing, P. B. [2006]. "Performance evaluation of a real-time pseudodynamic test system." Earthquake Engineering & Structural Dynamics 35(7): 789-810.   
Jung, R.-Y., et al. [2007]. "Performance of a real-time pseudodynamic test system considering nonlinear structural response." Earthquake Engineering & Structural Dynamics 36(12): 1785-1809.   
Kaps, P. and Wanner, G. [1981]. "A study of Rosenbrock-type methods of high order." Numerische Mathematik 38(2): 279-298.   
Kuhl, D. and Crisfield, M. A. [1999]. "Energy-conserving and decaying algorithms in non-linear structural dynamics." International Journal for Numerical Methods in Engineering 45(5): 569-599.   
Kutta, W. [1901]. "Beitrag zur näherungsweisen Integration totaler Differentialgleichungen." Zeitschrift für Mathematik und Physik 46(435-453).   
Kwon, O.-S., et al. [2005]. "A framework for multi-site distributed simulation and application to complex structural systems." Journal of Earthquake Engineering 9(5): 741-753.   
Lambert, J. D. [1991]. Numerical methods for ordinary differential systems: the initial value problem. Chichester ; New York, NY, Wiley.

Liu, W. K. and Belytschko, T. [1982]. "Mixed-time implicit-explicit finite elements for transient analysis." Computers and Structures 15(4): 445-450.   
Liu, W. K., et al. [1984]. "Implementation and accuracy of mixed-time implicit-explicit methods for structural dynamics." Computers & Structures 19(4): 521-530.   
Livermore Software Technology Corp. [2008]. "LS-DYNA." from http://www.lstc.com.   
Magonette, G. [2001]. "Development and application of large-scale continuous pseudo-dynamic testing techniques." Philosophical Transactions of the Royal Society: Mathematical, Physical and Engineering Sciences 359(1786): 1771-1799.   
Magonette, G. E. and Negro, P. [1998]. "Verification of the pseudodynamic test method." European Earthquake Engineering XII(1): 40-50.   
Mahin, S. A., et al. [1989]. "Pseudodynamic test method - current status and future directions." Journal of Structural Engineering 115(8): 2113-2128.   
Mahin, S. A. and Shing, P. S. B. [1985]. "Pseudodynamic method for seismic testing." Journal of Structural Engineering 111(7): 1482-1503.   
Mahin, S. A. and Williams, M. E. [1980]. Computer controlled seismic performance testing. Dynamic Response of Structures: Experimentation, Observation, Prediction and Control, American Society of Civil Engineers, New York, NY.   
Manring, N. [2005]. Hydraulic control systems. Hoboken, NJ, John Wiley & Sons.   
Maplesoft. [2008]. "Maple." from http://www.maplesoft.com.   
Mathworks. [2008]. "MATLAB, Simulink, Stateflow, xPC Target." from http://www.mathworks.com.   
McKenna, F. T. [1997]. Object-oriented finite element programming: frameworks for analysis, algorithms and parallel computing, University of California, Berkeley. Ph.D.: 247.   
Mercan, O. and Ricles, J. M. [2007]. "Stability and accuracy analysis of outer loop dynamics in real-time pseudodynamic testing of SDOF systems." Earthquake Engineering & Structural Dynamics 36(11): 1523-1543.   
Morgan, T. A. [2007]. The use of innovative base isolation systems to achieve complex seismic performance objectives, University of California, Berkeley. Ph.D.: 323.   
Mosqueda, G. [2003]. Continuous hybrid simulation with geographically distributed substructures, University of California, Berkeley. Ph.D.: 232.   
Mosqueda, G., et al. [2005]. Implementation and accuracy of continuous hybrid simulation with geographically distributed substructures. Berkeley, CA, Earthquake Engineering Research Center.   
Mosqueda, G., et al. [2007]. "Real-time error monitoring for hybrid simulation. Part II: Structural response modification due to errors." Journal of Structural Engineering (8): 1109-1117.   
Mosqueda, G., et al. [2007]. "Real-time error monitoring for hybrid simulation. Part I: methodology and experimental verification." Journal of Structural Engineering (8): 1100-1108.   
Mosqueda, G., et al. [2004]. Experimental and analytical studies of the friction pendulum system for the seismic protection of simple bridges. Berkeley, CA, Earthquake Engineering Research Center.   
MTS. [2008]. "Civil engineering testing solutions." from http://www.mts.com.   
Nakashima, M. [1985]. "Part 2: Relationship between integration time interval and accuracy of displacement, velocity, and acceleration responses in pseudo dynamic testing." Journal of Structural and Construction Engineering (Transactions of AIJ) (358): 35-42.

Nakashima, M. [1985]. "Part 1: Relationship between integration time interval and response stability in pseudo dynamic testing (stability and accuracy behavior of pseudo dynamic response)." Journal of Structural and Construction Engineering (Transactions of AIJ) (353): 29-36.   
Nakashima, M. [2001]. "Development, potential, and limitations of real-time online (pseudo-dynamic) testing." Philosophical Transactions of the Royal Society: Mathematical, Physical and Engineering Sciences 359(1786): 1851-1867.   
Nakashima, M., et al. [1988]. Feasibility of pseudo dynamic test using substructuring techniques. Proceedings, Ninth World Conference on Earthquake Engineering. Tokyo, Japan.   
Nakashima, M., et al. [1990]. Integration techniques for substructure pseudo dynamic test. Proceedings, Fourth U.S. National Conference on Earthquake Engineering. Palm Springs, CA.   
Nakashima, M. and Kato, H. [1987]. Experimental error growth behavior and error growth control in on-line computer test control method. Building Research Institute, Ministry of Construction, Tsukuba, Japan: 145 pages.   
Nakashima, M. and Kato, H. [1988]. "Part 3: experimental error growth in pseudo dynamic testing (stability and accuracy behavior of pseudo dynamic response)." Journal of Structural and Construction Engineering (Transactions of AIJ) (386): 36-48.   
Nakashima, M. and Kato, H. [1989]. "Part 4: Control of experimental error growth in pseudo dynamic testing-- Stability and accuracy behavior of pseudo dynamic response." Journal of Structural and Construction Engineering (Transactions of AIJ) (401): 129-138.   
Nakashima, M., et al. [1992]. "Development of real-time pseudo dynamic testing." Earthquake Engineering & Structural Dynamics 21(1): 79-92.   
Nakashima, M. and Masaoka, N. [1999]. "Real-time on-line test for MDOF systems." Earthquake Engineering & Structural Dynamics 28(4): 393-420.   
Newmark, N. M. [1959]. "A method of computation for structural dynamics." Journal of Engineering Mechanics, ASCE 67.   
Nise, N. S. [2004]. Control systems engineering. Hoboken, NJ, Wiley.   
OpenFresco. [2008]. "Open Framework for Experimental Setup and Control." from http://openfresco.neesforge.nees.org.   
OpenSees. [2008]. "Open System for Earthquake Engineering Simulation." from http://opensees.berkeley.edu.   
Pan, P., et al. [2005]. "Online test using displacement-force mixed control." Earthquake Engineering & Structural Dynamics 34(8): 869-888.   
Pan, P., et al. [2005]. "Online hybrid test by internet linkage of distributed test-analysis domains." Earthquake Engineering & Structural Dynamics 34(11): 1407-1425.   
Pan, P., et al. [2006]. "Development of peer-to-peer (P2P) internet online hybrid test system." Earthquake Engineering & Structural Dynamics 35(7): 867-890.   
Pinto, A. V., et al. [2004]. "Pseudo-dynamic testing of bridges using non-linear substructuring." Earthquake Engineering & Structural Dynamics 33(11): 1125-1146.   
Plesha, M. E. and Belytschko, T. [1985]. "A constitutive operator splitting method for nonlinear transient analysis." Computers & Structures 20(4): 767-777.

Rodgers, J. E. and Mahin, S. A. [2004]. Effects of connection hysteretic degradation on the seismic behavior of steel moment-resisting frames. Berkeley, CA, Pacific Earthquake Engineering Research Center.   
Runge, C. [1895]. "Ueber die numerische Auflösung von Differentialgleichungen." Mathematische Annalen 46: 167-178.   
Sandee, J. H., et al. [2005]. Event-driven control as an opportunity in the multidisciplinary development of embedded controllers, Technische Universiteit Eindhoven, Dept. of Electrical Engineering, Control Systems Group.   
Schellenberg, A. and Mahin, S. [2006]. Integration of hybrid simulation within the general-purpose computational framework Opensees. Proceedings, Eighth U.S. National Conference on Earthquake Engineering. San Francisco, CA.   
Schellenberg, A., et al. [2007]. A software framework for hybrid simulation of large structural systems. Proceedings, 2007 Structures Congress. Long Beach, CA.   
Schneider, S. P. and Roeder, C. W. [1994]. "An inelastic substructure technique for the pseudodynamic test method." Earthquake Engineering & Structural Dynamics 23(7): 761-775.   
Scott, M. H. and Fenves, G. L. [2003]. A Krylov subspace accelerated Newton algorithm. ASCE Structures Congress. Seattle, WA.   
Shampine, L. F. [1982]. "Implementation of Rosenbrock methods." ACM Transactions on Mathematical Software 8(2): 93-113.   
Shing, P. B., et al. [1994]. "Pseudodynamic tests of a concentrically braced frame using substructuring techniques." Journal of Constructional Steel Research 29(1-3): 121-148.   
Shing, P. B. and Mahin, S. A. [1983]. Experimental error propagation in pseudodynamic testing. Berkeley, CA, Earthquake Engineering Research Center: 175 pages.   
Shing, P. B., et al. [2002]. Conceptual design of fast hybrid test system at the University of Colorado. Proceedings, Seventh U.S. National Conference on Earthquake Engineering. Boston, MA.   
Shing, P. B., et al. [2004]. Nees fast hybrid test system at the University of Colorado. Proceedings, 13th World Conference on Earthquake Engineering. Vancouver, BC, Canada.   
Shing, P. S. B. and Mahin, S. A. [1984]. Pseudodynamic test method for seismic performance evaluation: theory and implementation. Berkeley, CA, Earthquake Engineering Research Center: 162 pages.   
Shing, P. S. B. and Mahin, S. A. [1987]. "Cumulative experimental errors in pseudodynamic tests." Earthquake Engineering & Structural Dynamics 15(4): 409-424.   
Shing, P. S. B. and Mahin, S. A. [1987]. "Elimination of spurious higher-mode response in pseudodynamic tests." Earthquake Engineering & Structural Dynamics 15(4): 425-445.   
Shing, P. S. B., et al. [1996]. "Application of pseudodynamic test method to structural research." Earthquake Spectra 12(1): 29-56.   
Shing, P. S. B. and Vannan, M. T. [1991]. "Implicit time integration for pseudodynamic tests: convergence and energy dissipation." Earthquake Engineering & Structural Dynamics 20(9): 809-819.   
Shing, P. S. B., et al. [1991]. "Implicit time integration for pseudodynamic tests." Earthquake Engineering & Structural Dynamics 20(6): 551-576.   
Simo, J. C. and Hughes, T. J. R. [1998]. Computational inelasticity. New York, NY, Springer.

Sivaselvan, M. V. [2006]. A unified view of hybrid seismic simulation algorithms. Boulder, CO, NEES at CU-Boulder.   
Smith, S. W. [1997]. The scientist and engineer's guide to digital signal processing. San Diego, CA, California Technical Pub.   
Systran. [2008]. "SCRAMNet+ network." from http://www.cwcembedded.com.   
Tada, M. and Pan, P. [2007]. "A modified operator splitting (OS) method for collaborative structural analysis (CSA)." International Journal for Numerical Methods in Engineering 72(4): 379-396.   
Takahashi, Y. and Fenves, G. L. [2006]. "Software framework for distributed experimental–computational simulation of structural systems." Earthquake Engineering & Structural Dynamics 35(3): 267-291.   
Takanashi, K. and Nakashima, M. [1987]. "Japanese activities on on-line testing." Journal of Engineering Mechanics 113(7): 1014-1032.   
Takanashi, K., et al. [1975]. "Non-linear earthquake response analysis of structures by a computer-actuator online system--Part 1: detail of the system." Transactions of the Architectural Institute of Japan (229): 77-83.   
Tcl Developer Xchange. [2008]. "Tcl/Tk." from http://www.tcl.tk.   
Tedesco, J. W., et al. [1999]. Structural dynamics: theory and applications. Menlo Park, CA, Addison-Wesley.   
Thewalt, C. R. and Mahin, S. A. [1987]. Hybrid solution techniques for generalized pseudodynamic testing. Berkeley, CA, Earthquake Engineering Research Center: 142 pages.   
Thewalt, C. R. and Mahin, S. A. [1995]. "An unconditionally stable hybrid pseudodynamic algorithm." Earthquake Engineering & Structural Dynamics 24(5): 723-731.   
Thewalt, C. R. and Roman, M. [1994]. "Performance parameters for pseudodynamic tests." Journal of Structural Engineering 120(9): 2768-2781.   
Thiele, K. [2000]. Pseudodynamische Versuche an Tragwerken mit grossen Steifigkeitsanderungen und mehreren Freiheitsgraden. Zurich, Switzerland, Federal Institute of Technology. Ph.D.: 168.   
Timoshenko, S. [1961]. Theory of elastic stability. New York, NY, McGraw-Hill.   
Uriz, P. [2005]. Towards earthquake resistant design of concentrically braced steel structures, University of California, Berkeley. Ph.D.: 436.   
US NSF. [2008]. "George E. Brown Jr. Network for Earthquake Engineering Simulation (NEES)." from http://www.nees.org.   
Verwer, J. G. [1981]. "An analysis of Rosenbrock methods for nonlinear stiff initial value problems." SIAM Journal on Numerical Analysis 19(1): 155-170.   
Wallace, M. I., et al. [2005]. "Stability analysis of real-time dynamic substructuring using delay differential equation models." Earthquake Engineering & Structural Dynamics 34(15): 1817-1832.   
Wallace, M. I., et al. [2005]. "An adaptive polynomial based forward prediction algorithm for multi-actuator realtime dynamic substructuring." Proceedings of the Royal Society of London A 461(2064): 3807-3826.   
Wang, T., et al. [2006]. "On-line hybrid test combining with general-purpose finite element software." Earthquake Engineering & Structural Dynamics 35(12): 1471-1488.   
Wang, Y.-P., et al. [2001]. "Modified state-space procedures for pseudodynamic testing." Earthquake Engineering & Structural Dynamics 30(1): 59-80.   
Wolfram. [2008]. "Mathematica." from http://www.wolfram.com.

Wu, B., et al. [2007]. "Equivalent force control method for generalized real-time substructure testing with implicit integration." Earthquake Engineering & Structural Dynamics 36(9): 1127-1149.   
Yang, T. Y. [2006]. Performance evaluation of innovative steel braced frames, University of California, Berkeley. Ph.D.: 245.   
Zayas, V. A., et al. [1989]. Feasibility and performance studies on improving the earthquake resistance of new and existing buildings using the friction pendulum system. Berkeley, CA, Earthquake Engineering Research Center: 302 pages.   
Zayas, V. A., et al. [1987]. The FPS earthquake resisting system: experimental report. Berkeley, CA, Earthquake Engineering Research Center: 98 pages.   
Zhong, W. [2005]. Fast hybrid test system for substructure evaluation, University of Colorado at Boulder. Ph.D.: 123.