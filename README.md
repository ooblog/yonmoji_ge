# 「yonmoji_ge」は「約四文字」サイトジェネレータのPythonによる実装です。

[http://ooblog.github.io/](http://ooblog.github.io/)のPagesを検索エンジン風に構築してみた。  

## セットアップ方法(GitHub Pageを「約四文字」にする)

「username.github.io」フォルダの親フォルダに「yonmoji&#95;ge」フォルダを作る形でzipを解凍する。  
もしくは「yakuyon.tsv」の「&#42;siteconfig」内のパスを設定する。  
「yonmoji&#95;ge.tsv」の「username」項目を「username.github.io」に合わせる。  
とりあえず様子見の場合設定は最適化せず、あえて「oobog.github.io」フォルダにHT\MLが作成される様子を見てから判断する。
設定ファイル「[yonmoji_ge.tsv](yonmoji_ge.tsv)」などの解説は「[yonmoji_ge.txt](yonmoji_ge.txt)」を参考。  

## ファイルの編集。

    ┏yonmoji&#95;ge━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃｢     site      ｣                                  1        ┃
    ┃[yakuyon        ]━━━━━━━━━━━━━━━━━□[   1日┃
    ┃｢  page(HTML)   ｣                          3                ┃
    ┃[やくよん       ]━━━━━━━━━━━━━□━━━━[   3日┃
    ┃｢ rewrite(TSV)  ｣                  2                        ┃
    ┃[<?tagline?>    ]━━━━━━━━━□━━━━━━━━[   2日┃
    ┃[ <section>                                               □┃
    ┃[  <article>                                              ∩┃
    ┃[   <div class="yonmoji">                                 Ⅱ┃
    ┃[    <H2 class="yonmoji&#95;word">やく<br />よん</H2>         Ⅱ┃
    ┃[    <H3>「<dfn>約四文字(<abbr title="約四文字"><!pagenameⅡ┃
    ┃[    <br class="yonmoji&#95;both" />                          ∪┃
    ┃[   </div>                                                  ┃
    ┃[   <ol class="yonmoji&#95;kiketsushouten">                     ┃
    ┃[    <li>よくアニメとかドラマとかでググる時Google先生の代   ┃
    ┃[    <li>逆に架空の検索エンジンを作ってしまうのはどうだろ   ┃
    ┃[    <li>架空の検索エンジンだけどURLが存在していれば便乗フ  ┃
    ┃[    <li>フィッシングとは違うけど「電車男」劇中掲示板に似   ┃
    ┃[   </ol>                                                 □┃
    ┃[□⊂二二二二二二二二⊃                                 □  ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

入力欄は３つ。「site」「page&#40;HTML&#41;」「rewrite&#40;TSV&#41;」。  
「site」は作成するサイト、または階層内ディレクトリを選びます。  
「page&#40;HTML&#41;」は作成するHTMLページ名を入力します。空入力&#40;「.」のみなど無効なファイル名&#41;で日付&#40;yyyy-mm-dd&#41;の代入も可能です。  
「rewrite&#40;TSV&#41;」は置換replaceする項目を選びます。  

一度作成したファイルはシーク操作等で開く事が可能。保存しないでシークすると入力データは消えるので注意。  
「yakuyon/&#42;.tsv」などファイルを消す操作は無いので逆に初期化したい時は「yakuyon/&#42;.tsv」を削除して、ファイルが無い状態で入力欄で&#91;enter&#93;キー。  

## 入力項目の変更やサイトのテンプレ追加もできます。

初期設定では[「約四文字&#40;yakuyon&#41;」](http://ooblog.github.io/)を想定したサンプルを同梱してます。
設定ファイル「[yonmoji_ge.tsv](yonmoji_ge.tsv)」の編集方法など詳しい事は「[yonmoji_ge.txt](yonmoji_ge.txt)」の方に書いてます。  

## 「L:Tsv」は「yonmoji_ge」を動かすためのモジュール群です。

「L&#58;Tsv」モジュールの仕様は「[kantray](https://github.com/ooblog/LTsv9kantray)」の方の「[LTsv.txt](https://github.com/ooblog/LTsv9kantray/blob/master/LTsv.txt)」の方に書いてます。  

## 動作環境。

Python2.7.3(PuppyLinux571JP)およびPython3.4.3(Wine1.7.18)で動作を確認しています。  

## ライセンス・著作権など。

Copyright (c) 2016 ooblog  
License: MIT  
[https://github.com/ooblog/yonmoji_ge/blob/master/LICENSE](https://github.com/ooblog/yonmoji_ge/blob/master/LICENSE "https://github.com/ooblog/yonmoji_ge/blob/master/LICENSE")  
