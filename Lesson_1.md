# MOAA GPV データのダウンロードと読み込み、描画

## MOAA GPV データとは
[Argoフロート](https://www.jamstec.go.jp/argo/j/)のデータやその他利用可能な水温塩分データを、最適内挿法を用いて格子化したデータセット。[海洋研究開発機構（JAMSTEC）](https://www.jamstec.go.jp/j/)が作成・公開を行っている。英語名は Grid Point Value of the Monthly Objective Analysis using the Argo data。

MOAA GPV データの詳細は[ここ](https://www.jamstec.go.jp/argo_research/dataset/moaagpv/moaa_ja.html)を参照。2025年9月に ver2 が公開された。2025年10月現在、水温, 塩分が公開されている。本課題演習ではこの ver2 を解析に使用。
データセットは Argo フロートが展開された 2001 年からあるが、2005年ころまではフロート数が十分でない点に注意。

## MOAA GPV データのダウンロード
[ここ](https://pubargo.jamstec.go.jp/argo_product/catalog/moaagpv2/catalog.html)からダウンロード。データセットには速報性を重視した near real time （準リアルタイム）と遅れて収集されたデータも含む delayed mode （遅延モード）がある。課題演習ではどちらを使っても良いが、以下では遅延モードを想定。  
ファイルは年毎に MOAAv2_OI_20XX_MON.tar.gz ファイルにまとめられている。 ファイル拡張子が tar のファイルは複数のファイルを tar コマンドでまとめたファイル、拡張子が gz のファイルはgzipコマンドで圧縮したファイルを示すのが慣例。
ファイル名をクリック、開いたサイトの Access の HTTPServer をクリックしてダウンロード。

ダウンロードしたファイルを以下の tar コマンドで解凍・展開する。

``` tar xvfz ***.tar.gz```

上記 tar のオプションの意味は以下。 
- x:extraction（ファイルを取り出す。まとめるときは c を指定）
- v:verbose（ファイル情報を端末に出力する）
- f:file（おまじないと思って良い）
- z:gzip（gzip で圧縮・解凍）
各月毎のファイルが展開される。

## MOAA GPV データの読み込み
MOAA GPV データは [NETCDF](https://www.unidata.ucar.edu/software/netcdf) ファイル形式で格納されている。簡単に言うと、数値データだけでなくそのフォーマットもファイル内に記述されているファイル形式。気象・海洋分野の世界的標準形式になっている。fortran や python で読み込める。  
含まれているデータを知るには、以下の ncdump コマンドが便利。

```ncdump -h NETCDFデータ```

以下は出力結果。

```
dimensions:
        LONGITUDE = 360 ;
        LATITUDE = 142 ;
        PRES = 66 ;
        STRING16 = 16 ;
variables:
        int PRES(PRES) ;
                PRES:name = "PRES" ;
        char CDATE0(STRING16) ;
                CDATE0:name = "CDATE0" ;
        char DATASET_TYPE(STRING16) ;
                DATASET_TYPE:name = "DATASET_TYPE" ;
                DATASET_TYPE:long_name = "Dataset type" ;
        float SOI_ERR(PRES, LATITUDE, LONGITUDE) ;
                SOI_ERR:name = "SOI_ERR" ;
                SOI_ERR:FillValue = -10000.f ;
        float TOI_ERR(PRES, LATITUDE, LONGITUDE) ;
                TOI_ERR:name = "TOI_ERR" ;
                TOI_ERR:FillValue = -10000.f ;
        float LATITUDE(LATITUDE) ;
                LATITUDE:name = "LATITUDE" ;
        float LONGITUDE(LONGITUDE) ;
                LONGITUDE:name = "LONGITUDE" ;
        float SOI(PRES, LATITUDE, LONGITUDE) ;
                SOI:name = "SOI" ;
                SOI:FillValue = -10000.f ;
        float S_CLIM(PRES, LATITUDE, LONGITUDE) ;
                S_CLIM:name = "S_CLIM" ;
                S_CLIM:FillValue = -10000.f ;
        float TOI(PRES, LATITUDE, LONGITUDE) ;
                TOI:name = "TOI" ;
                TOI:FillValue = -10000.f ;
        float T_CLIM(PRES, LATITUDE, LONGITUDE) ;
                T_CLIM:name = "T_CLIM" ;
                T_CLIM:FillValue = -10000.f ;
        float S_STDEV(PRES, LATITUDE, LONGITUDE) ;
                S_STDEV:name = "S_STDEV" ;
                S_STDEV:FillValue = -10000.f ;
        float T_STDEV(PRES, LATITUDE, LONGITUDE) ;
                T_STDEV:name = "T_STDEV" ;
                T_STDEV:FillValue = -10000.f ;
```


- dimensions：データの格子数（配列数）  
  LONGITUDE：経度方向格子数、LATITUDE：緯度方向格子数、PRES：深度（圧力）方向格子数  
  STRING16：文字数（１６文字の文字変数として定義されている）
- variables：データの種類  
  int PRES(PRES) ：整数変数で名前がPRES（圧力 dbar）の１次元配列、格子数もPRES  
  char CDATE0(STRING16) ：文字変数で名前がCDATE0（解析日時の中央値）、文字数がSTRING16  
  char DATASET_TYPE(STRING16)：文字変数で名前がDATASET_TYPE（near real time か delayed modeか）、文字数がSTRING16
  float SOI_ERR(PRES, LATITUDE, LONGITUDE) ：実数変数で名前がSOI_ERR（最適内挿時の塩分推定誤差、PSS-78、psu）の３次元（経度、緯度、深度）配列、不定値は -10000.0 が入っている  
  float TOI_ERR：水温推定誤差（ITS90、℃）  
  float LATITUDE(LATITUDE)：字数変数で名前がLATITUDE（緯度）の１次元配列  
  float LONGITUDE：経度  
  float SOI：塩分の最適内挿値（PSS-78、psu）  
  float S_CLIM：塩分の気候値（WOA13の平均値＝最適内挿法での初期値）  
  float TOI：水温の最適内挿値（ITS90、℃）  
  float T_CLIM：水温の気候値  
  float S_STDEV：塩分の格子内観測値の標準偏差  
  float T_STDEV：水温の格子内観測値の標準偏差

python で読み込むには以下のようにすれば良い（１例）

```
import numpy as np
import xarray as xr

# read MOAA GPV data
file='MOAAv2_OI_TS_20240115_MON_100deg_5-2000db.nc'
nc = xr.open_dataset(file)

date = nc['CDATE0']
dtyp = nc['DATASET_TYPE']
lat = nc['LATITUDE'][:]
lon = nc['LONGITUDE'][:]
prs = nc['PRES'][:]
toi = nc['TOI'][:]
soi = nc['SOI'][:]
nc.close()
```

なお、fortran形式の配列格納順に慣れている人（私など）は以下のように転置しておくと良い。

```
# transpose (pres,lat,lon) (C style) -> (lon,lat,pres) (F style)
toi = toi.T
soi = soi.T
```

## MOAA GPV データの描画
例えば最浅層の水温を描画するには以下のようにすれば良い（１例）。

```
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime

# 地図描画のため
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.style as mplstyle
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# 座標の定義（fortran形式の場合）
X,Y = np.meshgrid(lon, lat, indexing = 'ij')  # indexing = 'ij' is F style

# set contour interval
tlev=np.arange(21)*2.-2.
slev=np.arange(21)*0.5+30.

# set depth level
k=0

fig, (figa, figb) = plt.subplots(figsize=(8,6),ncols=1,nrows=2,subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=210)))

gl = figa.gridlines(crs=ccrs.PlateCarree())
gl.xlocator = mticker.FixedLocator(np.arange(-180,180.1,30))
gl.ylocator = mticker.FixedLocator(np.arange(-75,75.1,15))

data=np.copy(toi[:,:,k])
#data=np.copy(toi[:,:,:].sel(PRES=5)) # xarray の sel 関数を使うことも可能
cf=figa.contourf(X,Y,data, transform=ccrs.PlateCarree(),cmap='jet',levels=tlev)
cbar=fig.colorbar(cf,ax=figa,shrink=0.8)
cbar.set_label('temp [C]')
cs = figa.contour(cf, transform=ccrs.PlateCarree(), colors = 'w', linewidths = 0.5)
cs.clabel(cs.levels[::2],fmt='%1.2f')
cbar.add_lines(cs)

figa.coastlines(linewidth=3)
figa.set_title('Temperature at {:5} m depth,  ('.format(prs[k])+str(date.astype('U16').values)+')')

figa.set_global()

data=np.copy(soi[:,:,k])
cf=figb.contourf(X,Y,data, transform=ccrs.PlateCarree(),cmap='jet',levels=slev)
cbar=fig.colorbar(cf,ax=figb,shrink=0.8)
cbar.set_label('salt')
cs = figb.contour(cf, transform=ccrs.PlateCarree(), colors = 'w', linewidths = 0.5)
cs.clabel(cs.levels[::2],fmt='%1.2f')
cbar.add_lines(cs)

figb.coastlines(linewidth=3)
figb.set_title('Salinity at {:5} m depth,  ('.format(prs[k])+str(date.astype('U16').values)+')')

figb.set_global()

fig.tight_layout()

fig.show()
# plt.show() # ipython ではなく python で実行するときはこちらを選択
```

<img src="https://github.com/kugi-yosikawa/DD2025/blob/main/2024_01_15.jpg">


### 作成した図のファイル保存
図をファイルに保存するには画面出力のところ ```fig.show()``` で以下を加える。
```
fig.savefig('ファイル名')
```
'ファイル名'のところは保存させるファイル名を書く。例えば'test.jpg'とするとjpeg形式で、'test.eps'とするとEPS形式で保存される。 

なお、ファイル名に深度や年月を含めると簡単に整理できる。例えば以下のようにすると、深度や年月をファイル名に含めることができる。
```
filename=str(date.astype('U16').values) # date を、Unicode形式16文字（U16）に変換（astype）し、値のみ取り出し（values）、ndarray から文字変数に変換（str）
filename=filename.replace('/','') # 文字列中の"/"を""に変換（削除）、（replace）
filename=filename[0:6] # 先頭の６文字のみ取り出し
filename='map_k{:02}'.format(k)+'date'+filename+'.jpg' # 整数 k を書式指定して文字変数に変換（'{:02}'.format()、２桁表示：１桁の場合は０埋め）し、文字変数をつなぎ合わせて（+）最終ファイル名（filename）を設定
fig.savefig(filename) 
```

### 読み込むデータの年月を自動で変える（ループさせる）

```
import datetime
from dateutil.relativedelta import relativedelta

# （設定）

#　最初の年月、最後の年月を指定
year_begin,month_begin=2024,1 # 最初
year_end,month_end=2024,3 # 最後

# datetime オブジェクトを設定
dt    =datetime.datetime(year_begin,month_begin,15) # 最初の年月、逐次更新される
dt_end=datetime.datetime(year_end  ,month_end  ,15) # 最後の年月

while True: # ずっとループ処理
    dt_str=dt.strftime('%Y%m') # 年月を文字変数（dt_str）に変換

    # read MOAA GPV data
    rfile='../DATA/MOAA/2024/MOAAv2_OI_TS_'+dt_str+'15_MON_100deg_5-2000db.nc'
    ncr = xr.open_dataset(rfile)

    # （データ読み込み）
    # （作図）

    if dt == dt_end : # dt_endになったらループを抜ける
        break
    dt=dt+relativedelta(months=1) # １月進める
```
