# 海洋貯熱量の計算と描画
MOAAのデータを使って海洋貯熱量を計算し描画する。

## 海洋貯熱量の定義
単位面積あたりの海洋貯熱量（OHC \[J/m $^2$ \]）は以下で与えられる。  
OHC $= \int_D^0 \rho C_pT dz$  
ここで $\rho$ は海水密度（kg/m $^3$ ）、 $C_p$ は定圧比熱（J/kgK）、 $T$ は温度（K）で、 $D$ は貯熱量を求める水柱の下端深度（MOAAのデータでは2000ｍ）である。全貯熱量（TOHC）はこれに面積を乗じる。

## 海洋貯熱量の計算方法
[The Gibbs SeaWater (GSW) Oceanographic Toolbox of TEOS-10](https://www.teos-10.org/pubs/gsw/html/gsw_front_page.html) の各種ライブラリを使うと正確かつ簡単に計算できる。  
使用する関数は
+ gsw.SA_from_SP：実用塩分（PSS-78）、緯度・経度・圧力（水深）から絶対塩分を計算
+ gsw.CT_from_t：水温（ITS90）、絶対塩分、圧力がら保存水温を計算
+ gsw.enthalpy：絶対塩分、保存水温から単位質量あたりのエンタルピー（ $C_p T$ ）を計算
+ gsw.rho：絶対塩分、保存水温、圧力から海水密度（ $\rho$ ）を計算
の4つ。各関数の使い方は[GSW Toolbox のマニュアル](https://www.teos-10.org/pubs/gsw/html/gsw_contents.html)を参照のこと。

> 実用塩分とは、海水の電気伝導度から推定した海水の塩分であり、実際の塩分（絶対塩分：海水1kg中に含まれる塩素・臭素・ヨウ素の全量をgで表したもの、ただし臭素・ヨウ素は塩素に置換する）とは完全に一致しない。また、塩素・臭素・ヨウ素の比も海域・深度によって異なる。  
> 保存温度とは、断熱過程で保存される温度である。観測された温度（現場温度、ITS90）は深層の高水圧で圧縮されることでわずかに昇温している。この圧縮による昇温の効果を取り除くために導入されたのが温位（ポテンシャル温度）であるが、比熱 $C_p$ も圧力や塩分に依存するため、海水の内部エネルギー（エンタルピー）は保存していない。保存温度は、海水が断熱的に変化した場合にエンタルピーが保存されるように（比熱の変化も考慮して定義された）温度。  
> 実用塩分、保存温度の詳細は[ここ](https://www.nature.com/scitable/knowledge/library/key-physical-variables-in-the-ocean-temperature-102805293/)を参照。

具体的な計算手順は以下。
1. MOAAで提供されている水温（ITS90）、塩分（PSS-78）、圧力から、エンタルピーと海水密度を以下の手順で計算する。
   1. gsw.SA_from_SPを使って、実用塩分・緯度・経度・圧力から絶対塩分（SA）を計算
   2. gsw.CT_from_tを使って、水温・絶対塩分・圧力がら保存水温（CT）を計算
   3. gsw.enthalpyを使って、絶対塩分・保存水温・圧力からエンタルピー（ET）を計算
   4. gsw.rhoを使って、絶対塩分・保存水温・圧力から海水密度（RO）を計算
2. 基準深度（5m,10m,15m、・・・、1950m、2000m）で与えられた水温・塩分が代表する深度幅（DZ）を求める。具体的には、１層目は（0mから7.5mまでの）7.5m、２層目は（7.5mから12.5mまでの）5m、最深層は（1975mから2000mまでの）25m。
   1. 基準深度の中点を求める。
   2. 中点同士の距離を求め、配列DZに入力する。
   3. 最浅層・最深層に注意する。
3. RO\*ET\*DZ を鉛直に足し合わせて、各緯度経度での単位面積あたりの海洋貯熱量（OHC）を求める。
   1. np.sum
5. 各緯度経度における面積を乗じて足し合わせることで、全海洋貯熱量（TOHC）を求める。なお、緯度１度の距離は 111.194km である。（gsw.distance(\[0.,0.\],\[0.,1.\]) で求めることができる。）

注意とTips
+ OHCの計算に欠測値（水温、塩分が-10000となっている）を含めないこと。
+ 各緯度経度での計算を for loop で回すと時間がかかる（pythonの限界）。配列のままGSW関数の引数とすると早い。
+ 上記に関連して、正常値は1、欠測値は0となるようなマスク配列を作っておくと便利。   
```
im,jm,km=toi.values.shape
mask=np.ones([im,jm,km])
mask[toi.values == -10000.]=0.
mask[soi.values == -10000.]=0.
```
+ lat,lon も３次元配列を用意すると良い。
```
LON_3D=np.zeros([im,jm,km])  
for i in range(im) :
    LON_3D[i,:,:]=lon.values[i]
```

## 空間分布の描画と時系列の描画

OHCの水平分布と、TOHCの時系列を描画する。 時系列をTrenberthと比較する。
```
TOHC=[]
while True :
    データ読み込み   
    fig,figa=plt.subplots()   
    data=np.copy(OHC)   
    figa.contourf(X,Y,data)
    plt.close()
    TOHC=np.append(TOHC,np.sum(OHC*面積))
fig,figa=plt.subplots()
figa.plot(TOHC)
```
