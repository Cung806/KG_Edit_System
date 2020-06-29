# **KG_Edit_System**
该项目是是一个基于Neo4j的知识图谱编辑工具，由Django框架完成。在导入三元组在neo4j数据库后，可以实现对知识图谱关系和实体结点的增删改查。数据目前用的是专业内容知识图谱数据，由项目组构建的计算机领域的实体和关系数据。
#### 知识图谱链接（演示链接）：<http://39.100.48.36:3010/account/demo>
上面的链接没有知识图谱编辑功能，仅供展示，只能查看搜索，编辑的功能需要登录才可使用。
#### 目前只有计算机领域的知识图谱
计算机领域的知识图谱实体和关系类型如下：

| 关系类型        | 实体类型   |
| --------   | -----:  |
| 应用关系      | 处理任务   |
| 对比关系        |   处理方法   |
| 同指关系        |    数据集    |
| 包含关系        |    评估指标    |

#### 项目截图如下:
![demo](https://raw.githubusercontent.com/Cung806/KG_Edit_System/master/demo.png)

----
# 实验室项目组介绍以及项目展示如下
#### 重庆大学nlp平台链接：<http://39.100.48.36>
#### 知识图谱构建中用到的命名实体识别模型的demo展示链接： <http://39.100.48.36/entity.html>
#### 知识图谱构建中用到的关系抽取模型的demo展示链接：<http://39.100.48.36/relation.html>