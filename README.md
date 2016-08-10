<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>基于Flask的项目管理网站</title>
</head>
<body>
<div style="visibility: hidden; overflow: hidden; position: absolute; top: 0px; height: 1px; width: auto; padding: 0px; border: 0px none; margin: 0px; text-align: left; text-indent: 0px; text-transform: none; line-height: normal; letter-spacing: normal; word-spacing: normal;"><div id="MathJax_SVG_Hidden"></div><svg><defs id="MathJax_SVG_glyphs"><path d="M492 213Q472 213 472 226Q472 230 477 250T482 285Q482 316 461 323T364 330H312Q311 328 277 192T243 52Q243 48 254 48T334 46Q428 46 458 48T518 61Q567 77 599 117T670 248Q680 270 683 272Q690 274 698 274Q718 274 718 261Q613 7 608 2Q605 0 322 0H133Q31 0 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q146 66 215 342T285 622Q285 629 281 629Q273 632 228 634H197Q191 640 191 642T193 659Q197 676 203 680H757Q764 676 764 669Q764 664 751 557T737 447Q735 440 717 440H705Q698 445 698 453L701 476Q704 500 704 528Q704 558 697 578T678 609T643 625T596 632T532 634H485Q397 633 392 631Q388 629 386 622Q385 619 355 499T324 377Q347 376 372 376H398Q464 376 489 391T534 472Q538 488 540 490T557 493Q562 493 565 493T570 492T572 491T574 487T577 483L544 351Q511 218 508 216Q505 213 492 213Z" stroke-width="1" id="MJMATHI-45"></path><path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" stroke-width="1" id="MJMAIN-3D"></path><path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" stroke-width="1" id="MJMATHI-6D"></path><path d="M34 159Q34 268 120 355T306 442Q362 442 394 418T427 355Q427 326 408 306T360 285Q341 285 330 295T319 325T330 359T352 380T366 386H367Q367 388 361 392T340 400T306 404Q276 404 249 390Q228 381 206 359Q162 315 142 235T121 119Q121 73 147 50Q169 26 205 26H209Q321 26 394 111Q403 121 406 121Q410 121 419 112T429 98T420 83T391 55T346 25T282 0T202 -11Q127 -11 81 37T34 159Z" stroke-width="1" id="MJMATHI-63"></path><path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" stroke-width="1" id="MJMAIN-32"></path><path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" stroke-width="1" id="MJSZ1-2211"></path><path d="M21 287Q22 293 24 303T36 341T56 388T89 425T135 442Q171 442 195 424T225 390T231 369Q231 367 232 367L243 378Q304 442 382 442Q436 442 469 415T503 336T465 179T427 52Q427 26 444 26Q450 26 453 27Q482 32 505 65T540 145Q542 153 560 153Q580 153 580 145Q580 144 576 130Q568 101 554 73T508 17T439 -10Q392 -10 371 17T350 73Q350 92 386 193T423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 180T152 343Q153 348 153 366Q153 405 129 405Q91 405 66 305Q60 285 60 284Q58 278 41 278H27Q21 284 21 287Z" stroke-width="1" id="MJMATHI-6E"></path><path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" stroke-width="1" id="MJMATHI-69"></path><path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" stroke-width="1" id="MJMAIN-31"></path><path d="M33 157Q33 258 109 349T280 441Q331 441 370 392Q386 422 416 422Q429 422 439 414T449 394Q449 381 412 234T374 68Q374 43 381 35T402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487Q506 153 506 144Q506 138 501 117T481 63T449 13Q436 0 417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157ZM351 328Q351 334 346 350T323 385T277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q217 26 254 59T298 110Q300 114 325 217T351 328Z" stroke-width="1" id="MJMATHI-61"></path><path d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z" stroke-width="1" id="MJMAIN-30"></path></defs></svg></div><div id="wmd-preview" class="wmd-preview"><div class="md-section-divider"></div><div class="md-section-divider"></div><h1 id="基于flask的项目管理网站" data-anchor-id="1y8z">基于Flask的项目管理网站</h1><hr><div class="md-section-divider"></div><h2 id="注意" data-anchor-id="m0bo">注意</h2><p data-anchor-id="1x20">还未完工.....</p><div class="md-section-divider"></div><h2 id="介绍" data-anchor-id="9ec3">介绍</h2><p data-anchor-id="1cd8">此项目利用了python的微框架Flask，目前使用关系型数据库SQLite出储存项目信息。</p><div class="md-section-divider"></div><h4 id="基本功能" data-anchor-id="7pxb">基本功能：</h4><ul data-anchor-id="cnhu">
<li>用户登录注册</li>
<li>项目新建、提交、进度</li>
</ul><div class="md-section-divider"></div><h2 id="模型" data-anchor-id="2d0c">模型</h2><ul data-anchor-id="jmbl">
<li>USER</li>
</ul><table class="table table-striped-white table-bordered" data-anchor-id="8r4f">
<thead>
<tr>
 <th>列名</th>
 <th style="text-align:center;">类型</th>
 <th style="text-align:right;">说明</th>
</tr>
</thead>
<tbody><tr>
 <td>id</td>
 <td style="text-align:center;">Interger</td>
 <td style="text-align:right;">工号</td>
</tr>
<tr>
 <td>name</td>
 <td style="text-align:center;">String(40)</td>
 <td style="text-align:right;">用户名</td>
</tr>
<tr>
 <td>passwd</td>
 <td style="text-align:center;">String(128)</td>
 <td style="text-align:right;">密码</td>
</tr>
<tr>
 <td>admin</td>
 <td style="text-align:center;">Boolean</td>
 <td style="text-align:right;">管理权限</td>
</tr>
<tr>
 <td>image_url</td>
 <td style="text-align:center;">String(500)</td>
 <td style="text-align:right;">头像</td>
</tr>
<tr>
 <td>create_at</td>
 <td style="text-align:center;">DateTime</td>
 <td style="text-align:right;">创建时间</td>
</tr>
<tr>
 <td>projects</td>
 <td style="text-align:center;">relationship</td>
 <td style="text-align:right;">指向PROJECT</td>
</tr>
</tbody></table><p data-anchor-id="oucs">* PROJECT</p><table class="table table-striped-white table-bordered" data-anchor-id="lhcu">
<thead>
<tr>
 <th>列名</th>
 <th style="text-align:center;">类型</th>
 <th style="text-align:right;">说明</th>
</tr>
</thead>
<tbody><tr>
 <td>id</td>
 <td style="text-align:center;">String(50)</td>
 <td style="text-align:right;">项目ID</td>
</tr>
<tr>
 <td>name</td>
 <td style="text-align:center;">String(40)</td>
 <td style="text-align:right;">项目名</td>
</tr>
<tr>
 <td>content</td>
 <td style="text-align:center;">Text</td>
 <td style="text-align:right;">项目简介</td>
</tr>
<tr>
 <td>status</td>
 <td style="text-align:center;">Boolean</td>
 <td style="text-align:right;">状态</td>
</tr>
<tr>
 <td>create_at</td>
 <td style="text-align:center;">String(500)</td>
 <td style="text-align:right;">创建时间</td>
</tr>
<tr>
 <td>finish_at</td>
 <td style="text-align:center;">DateTime</td>
 <td style="text-align:right;">完成时间</td>
</tr>
<tr>
 <td>excepted_finish_time</td>
 <td style="text-align:center;">DateTime</td>
 <td style="text-align:right;">完成时间</td>
</tr>
<tr>
 <td>create_id</td>
 <td style="text-align:center;">Interger</td>
 <td style="text-align:right;">创建人 指向USER</td>
</tr>
<tr>
 <td>steps</td>
 <td style="text-align:center;">relationship</td>
 <td style="text-align:right;">步骤 指向STEP</td>
</tr>
</tbody></table><ul data-anchor-id="31k8">
<li>STEP</li>
</ul><table class="table table-striped-white table-bordered" data-anchor-id="al0j">
<thead>
<tr>
 <th>列名</th>
 <th style="text-align:center;">类型</th>
 <th style="text-align:right;">说明</th>
</tr>
</thead>
<tbody><tr>
 <td>id</td>
 <td style="text-align:center;">String(50)</td>
 <td style="text-align:right;">步骤ID</td>
</tr>
<tr>
 <td>content</td>
 <td style="text-align:center;">Text</td>
 <td style="text-align:right;">步骤简介</td>
</tr>
<tr>
 <td>status</td>
 <td style="text-align:center;">Boolean</td>
 <td style="text-align:right;">状态</td>
</tr>
<tr>
 <td>create_at</td>
 <td style="text-align:center;">String(500)</td>
 <td style="text-align:right;">创建时间</td>
</tr>
<tr>
 <td>finish_at</td>
 <td style="text-align:center;">DateTime</td>
 <td style="text-align:right;">完成时间</td>
</tr>
<tr>
 <td>project_id</td>
 <td style="text-align:center;">Interger</td>
 <td style="text-align:right;">所属项目 指向PROJECT</td>
</tr>
</tbody></table><div class="md-section-divider"></div><h3 id="暂未解决的问题" data-anchor-id="o51a">暂未解决的问题☑</h3>
<p data-anchor-id="kp3j">邀请成员加入功能--已经解决 ☑2016/8/10</p><p data-anchor-id="kp3j">如何与git服务器交互，同步git上的commit数据--已解决2016/8/10☑</p>
<p data-anchor-id="kp3j">历史项目</p>
<p data-anchor-id="kp3j">完成备注</p>
<p data-anchor-id="kp3j">管理part</p></div>

</body>
</html>