# 回顾性计划表

| [English Ver.](README.md) |
| - |

这是一个将回顾性计划表从 `.csv` 转为 `png` 的工具。

## 目录

- [背景介绍](#背景介绍)

    - [回顾性计划](#回顾性计划)
    - [CSV](#csv)
    - [JSON](#json)
    - [正则表达式](#正则表达式)

- [前置要求](#前置要求)

- [使用方法](#使用方法)

    - [创建一个CSV文件](#创建一个CSV文件)
    - [CSV基础](#CSV基础)
    - [CSV转PNG](#csv转png)
    - [配置](#配置)
    - [主题](#主题)

- [示例](#示例)

## 背景介绍

### 回顾性计划

[回顾性计划](https://www.youtube.com/watch?v=b7o09a7t4RA)是前瞻性计划的反面。
在前瞻性计划中，未来事项提前按时间线和最终目标规划，整齐而有条理。
对于固定的日常任务来说，这很有用。

但是，这种计划有几点不足：

- 进展不明确

    目标的进度，尤其是学习目标的，通常不与所花的时间成正比。
    学习或工作的效率也时常变化。
    由时间线规划的任务无法很好地反映其进度。

- 灵活性低
    
    因为任务是根据时间规划的，很难在不打乱其他任务计划的情况下调整某一项任务。

- 难以坚持

    是的，就像所有严格但不强制的要求一样。

现在来看看**回顾性计划**。
在回顾性计划中，未来的行动基于过去的成果，而非安排好的时间表。
目标，或者说学习中的科目，被排在一张表格的首列。
每当你做些工作来缩短与最终目标之间的距离，比如说，做几道练习题来巩固三角函数，就在对应科目后加一格日期，以及当次学习的进展。
在科目间循环往复，每一项的进度和紧迫程度都能清晰地看到。

来看一个例子：

| 三角函数 | 09-08 (差) | 09-12 (还行) | 09-16 (很好) | 09-20 (考试) |
| - | - | - | - | - |

1. 计划表的使用者正为 `09-20` 的三角函数考试发愁，表格的末尾写上了 `考试` 的死线。
2. 第一次学三角函数，他尝试了10道练习题，但只做对了2道，所以日期后面加上了 `差` 的标签。
3. 4天后，他看见 `三角函数` 这项的最新进度还是 `差`，就复习了一下。这次他做对了5道，有进步，但不够，故标记为 `还行`。
4. 然后，他花了更多精力在这门课上，最终在练习时达到了 8/10 的好成绩，`很好`。
5. 现在，他对20日的考试很自信了。

一般来说，这样的表格是用 Excel 之类的软件制作的。
在 Excel 中，表格可以上色以便区分不同的进度/成果。

有的人（我）希望用一种更简单，可扩展且不需要任何 Office 软件制作的格式来记录自己的规划。
那么这里有一个给 `.csv` 爱好者用的工具。

### CSV

CSV 指 **C**omma-**S**eparated **V**alues。
英文逗号之间的文本被视为一个值，或者叫 Excel 中的“一格”。

`.csv` 文件写起来非常简单，见下：

```csv
三角函数,1a,2b,3c
复述,i,e,theta
```

就是这样，用逗号分割文本！

### JSON

[JSON](https://www.w3schools.com/whatis/whatis_json.asp)指 **J**ava**S**cript **O**bject **N**otation。
这是一种文件格式，其内容应该易于阅读。

此脚本用 JSON 作为其配置和主题的格式。

**请注意，JSON 语法严格，编辑时要小心。**

### 正则表达式

[正则表达式（regex）](https://zh.wikipedia.org/wiki/正则表达式)是一个强大的“查找与替换”工具。

此脚本用正则查找输入和主题文件。

**请注意，正则语法严格，编辑时要小心。**

## 前置要求

- [python](https://www.python.org) (在最新稳定版上测试过)

    Python 是这个脚本使用的编程语言。
    要安装 python，去[它的官网](https://www.python.org/downloads/)下载安装包并遵循指示。
    你还可以用你喜欢的包管理器安装：

    - macOS

        `brew install python`
        (需要 [homebrew](https://brew.sh))
    
    - Windows

        `winget install -e --id Python.Python.3.11 --scope machine`
    
    - Linux

	使用对应的包管理器。

- [matplotlib](https://matplotlib.org)

    这是一个用于绘图的 python 扩展包。
    运行下面这条指令安装（先安装 python）

    `pip install matplotlib`

## 使用方法

### 创建一个CSV文件

新建一个 `.csv` 文件。
也许将它命名为 `plans.csv`？

接下来用你喜欢的文本编辑器打开它，记事本、文本编辑、VS Code、Vim 或者任何可以编辑文本的东西！

### CSV基础

1. 在第一列写下各个事项的名称

    ```csv
    三角函数
    复数
    ```

    你可以为项目设置死线，加一个带 `#dead` 标签格子就行：

    ```csv
    三角函数,11-01#dead
    复数,11-21#dead
    ```

2. 每当你有新进度，在对应项目后面加上一格日期

    ```csv
    三角函数,09-08
    复数,09-01
    ```

    **请注意，没有后续格子的项目不会被脚本放进图片中。**

3. 基于当次的成果，给格子加上 `#good`，`#ok` 或 `#bad` 的标签

    ```csv
    三角函数,09-08#bad
    复数,09-01#ok
    ```

    目前，**每一格只有第一个标签有用**。
    未定义的标签也会被忽略。

### CSV转PNG

在 `.csv` 文件中写上你的计划后，你大概想要把它导出成一张彩色图片，清晰又好看。

既然如此，[这个脚本](csv2png.py) 就是你需要的了。
把它下载到你的电脑上。

1. 将 `.csv` 文件和 `csv2png.py` 脚本放到同一文件夹下，这里我们叫它 `辣个文件夹`

    ```
    辣个文件夹/
    |--- plans.csv
    |--- csv2png.py
    ```

2. 启动终端模拟器（bash、cmd、pwsh、zsh……）, `cd` 到 `辣个文件夹`

    ```sh
    cd 到/辣个文件夹/的/路径
    ```

3. 运行脚本

    ```sh
    python csv2png.py
    ```

4. 按照指示操作

    1. 输入 `.csv` 文件的名称，不带 `.csv`

        ```
        plans (再按 Enter)
        ```
    
    2. 等待转换完成

	你会看到输出的日志。

    3. 一个与你 `.csv` 文件名相同的 `.png` 文件应该会出现在 `辣个文件夹` 里

        ```
        辣个文件夹/
        |--- csv2png.py
        |--- plans.csv
        |--- plans.png
        ```

### 配置

此脚本允许你配置输入、输出和主题文件的路径，以及所使用的主题。

若想自定义主题，请看[主题](#主题)

#### 创建配置文件

1. 新建一个叫做 `retro.conf.json` 的 JSON 文件
2. place it in the same folder as the script

#### Adding Config Items

```json
{
    "input_path": "./in/plan.*",
    "output_dir": "./out/",
    "theme_path": "./themes/fun.*",
    "theme_name": "funky"
}
```

##### `input_path`
`input_path` is path to the input file(s).
With this item set to a proper value, typing filename is not needed while running the script.

Its default value is an empty string, which you have to specify.

**Note that the filename section of this path is treated as a [regular expression](https://regexr.com) pattern, and does not need the `\.csv$` pattern.**

For example, `plan.*` will match every `.csv` file in `./in/` which its name starts with `plan`.

##### `output_dir`
`output_dir` decides the directory/folder which pictures will be output to.
If its set to `./out/`, output pictures will be placed in `./out/`.

Its default value is `./`.

**Note that the script does not generate non-existing paths, so make sure the directory actually exists.**

##### `theme_path`
`theme_path` means path to the theme file(s).
If the path does not exist, the default theme will be used.

**Note that the filename section of this path is treated as a [regular expression](https://regexr.com) pattern, and does not need the `\.json$` pattern.**

For example, `./themes/fun.*` will match every `.json` file in `./themes/` which its name starts with `fun`.

Its default value is ``.

##### `theme_name`
`theme_name` is name of the theme that will be used in picture generation.
If the theme does not exist or the theme name is not set, the default theme will be used.

Its default value is an empty string, which represents no theme chosen.

### Themes

Themes define colors (possibly dimensions in the future) of cells and texts in the output pictures.

#### Default Theme

If no theme is specified or the specified theme does not exist, the default theme will be used.

#### Making A Theme File

1. create a `.json` file named as `theme.json`
2. place it at `theme_path`, which by default is `./`

#### Adding A Theme

```json
{
	"funky": {
		"fore": "#E6DAA6",
		"back": "#808080",
		"edge": "#929591",
		"subject": {
			"back": "#01153E"
		},
		"tags": {
			"good": {
				"back": "#029386"
			},
			"ok": {
				"back": "#A9561E"
			},
			"bad": {
				"back": "#EF4026"
			},
			"dead": {
				"fore": "#3D1C02",
				"back": "#E6DAA6"
			},
			"hey": {
				"back": "white",
				"fore": "black"
			}
		}
	}
}
```

At the first level, name of the theme is stated (`funky`).

It has three main elements, `fore` for foreground (texts), `back` for background and `edge` for edge lines of the cell.

**These three values must be set, otherwise the script won't work.**

Other than the main elements, there are optional elements `subject` and `tags`.

`subject` is and is only for the first column.

`tags` contains tags that can be used in the `.csv` files by appending `#tag_name` into a cell.

Each optional elements can have `fore`, `back` or `edge` set.
**Main colors will be used if they are not specified for optional elements.**

**Basic color names (white, black, red, blue, etc.) and hex color code are supported.**

#### Adding A Tag

As you may have noticed, there is a `hey` tag in the theme code above.
`hey` is not a built-in tag, but with this theme it works as expected, changing text color to black and background color to white.

That simple!
To add a tag, you only need a new element under `tags` in the theme.

## Examples

- [example configuration](retro.conf.json)
- [example CSV](example-plan.csv)
- [example custom theme](example-theme.json)
- [example PNG](example-plan.csv)
- example shell outputs
    
    ```
    tools/retro-planner% python csv2png.py
    [Info] Reading the theme file example-theme.json...
    [Info] Using "funky" in example-theme.json...
    [Info] Reading example-plan.csv...
    [Info] Converting example-plan.csv...
    [Info] Saving example-plan.csv into a picture...
    [Info] Finished conversion, output to ./.
    ```

    ```
    tools/retro-planner% python csv2png.py
    [Warning] Configuration file retro.conf.json not found, using the default configuration...
    To use a custom configuration, put "retro.conf.json" in the same directory as this script.

    Enter name/regex of the .csv file(s) without ".csv": example-.*
    [Info] No theme specified, using the default theme...
    [Info] Reading example-plan.csv...
    [Info] Converting example-plan.csv...
    [Info] Saving example-plan.csv into a picture...
    [Info] Finished conversion, output to ./.
    ```

    ```
    tools/retro-planner% python csv2png.py
    [Error] Output directory ./out does not exist!
    ```

    ```
    tools/retro-planner% python csv2png.py
    [Info] Reading the theme file example-theme.json...
    [Warning] Theme "mr.nothing" not found! Falling back to default theme...
    [Info] Reading example-plan.csv...
    [Info] Converting example-plan.csv...
    [Info] Saving example-plan.csv into a picture...
    [Info] Finished conversion, output to ./.
    ```
