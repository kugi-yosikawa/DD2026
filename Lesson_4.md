# 主成分分析（Principal Component Analysis）／経験直交関数（Empirical Orthogonal Function）展開

## 主成分分析とは

自然現象に含まれる様々な変動を（ある基準をもとに）成分に分解することで、主要な（卓越する）変動成分を抽出する統計手法。大気海洋分野では経験直行関数展開とも呼ばれる。

## 考え方の基本

+ 空間構造パターン（モード）をもとに成分に分解
  + 異なる空間構造を持つ成分（モード）に分解
  + 分解された各成分（モード）は空間構造を保ったまま振幅が時間変化
+ 観測データは成分（モード）の重ね合わせ（線型結合）
+ 観測される変動強度（分散）への寄与率（モードの変動強度／全体の変動強度）に基づいてモードを順位付け
+ 変動の力学などは考慮しない・データに100%頼る

## 応用

+ 複雑な変動から主要な変動を抽出
  + それが物理・力学過程の抽出につながる場合もある（力学に基づいていないのでつながらない場合もある）
+ 将来の予測
+ 

## 準備

### 定義

時刻 $n$ 、地点 $l$ で観測される変数を $x_{nl}$ （ $n=1-N$ 、 $l=1-L$ ）とする。ある地点 $l$ における観測データ $x_{nl}$ の時間に関する平均、分散、標準偏差、規格化を以下のように表記する。

平均：
```math
\begin{align}
& \overline{x}^{n}_l \equiv \frac{1}{N}\sum_n x_{nl}
\end{align}
```

分散（変動強度を表す指標）：
```math
\begin{align}
& s^{2}_l \equiv \frac{1}{N}\sum_n (x_{nl}- \overline{x}^n_l)^2
\end{align}
```

標準偏差（変動強度を表す指標）：
```math
\begin{align}
& s_l \equiv \sqrt{ \frac{1}{N}\sum_n (x_{nl}- \overline{x}^n_l)^2 }
\end{align}
```

規格化変数：
```math
\begin{align}
& \check{x}_{nl} \equiv \frac{x_{nl}-\overline{x}^n_l}{s_l}
\end{align}
```

共分散（共変強度を表す指標）：
```math
\begin{align}
& c_{12} \equiv \frac{1}{N}\sum_n (x_{n1}-\overline{x}^n_1)(x_{n2}-\overline{x}^n_2)   \\  
& c_{11} = s^2_1
\end{align}
```

相関係数（共変強度を表す指標）：
```math
\begin{align}
r_{12} & \equiv \frac{c_{12}}{s_1s_2} \\
& = \frac{1}{N}\sum_n \frac{x_{n1}-\overline{x}^n_1}{s_1}\frac{x_{n2}-\overline{x}^n_2}{s_2}\\
& =\frac{1}{N}\sum_n \check{x}_{n1}\check{x}_{n2}
\end{align}
```

### 共分散のイメージ

分散は変動の強度指標、共分散は共変動の強度指標

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/scatter.jpg">

左から、正の共変関係のある、ほとんど共変関係の無い、負の共変関係のある、２つのデータの組。それぞれの分散値はグラフの上に記してある。

## 主成分分析：２地点データの場合の例

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/obsdat_sct.png">

例えば京都と東京の気温の時系列。横軸に京都の気温、縦軸に東京の気温を取ると、上の図のように（多分）なる。図からは、主要な特徴として

+ 京都の気温が高いときは東京の気温も高い時が多い
+ 京都の気温変化の方が、東京の気温変化よりも大きい（２倍くらい）

が読み取れる。ただし、主要な特徴からのズレも存在する（例えば第３象限に位置するデータ）。

言い換えると、観測される変動のうち、”主要な”変動は右上向きの赤線（傾きはおよそ1/2）軸（主軸）に沿う方向の変動、”ズレの”変動は左上向きの赤線軸（副軸）に沿う方向の変動。

これを変動強度（分散）を用いて以下のように定量的に表現するのが主成分分析。

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/PCA_image.png">

+ 時刻 $n$ での変動 $(x_{n1},x_{n2})$ を、主軸と副軸の成分を用いて、 $(y_{n1},y_{n2})$ で表現することを試みる。この際、時刻 $n$ での全変動強度を変えないように $y_{nl}$ を定義する。
```math
\begin{align}
& x_{n1}^2+x_{n2}^2=y_{n1}^2+y_{n2}^2
\end{align}
```

  全変動強度も不変（ $\sum_n \sum_l x_{nl}^2 = \sum_n \sum_l y_{nl}^2$ ）に注意
+ 主軸を $\sum_n y_{n1}^2$ が最大となる軸と定義
+ 副軸を それに直交する軸と定義

## 主成分分析：一般化

### 準備

観測値：
```math
x_{nl}, n=1-N（観測時刻数）, l=1-L（観測地点数）
```  
ただし各地点での時間平均値 $\overline{x}^n_l$ は予め差し引いておく。

ある時刻 $n$ での観測値：
```math
\begin{align}
& \boldsymbol{x}_n^T=\left( x_{n1}, x_{n2}, \cdots, x_{nL} \right)
\end{align}
```

ある地点 $l$ での観測値：
```math
\begin{align}
& \boldsymbol{x}_l = \begin{pmatrix}
  x_{1l}\
  x_{2l}\
  \vdots\
  x_{Nl}\
  \end{pmatrix}
\end{align}
```

主成分（主軸・第一モード）の空間構造：
```math
\begin{align}
& \boldsymbol{y}=\begin{pmatrix}
y_1\
y_2\
\vdots\
y_L
\end{pmatrix}
\\  
& \boldsymbol{y}^T\boldsymbol{y}=1
\end{align}
```

時刻 $n$ での観測値 $x_{nl}$ と主成分構造 $y_l$ の内積値（主軸への射影成分）：
```math
\begin{align}
\boldsymbol{x}_n^T\boldsymbol{y} & =x_{n1}y_1+x_{n2}y_2+\cdots+x_{nL}y_L \\
& \equiv a_n \\
\end{align}
```

主成分（第一モード）で評価した時刻 $n$ での分散：
```math
\begin{align}
& a_n^2
\end{align}
```

### 主成分（主軸、第一モード）の定義：直感的定義と数学的定義

主成分分析における主成分の定義： 
+ データが最も広がっている方向（＝分散が最も大きくなる軸）：直感的定義
+ $\boldsymbol{y}^T\boldsymbol{y}=1$ の条件で $\sum_n a_n^2$ を最大とする $\boldsymbol{y}$ ：数学的定義 

観測行列：
```math
\begin{align}
& \mathbf{X} \equiv (\boldsymbol{x}_1,\boldsymbol{x}_2,\cdots,\boldsymbol{x}_L)=\begin{pmatrix}
x_{11} & x_{12} & \cdots & x_{1L} \
x_{21} & x_{22} & \cdots & x_{2L} \
\vdots & \vdots & \ddots & \vdots \
x_{N1} & x_{N2} & \cdots & x_{NL} \
\end{pmatrix}
\end{align}
```

共分散行列（半正値対称行列）：
```math
\begin{align}
& \mathbf{C}=\mathbf{X}^T\mathbf{X}=\begin{pmatrix}
x_{11} & x_{21} & \cdots & x_{N1} \
x_{12} & x_{22} & \cdots & x_{N2} \
\vdots & \vdots & \ddots & \vdots \
x_{1L} & x_{2L} & \cdots & x_{NL} \
\end{pmatrix}\begin{pmatrix}
x_{11} & x_{12} & \cdots & x_{1L} \
x_{21} & x_{22} & \cdots & x_{2L} \
\vdots & \vdots & \ddots & \vdots \
x_{N1} & x_{N2} & \cdots & x_{NL} \
\end{pmatrix}=\begin{pmatrix}
c_{11} & c_{12} & \cdots & c_{1L} \
c_{21} & c_{22} & \cdots & c_{2L} \
\vdots & \vdots & \ddots & \vdots \
c_{L1} & c_{L2} & \cdots & c_{LL} \
\end{pmatrix}
\end{align}
```

内積ベクトル：
```math
\begin{align}
\boldsymbol{a} & \equiv \begin{pmatrix}
a_1 \
a_2 \
\vdots \
a_N
\end{pmatrix} = \begin{pmatrix}
x_{11} y_1+x_{12}y_2+ \cdots +x_{1L}y_L \
x_{21} y_1+x_{22}y_2+ \cdots +x_{2L}y_L \
\vdots \
x_{N1} y_1+x_{N2}y_2+ \cdots +x_{NL}y_L
\end{pmatrix} \\
& = \begin{pmatrix}
x_{11} & x_{12} & \cdots & x_{1L} \
x_{21} & x_{22} & \cdots & x_{2L} \
\vdots & \vdots & \ddots & \vdots \
x_{N1} & x_{N2} & \cdots & x_{NL} \
\end{pmatrix} \begin{pmatrix}
y_1\
y_2\
\vdots \
y_L\
\end{pmatrix}=\mathbf{X}\boldsymbol{y}
\end{align}
```

内積２乗和：
```math
\begin{align}
& \boldsymbol{a}^T\boldsymbol{a}=(X\boldsymbol{y})^TX\boldsymbol{y}=\boldsymbol{y}^T\mathbf{X}^T\mathbf{X}\boldsymbol{y}=\boldsymbol{y}^T\mathbf{C}\boldsymbol{y}
\end{align}
```

主成分の数学的再定義： $\boldsymbol{y}^T\boldsymbol{y}=1$ の条件のもと $\boldsymbol{a}^T\boldsymbol{a}=\boldsymbol{y}^T\mathbf{C}\boldsymbol{y}$ が最大となる $\boldsymbol{y}$ 


### 主成分（主軸、第一モード）の導出

ラグランジュの未定乗数法
```math
\begin{align}
J &=\boldsymbol{y}^T{C}\boldsymbol{y}
-\lambda \left(\boldsymbol{y}^T\boldsymbol{y}-1\right) \\
&=(y_1,y_2,\cdots,y_L)
\begin{pmatrix}
c_{11} & c_{12} & \cdots & c_{1L} \
c_{21} & c_{22} & \cdots & c_{2L} \
\vdots & \vdots & \ddots & \vdots \
c_{L1} & c_{L2} & \cdots & c_{LL} \
\end{pmatrix}
\begin{pmatrix}
y_1\
y_2\
\vdots\
y_L\
\end{pmatrix}
-\lambda \left(y_1^2+y_2^2+\cdots +y_L^2-1\right) \\
<!--
&=(y_1,y_2,\ldots,y_L)
\begin{pmatrix}
\sum_{l=1}^Lc_{1l}y_l \\
\sum_{l=1}^Lc_{2l}y_l \\
\vdots \\
\sum_{l=1}^Lc_{Ll}y_l \\
\end{pmatrix}
-\lambda \left(y_1^2+y_2^2+\cdots +y_L^2-1\right) \\
-->
&=y_1\sum_{l=1}^Lc_{1l}y_l+y_2\sum_{l=1}^Lc_{2l}y_l+\cdots+
y_L\sum_{l=1}^Lc_{Ll}y_l
-\lambda \left(y_1^2+y_2^2+\cdots +y_L^2-1\right) 
\end{align}
```

$J$ が最大となる条件
```math
\begin{align}
\frac{\partial J}{\partial y_i} &=
2\sum_{l=1}^Lc_{il}y_l-2\lambda y_i=
2\left(\sum_{l=1}^Lc_{il}y_l-\lambda y_i\right)=
2\left(\mathbf{C}\boldsymbol{y}-\lambda \boldsymbol{y}\right) \text{ for all } i
\end{align}
```
$\boldsymbol{y}$ の満たすべき条件
```math
\begin{align}
\mathbf{C}\boldsymbol{y}-\lambda \boldsymbol{y} &=0 
\end{align}
```

求める $\boldsymbol{y}$ は $\mathbf{C}$ の（固有値 $\lambda$ に対応する）固有ベクトル
```math
\begin{align}
\boldsymbol{a}^T\boldsymbol{a} &=\boldsymbol{y}^T\mathbf{C}\boldsymbol{y} =\lambda\boldsymbol{y}^T\boldsymbol{y} =\lambda
\end{align}
```
固有値 $\lambda$ は $\boldsymbol{a}^T\boldsymbol{a}$ 

すなわち主成分（第一モード）は 共分散行列 $C$ の最大固有値に対応する固有ベクトル

### 共分散行列の数学的性質（補足）

共分散行列 $\mathbf{C}$ は $(L\times L)$ の半正値対称行列（エルミート行列）
+ 固有値は（重複も含めて） $L$ 個存在し全て非負（零以上）
```math
\begin{align}
& \lambda^m \ge 0 \textrm{ for } m=1\sim L
\end{align}
```
+ 対応する固有ベクトルは互いに直交
```math
\begin{align}
& (\boldsymbol{y}^m)^T\boldsymbol{y}^n =
\begin{cases}
1 & \textrm{ for } m=n \\
0 & \textrm{ for } m\ne n
\end{cases}
\end{align}
```

以下では固有ベクトルの番号（モード番号） $m$ を固有値の大きい順とする
```math
\begin{align}
& \mathbf{C}\boldsymbol{y}^1=\lambda^1\boldsymbol{y}^1 \\
& \mathbf{C}\boldsymbol{y}^2=\lambda^2\boldsymbol{y}^2 \\
      &\vdots
\end{align}
```

$m$ 番目の固有ベクトル、固有値を $\boldsymbol{y}^m$ 、 $\lambda^m$ で表現

数学的関係式
```math
\begin{align}
&\mathbf{Y} \equiv(\boldsymbol{y}^1,\boldsymbol{y}^2,\cdots,\boldsymbol{y}^L) \textrm{（定義）}\\
&\mathbf{Y}^T\mathbf{Y} =I \text{（単位行列）}\\
&\mathbf{C} = \mathbf{Y}
\begin{pmatrix}
\lambda^1 & 0         & \cdots    & 0       \
0         & \lambda^2 &           & \vdots  \
\vdots    &           & \ddots    & 0       \
0         & \cdots    & 0         & \lambda^L
\end{pmatrix}\mathbf{Y}^T \text{（直交化）}\\
\end{align}
```

### 主成分（第一モード）で表される変動
```math
\begin{align}
\boldsymbol{a}^1\boldsymbol{y}^{1T} &=
\begin{pmatrix}
a^1_1y^1_1 & a^1_1y^1_2 & \cdots & a^1_1y^1_L \
a^1_2y^1_1 & a^1_2y^1_2 & \cdots & a^1_2y^1_L \
\vdots      & \vdots      & \ddots & \vdots   \
a^1_Ny^1_1 & a^1_Ny^1_2 & \cdots & a^1_Ny^1_L
\end{pmatrix}
\end{align}
```

### 主成分以外の変動
```math
\begin{align}
& \mathbf{X}^\dagger \equiv \mathbf{X}-\boldsymbol{a}^1\boldsymbol{y}^{1T} \\
& \mathbf{C}^\dagger \equiv \mathbf{X}^{\dagger T}\mathbf{X} = \mathbf{Y}^T \mathbf{A}^{\dagger T} \mathbf{A}^\dagger \mathbf{Y} = \mathbf{Y}^T
\begin{pmatrix}
0         & 0         & \cdots    & 0       \
0         & \lambda^2 &           & \vdots  \
\vdots    &           & \ddots    & 0       \
0         & \cdots    & 0         & \lambda^L
\end{pmatrix}\mathbf{Y}^T
\end{align}
```

第２モードは観測共分散行列の２番目に大きい固有値に対応する固有ベクトル

第 $m$ モードは観測共分散行列の $m$ 番目に大きい固有値に対応する固有ベクトル

### 主成分の特性
+ 主成分の分散の和＝共分散行列のトレース
+ 各モードは空間的に独立
  （固有ベクトルが直交）
+ 振幅の時系列 $\boldsymbol{a}$ も独立
```math
\begin{align}
\boldsymbol{a}^{mT}\boldsymbol{a}^n &=
\boldsymbol{y}^{mT}\mathbf{X}^T\mathbf{X}\boldsymbol{y}^n 
=\boldsymbol{y}^{mT}\mathbf{C}\boldsymbol{y}^n
=\boldsymbol{y}^{mT}\lambda^n\boldsymbol{y}^n =\begin{cases}
\lambda_m & \textrm{for} \ \ m=n \\
0 & \textrm{for} \ \ m\ne n
\end{cases}
\end{align}
```
（データ解析風に言い替えると、主成分分析で得られた各モードは無相関）

主成分分析で抽出したモードは、空間的・時間的に独立


### 主成分分析の用語

| 一般表記 | 吉川の言い方 | 英語表記 | 数学表記 | 意味 |
| :---:   | :---:      | :---:   | :---: | :---: |
| 主成分 | | Principal Component | | |
| 結合係数数 | 構造関数| Loading | $\boldsymbol{y}^m=(y_1^m,y_2^m,\cdots,y_L^m)$ | 各成分の空間構造 |
| 主成分得点 | 振幅 | Score | $\boldsymbol{a}^m=(a_1^m,a_2^m,\cdots,a_N^m)$ | 各成分の振幅 |
| 寄与率 | | Proportion | $\frac{\lambda^m}{\sum_{m=1}^M\lambda^m}$ | モードの説明分散比 |
| 累積寄与率 | | Cummulative Proportion | $\frac{\sum_{m=1}^m\lambda^m}{\sum_{m=1}^M\lambda^m}$ | そのモードまでの累積説明分散比 |

## 主成分の具体的計算方法

1. 観測行列の作成
2. 共分散行列の作成
3. 共分散行列の固有値（寄与率）固有ベクトル（構造ベクトル）計算
4. 主成分得点（振幅時系列）＝観測行列✕構造ベクトルの計算

## サンプル

pythonの[サンプルコード](https://github.com/kugi-yosikawa/DD2025/blob/main/pca_onedim_sample.py) は２地点の時間変動データの主成分分析を行うコードを例とする。このコードでは、以下の動画のように２地点で変動するデータ（例えば京都と東京の気温のようなデータ、コードの中で適当に作成したデータ）を主成分分析する。

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/obsdat.gif">

サンプルコードで出力される、観測データの時系列表示、散布図（＋主成分構造）表示、主成分振幅の時系列表示を以下に示す

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/obsdat_timser.jpg">

観測データの時系列（赤：地点１の時系列、青：地点２の時系列）

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/obsdat_scattr.jpg">

観測データの散布図（横軸：地点１の観測値、縦軸：地点２の観測値）と主成分分析で得られた第一モード（赤線）と第２モード（青線）の構造関数

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/scores_timser.jpg">

第一モード振幅（赤線）と第２モード振幅（青線）の時系列
