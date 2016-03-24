# 「yonmoji_ge」は「約四文字(yonmoji)」サイトジェネレータのPythonによる実装です。

[http://ooblog.github.io/](http://ooblog.github.io/)のPages構築を検索エンジン風に構築してみた。  

## セットアップ方法(GitHub Pageを「約四文字」にする)

「[.gitignore](.gitignore)」ファイルに「yonmoji&#95;ge/」フォルダを追加しておく(リポジトリ混入回避)。  
「yonmoji&#95;ge/」フォルダの中に「yonmoji&#95;ge.py」などの実行環境をコピー。  
「[yonmoji_ge.py](yonmoji_ge.py)」でページ保存すると「index,html」がリポジトリのルートにできてるか確認。  
設定ファイル「[yonmoji_ge.tsv](yonmoji_ge.tsv)」の解説は「[yonmoji_ge.txt](yonmoji_ge.txt)」を参考。  

## ファイルの編集。

    ┏yonmoji&#95;ge━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃｢     save      ｣                                  3        ┃
    ┃[よんもじ       ]━━━━━━━━━━━━━━━━━□[   1日┃
    ┃   <?title?>    [ <title><?pagename?>-「約四文字」(<?userna]┃
    ┃                [  <span> &#62; <mark><?pagename?></mark><□┃
    ┃<?breadcrumbs?> [  <span class="yonmoji&#95;gesitemap"><a href="□┃
    ┃                [□⊂二二二二二二二二⊃                 □  ┃
    ┃                [ <section>                               □┃
    ┃                [  <article>                              ∩┃
    ┃                [   <div class="yonmoji">                 ∪┃
    ┃  <?tagline?>   [    <H1 class="yonmoji&#95;word">よん<br />も  ┃
    ┃                [    <H2>「約四文字」は架空の検索エンジン   ┃
    ┃                [    <br class="yonmoji&#95;both" />          □┃
    ┃                [□⊂二二二二二二二二⊃                 □  ┃
    ┃                [ <section>                               □┃
    ┃                [  <article>                              ∩┃
    ┃                [   <H2>サンプルページ。</H2>             Ⅱ┃
    ┃   <?links?>    [   <dl>                                  ∪┃
    ┃                [    <dt><a href="とりせつ.html" title="と  ┃
    ┃                [    <dd>「約四文字」の「取扱説明書」略し □┃
    ┃                [□⊂二二二二二二二二⊃                 □  ┃
    ┃  <?pagename?>  [よんもじ                                  ]┃
    ┃  <?username?>  [ooblog                                    ]┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

左上の入力欄にはファイル名を入力します。空入力(文字列長さ0もしくは「.」のみ)すると日付(yyyy-mm-dd)がページ名になります。  
入力欄で&#91;Enter&#93;キーを押すと初期設定を読み込みます。「pages/&#42;.tsv」があると設定を読み込みます。  
「save」ボタンを押すと「pages/&#42;.tsv」と「../&#42;.html」、上記の例だと「index.tsv」「index.html」を上書き保存します。  
ベースとなるHTMLテキスト内のタグ(左側の「&#60;&#63;〜&#63;&#62;」)を右側の入力に置換replaceする方法で個々のページを編集するスタイルです。  
一度作成したファイルはシーク操作で開く事が可能。保存しないでシークすると入力データは消えるので注意。  

「pages/&#42;.tsv」を消す操作は無いので初期化したい時は「pages/&#42;.tsv」を削除して、ファイルが無い状態で入力欄で&#91;enter&#93;キー。  

## 入力項目タグは変更できます。

設定ファイル「[yonmoji_ge.tsv](yonmoji_ge.tsv)」の編集方法など詳しい事は「[yonmoji_ge.txt](yonmoji_ge.txt)」の方に書いてます。  

## 「L:Tsv」はアプリを作るためのモジュール群です。

LTSVモジュールの仕様は「[kantray](https://github.com/ooblog/LTsv9kantray)」の方の「[LTsv.txt](https://github.com/ooblog/LTsv9kantray/blob/master/LTsv.txt)」の方に書いてます。  

## 動作環境。

Python2.7.3(PuppyLinux571JP)およびPython3.4.3(Wine1.7.18)で動作を確認しています。  

## ライセンス・著作権など。

Copyright (c) 2016 ooblog  
License: MIT  
[https://github.com/ooblog/LTsv9kantray/blob/master/LICENSE](https://github.com/ooblog/LTsv9kantray/blob/master/LICENSE "https://github.com/ooblog/LTsv9kantray/blob/master/LICENSE")  
