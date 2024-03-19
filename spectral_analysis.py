#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:28:10 2024
@author: ekaterinasivokon
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
from itertools import islice
import numpy as np
import math

DIRECTORY = "/Users/ekaterinasivokon/Desktop/Harvard Cohen Lab/fluorescence-microscope-spectra-analysis/Spectra_Data"
DIRECTORY_EXC = "/Users/ekaterinasivokon/Desktop/Harvard Cohen Lab/fluorescence-microscope-spectra-analysis/excel_spectra_data"
# =============================================================================
# # Dichroics Spectra 350 - 750 nm
# dichr = "5323-ascii.txt" #T612lpxr
# # Emission Filters Spectra 350 - 750 nm
# em = "5085-ascii.txt" #ET640_30x
# # Excitation Filters Spectra 350 - 750 nm
# exc = "5750-ascii.txt" #ET590_33m
# =============================================================================

# intensity data from web digitizer
amber_led_intensity = '''
380, 0.200483645887104
380.5, 0.10402768183473654
381, 0.10023314446978304
381.5, 0.10023672704890885
382, 0.10024184593056873
382.5, 0.10024179246774167
383, 0.10024202104683866
383.5, 0.100269157315239
384, 0.10004593010272345
384.5, 0.07015613119708064
385, 0.049003965649006886
385.5, 0.10495919996068892
386, 0.09436021937712269
386.5, 0.07253489809508551
387, 0.055008700929860765
387.5, 0.09918577268300055
388, 0.10026128659013978
388.5, 0.10024324361415893
389, 0.10024112656746809
389.5, 0.10021459338680927
390, 0.10078483126805793
390.5, 0.13701971629789966
391, 0.15064173215328935
391.5, 0.14901717090687328
392, 0.09554424801842742
392.5, 0.10004176558832967
393, 0.10024855871952809
393.5, 0.10024207718427647
394, 0.10024181346253158
394.5, 0.10024182504355394
395, 0.10024173665665614
395.5, 0.10024015712861001
396, 0.10030856760008078
396.5, 0.10137667958512964
397, 0.1539477282436792
397.5, 0.17701121977495404
398, 0.16724965002275383
398.5, 0.16706198155453933
399, 0.16773280788137868
399.5, 0.174368812974933
400, 0.05351087782372588
400.5, 0.05027750100801143
401, 0.0410219167208794
401.5, 0.20203143309562677
402, 0.09634144613555407
402.5, 0.10020939967165532
403, 0.10027756716731062
403.5, 0.10036514423039478
404, 0.07254723723495715
404.5, 0.10053524159883409
405, 0.1033715932764494
405.5, 0.20040668194947386
406, 0.04851073262528871
406.5, 0.05012316353115409
407, 0.05013005916416091
407.5, 0.05010137680635296
408, 0.04498416870842448
408.5, 0.09938653228967098
409, 0.15473986711397458
409.5, 0.15131663887170532
410, 0.14843415744812205
410.5, 0.10145305945860628
411, 0.09501331993340045
411.5, 0.14960385306834212
412, 0.1502692307083322
412.5, 0.15053893538474483
413, 0.16065708966982584
413.5, 0.05931670881551554
414, 0.04858210112392669
414.5, 0.1291410870138634
415, 0.052118707475997894
415.5, 0.05007563731174969
416, 0.050120252981272984
416.5, 0.05007938457671912
417, 0.04874697551923646
417.5, -0.004618436798750736
418, -0.00020670561603708393
418.5, 0.000017458761362831865
419, 0.0002796533392057654
419.5, -0.008497831918433008
420, 0.15764698366864138
420.5, 0.15007002836772187
421, 0.15039325925903313
421.5, 0.14884648752639862
422, 0.06976897621858313
422.5, 0.0006586963116745892
423, 0.000015679594881135017
423.5, -9.198698620593859e-7
424, -1.8931658019027964e-8
424.5, 1.2761489642798551e-9
425, -9.904965736495797e-12
425.5, 2.0915251752740005e-9
426, 2.0731022232212126e-8
426.5, -0.0000015833894053685071
427, -0.000012882296033467355
427.5, 0.001192872358572572
428, 0.04755362314300271
428.5, 0.045999656686262824
429, 0.10115910770089442
429.5, 0.15551311871909945
430, 0.15038462061257007
430.5, 0.15035753980866673
431, 0.1503651547446907
431.5, 0.1490221988389493
432, 0.10011395634650455
432.5, 0.09988433861082058
433, 0.10024678271952325
433.5, 0.10163708295168306
434, 0.15162018394457277
434.5, 0.15069874949914208
435, 0.15036029859898292
435.5, 0.15036228302655275
436, 0.15036275892315132
436.5, 0.15036468816981596
437, 0.15034420536433402
437.5, 0.14894330289182278
438, 0.0968633621219368
438.5, 0.06729228697143697
439, 0.04988011225728428
439.5, 0.050101696173214805
440, 0.05012127587619375
440.5, 0.0501209366037898
441, 0.05012091092891069
441.5, 0.05012091143905195
442, 0.050120911472546936
442.5, 0.05012091147180797
443, 0.05012091147177955
443.5, 0.05012091147177955
444, 0.05012091147177955
444.5, 0.05012091147177955
445, 0.05012091147177955
445.5, 0.05012091147177955
446, 0.05012091147177955
446.5, 0.05012091147177955
447, 0.05012091147177955
447.5, 0.05012091147177955
448, 0.05012091147177955
448.5, 0.05012091147177955
449, 0.05012091147177955
449.5, 0.05012091147177955
450, 0.05012091147177955
450.5, 0.05012091147177955
451, 0.05012091147177955
451.5, 0.05012091147177955
452, 0.05012091147177955
452.5, 0.05012091147177955
453, 0.05012091147177955
453.5, 0.05012091147177955
454, 0.05012091147177955
454.5, 0.05012091147177955
455, 0.05012091147175113
455.5, 0.05012091147175113
456, 0.050120911473527485
456.5, 0.050120911475360685
457, 0.05012091014984321
457.5, 0.0501209110522467
458, 0.05012189075353035
458.5, 0.05011953102489031
459, 0.04939797680452784
459.5, 0.05241796516590114
460, 0.12537001264465175
460.5, 0.050444677644705394
461, 0.05018891431649308
461.5, 0.050120326523639847
462, 0.050120820866666804
462.5, 0.050120912455312805
463, 0.0501209115920318
463.5, 0.050120911470187934
464, 0.05012091147159481
464.5, 0.05012091147177955
465, 0.05012091147177955
465.5, 0.05012091147177955
466, 0.05012091147177955
466.5, 0.05012091147177955
467, 0.05012091147177955
467.5, 0.05012091147177955
468, 0.05012091147177955
468.5, 0.05012091147177955
469, 0.05012091147173692
469.5, 0.050120911472205876
470, 0.05012091148486775
470.5, 0.05012091110781114
471, 0.05012090230592037
471.5, 0.05012119696684181
472, 0.0501272835192168
472.5, 0.04989850259258333
473, 0.04572810388135906
473.5, 0.0988395382345999
474, 0.10020464855625733
474.5, 0.10024378858612693
475, 0.10024186836970728
475.5, 0.10024182020114836
476, 0.10024182288887573
476.5, 0.10024182294733919
477, 0.10024182294360173
477.5, 0.10024182294353068
478, 0.10024182294353068
478.5, 0.10024182294353068
479, 0.10024182294353068
479.5, 0.10024182294353068
480, 0.10024182294353068
480.5, 0.10024182294353068
481, 0.10024182294353068
481.5, 0.10024182294353068
482, 0.10024182294353068
482.5, 0.10024182294353068
483, 0.10024182294353068
483.5, 0.10024182294353068
484, 0.10024182294353068
484.5, 0.10024182294353068
485, 0.10024182294353068
485.5, 0.10024182294353068
486, 0.10024182294353068
486.5, 0.10024182294353068
487, 0.10024182294353068
487.5, 0.1002418229435591
488, 0.10024182294348805
488.5, 0.10024182293975059
489, 0.10024182298118944
489.5, 0.10024182570543871
490, 0.10024179005617384
490.5, 0.10023982513473584
491, 0.10026979627433263
491.5, 0.10168103551876584
492, 0.15417391049564344
492.5, 0.15061803802966267
493, 0.15035707324720704
493.5, 0.1503624025274206
494, 0.1503627427228622
494.5, 0.15036273484436435
495, 0.1503627344032452
495.5, 0.1503627344147418
496, 0.15036273441594972
496.5, 0.15036273443158166
497, 0.1503627339304927
497.5, 0.15036272306483056
498, 0.15036311310441874
498.5, 0.15037058645468449
499, 0.15006884671194598
499.5, 0.14498068133960373
500, 0.14366355026420763
500.5, 0.15019714199659973
501, 0.15046609494724805
501.5, 0.15168148019186845
502, 0.1854100497627229
502.5, 0.20230222190204472
503, 0.20034439206543198
503.5, 0.20048153095736154
504, 0.20048383806491188
504.5, 0.20048364827280807
505, 0.20048364562289578
505.5, 0.2004836458845034
506, 0.20048364588744505
506.5, 0.200483645887104
507, 0.20048364588714662
507.5, 0.20048364588730294
508, 0.20048364583935552
508.5, 0.200483645807779
509, 0.2004836813522104
509.5, 0.20048364438355293
510, 0.20045739250809902
510.5, 0.20053028241497373
511, 0.2272887597268749
511.5, 0.2506878068533638
512, 0.25062896364075016
512.5, 0.2506036415948216
513, 0.250501961589606
513.5, 0.251344348956124
514, 0.19609361507298217
514.5, 0.2005346974446951
515, 0.2005931906461882
515.5, 0.19933176873817615
516, 0.2547388698769737
516.5, 0.2491713553622361
517, 0.3045277921427214
517.5, 0.30111030221952717
518, 0.33680894868707867
518.5, 0.4052427152545306
519, 0.40123124593446846
519.5, 0.4009609893118693
520, 0.4009669497552295
520.5, 0.4009673011967436
521, 0.4009672994915974
521.5, 0.40096710691953774
522, 0.4009621696901462
522.5, 0.4011131617188255
523, 0.42665037554658625
523.5, 0.5948282979125707
524, 0.6534617955196609
524.5, 0.6641903651310201
525, 0.6964686989743853
525.5, 0.7645121881850656
526, 0.8024869879319283
526.5, 0.8574752518325823
527, 0.8531539727884478
527.5, 0.9095422268200082
528, 0.9912091562573409
528.5, 1.0205411786619436
529, 1.0530427710619108
529.5, 1.1091863836419122
530, 1.1488649949553036
530.5, 1.1683430032023665
531, 1.253607644582857
531.5, 1.2541490566969173
532, 1.3008332137819707
532.5, 1.3060252258243281
533, 1.400280764882993
533.5, 1.3994324107686253
534, 1.4539746121836004
534.5, 1.50370433632321
535, 1.5538024565219644
535.5, 1.5737751875880264
536, 1.6539463819873106
536.5, 1.6816553794459708
537, 1.7552461602138294
537.5, 1.7545986325635425
538, 1.7542297488352858
538.5, 1.7542362791746342
539, 1.7542003908164645
539.5, 1.7506732250738537
540, 1.6549660440317098
540.5, 1.8308502927223174
541, 1.9080219418236481
541.5, 1.9495745426014963
542, 2.0576469526002086
542.5, 2.0868411304150953
543, 2.05172708009151
543.5, 2.058627889450463
544, 1.9520056213398504
544.5, 1.9597391611973194
545, 1.9076152903838448
545.5, 1.8497265485554806
546, 1.8023517001806084
546.5, 1.7559525352526464
547, 1.7078618266662602
547.5, 1.651898606088963
548, 1.6331014585785226
548.5, 1.555169939102953
549, 1.5536968554965824
549.5, 1.5537467955723372
550, 1.553736790832673
550.5, 1.5535151095933628
551, 1.5640685452233782
551.5, 1.6554360988545511
552, 1.653867658054395
552.5, 1.6532403948831274
553, 1.5817926604415646
553.5, 1.5100134946790433
554, 1.4892265295641494
554.5, 1.3573515649637926
555, 1.34994654981044
555.5, 1.450227554800989
556, 1.4726119092355248
556.5, 1.5013754250220472
557, 1.630487385605221
557.5, 1.7494809796447015
558, 1.8071922260312192
558.5, 1.9037527100562386
559, 1.9508338774796812
559.5, 2.055866106907402
560, 2.1101939883198924
560.5, 2.1052909125882167
561, 1.9508637688713435
561.5, 1.9046688438611028
562, 1.828745381258372
562.5, 1.7546001931006003
563, 1.6997395539079463
563.5, 1.7026645453435094
564, 1.6552500380200996
564.5, 1.6539776583148438
565, 1.6535777037964152
565.5, 1.657142658877774
566, 1.7331150151246817
566.5, 1.757180957385998
567, 1.857138537361692
567.5, 1.8593133406910027
568, 1.936424726044649
568.5, 1.9520766173370845
569, 2.0585756673557682
569.5, 2.1587114848384203
570, 2.226674624667808
570.5, 2.308402884247016
571, 2.362147125228404
571.5, 2.464861837072789
572, 2.488230084497985
572.5, 2.5552634443390474
573, 2.556124290174793
573.5, 2.556167787625327
574, 2.5561665389818558
574.5, 2.556166483302789
575, 2.5561664875499304
575.5, 2.556166401504612
576, 2.556164712840669
576.5, 2.5562314060301077
577, 2.557383439911362
577.5, 2.60879073747482
578, 2.69681553689081
578.5, 2.7833156106883905
579, 2.9491938642969586
579.5, 3.045931606168267
580, 3.2575561552779533
580.5, 3.4177479993009
581, 3.701055180524449
581.5, 3.8120474896168304
582, 4.157649940851812
582.5, 4.284483231526039
583, 4.50840475368426
583.5, 4.582384489030389
584, 4.657967020088236
584.5, 4.803973480819266
585, 4.910589036601422
585.5, 4.958100129821133
586, 5.062933908008816
586.5, 5.199453210170958
587, 5.31262284911422
587.5, 5.438403560020262
588, 5.766020015833135
588.5, 6.133429691654328
589, 6.472259124536919
589.5, 6.890482454281923
590, 7.329957034769237
590.5, 7.85796428788386
591, 8.491621189623928
591.5, 9.047331093667893
592, 9.643411601348063
592.5, 10.090659211531474
593, 10.654572685256753
593.5, 11.162103683298895
594, 11.653014027046638
594.5, 12.232394707926957
595, 12.711052671635727
595.5, 13.253475015097678
596, 13.725446469786263
596.5, 14.271199403777189
597, 15.099475630782166
597.5, 15.676171478332762
598, 16.709989611641262
598.5, 18.113503061653375
599, 19.114762053517694
599.5, 20.472345494575222
600, 21.721976412183523
600.5, 23.41223921959046
601, 24.85335493537127
601.5, 26.43243099567617
602, 28.326232928402902
602.5, 29.73824923815789
603, 31.743005403787677
603.5, 33.56745818863848
604, 35.53368850399154
604.5, 37.85637508708945
605, 39.67572032494169
605.5, 41.98428624679893
606, 44.06159796767558
606.5, 46.69683042702921
607, 49.30517598231859
607.5, 51.422287942370176
608, 54.21016317358526
608.5, 56.61874031238017
609, 60.13829248782827
609.5, 63.622579093422075
610, 66.3659020386773
610.5, 69.71732762162992
611, 73.30364766925155
611.5, 76.84433885293507
612, 80.2298865735645
612.5, 83.48921680670195
613, 86.5358664795458
613.5, 89.02662044673652
614, 92.07937025000382
614.5, 94.65703578760845
615, 95.92108566037197
615.5, 97.55063657318532
616, 98.31134250106349
616.5, 98.80037742096657
617, 98.88881611287542
617.5, 97.96911983268343
618, 96.32560141632271
618.5, 94.20364161184844
619, 90.47325654356241
619.5, 86.81285599825523
620, 82.9837383313542
620.5, 77.22691693050783
621, 73.40921783498678
621.5, 67.51323953708689
622, 62.22942989128245
622.5, 57.59407320540693
623, 52.774744029658905
623.5, 49.17133121312915
624, 45.20792671890864
624.5, 41.52313249143849
625, 37.93125382936516
625.5, 34.11688564102906
626, 32.06705068125105
626.5, 28.967617576436908
627, 26.21495743460349
627.5, 23.59798698347808
628, 21.278826216823944
628.5, 19.671854581673898
629, 17.72622458555678
629.5, 16.264698074010965
630, 14.906640822831065
630.5, 13.531845364913607
631, 12.636150912615278
631.5, 11.69839785535116
632, 11.01944368864352
632.5, 10.30037025095909
633, 9.605876910091538
633.5, 9.199407294677798
634, 8.485145331658387
634.5, 8.039457790897174
635, 7.6327823132894395
635.5, 7.254420118510069
636, 6.924688113490504
636.5, 6.643355987844529
637, 6.419407604618144
637.5, 6.106416087241868
638, 5.8672645645407755
638.5, 5.588433150995655
639, 5.312690830967085
639.5, 5.036491939700255
640, 4.810154269550267
640.5, 4.558436739773299
641, 4.306037557997655
641.5, 4.1027025343310015
642, 3.852859302617958
642.5, 3.729592712443875
643, 3.6070092640481874
643.5, 3.608487623328628
644, 3.608438453387123
644.5, 3.5760864581491774
645, 3.5029848821380796
645.5, 3.3268534502775395
646, 3.094136387049417
646.5, 2.8438137705566504
647, 2.6434425639806847
647.5, 2.4818618452377166
648, 2.407824907286539
648.5, 2.5035128354973892
649, 2.67105772973666
649.5, 2.9313304998723737
650, 3.066674256158123
650.5, 3.284835549663029
651, 3.420758551641015
651.5, 3.583546089020402
652, 3.658070389742079
652.5, 3.656982173339543
653, 3.523059897513008
653.5, 3.3771873672263695
654, 3.0838265749784455
654.5, 2.8728857918036823
655, 2.485636301871992
655.5, 2.192977005994038
656, 1.7304422914725706
656.5, 1.4238213347494195
657, 1.1563435400718447
657.5, 0.8602241254531862
658, 0.7001561782068961
658.5, 0.7476974206002183
659, 0.8283067122187759
659.5, 0.9438148233334687
660, 1.1769553819545848
660.5, 1.0510964533140736
661, 1.0527218617121292
661.5, 1.0525306893467103
662, 1.0538564612065642
662.5, 1.1013854033010801
663, 1.1787947906018132
663.5, 1.3510482068604688
664, 1.5022082828628953
664.5, 1.6536412639282076
665, 1.7784273672706234
665.5, 1.8543588401822149
666, 1.8264398636934658
666.5, 1.75377080047069
667, 1.6427242604005983
667.5, 1.6023143668509618
668, 1.5747854346797823
668.5, 1.5542759204098502
669, 1.4992557375201017
669.5, 1.5028077856725304
670, 1.5581108733594675
670.5, 1.5529075700380588
671, 1.6400848025315184
671.5, 1.6532090503362724
672, 1.7407467196683513
672.5, 1.7610137010422875
673, 1.8722631113585493
673.5, 1.8984963309317067
674, 1.855451379281945
674.5, 1.85444339634833
675, 1.8541728152727757
675.5, 1.8613861311063147
676, 1.9930106840637904
676.5, 1.9516366992083647
677, 2.031456355437669
677.5, 2.0575257310214425
678, 1.9614533514018575
678.5, 1.8979951997214641
679, 1.827139289300149
679.5, 1.6861961916709873
680, 1.611752715484073
680.5, 1.5484810380257699
681, 1.5789199722138108
681.5, 1.74298509919808
682, 1.8332619531002479
682.5, 1.9036968711046143
683, 1.8984251056494656
683.5, 2.0534950231232187
684, 2.1055856584536627
684.5, 2.047540603586981
685, 1.9657080412629
685.5, 1.9131295580475154
686, 1.759581541619255
686.5, 1.5270148762232765
687, 1.3144244787541624
687.5, 1.1867870031482681
688, 1.0544315775155297
688.5, 0.8152791823830796
689, 0.80303401217067
689.5, 0.7295480865878403
690, 0.7017260367535982
690.5, 0.7031517007560382
691, 0.751906771207473
691.5, 0.9113972512710404
692, 1.1048759729109605
692.5, 1.177298721774875
693, 1.4247118672699344
693.5, 1.4382777419742183
694, 1.757790313787794
694.5, 1.8881250822054199
695, 1.962966034444193
695.5, 2.0471873808066334
696, 2.1081388716118
696.5, 2.15400344864878
697, 2.1552177886199217
697.5, 2.155302674014905
698, 2.153807234601217
698.5, 2.210543848553627
699, 2.259257696299102
699.5, 2.2614500938621376
700, 2.1171600614778043
700.5, 1.7922613823503895
701, 1.3477699327072656
701.5, 1.1209159659735093
702, 0.5823767648627154
702.5, 0.33979018670022754
703, 0.17579379326942046
703.5, 0.10152031957726138
704, 0.10019751282729317
704.5, 0.10024068657052965
705, 0.10022599332846482
705.5, 0.09990576661819262
706, 0.11386971876619612
706.5, 0.17081865381589978
707, 0.17677886465462223
707.5, 0.17616321754930198
708, 0.0528704162464777
708.5, 0.04151696189641996
709, 0.16306878076636622
709.5, 0.1756424536815473
710, 0.17235226788578473
710.5, 0.15564470341689685
711, 0.13126766934514933
711.5, 0.10049518607755203
712, 0.10021470207182404
712.5, 0.10024154712118616
713, 0.10024185145920228
713.5, 0.10024177732742601
714, 0.10024830235381899
714.5, 0.10026526303531114
715, 0.09540866778777968
715.5, 0.15055630538910236
716, 0.15026453444765764
716.5, 0.15036270343931335
717, 0.15036286693650425
717.5, 0.1503627344307148
718, 0.1503628717445622
718.5, 0.15036228622125236
719, 0.1502615917964789
719.5, 0.15087477203071842
720, 0.09566200482375109
720.5, 0.10028172455282913
721, 0.10024792382704106
721.5, 0.10024175603147967
722, 0.10024181484773464
722.5, 0.10024182305092211
723, 0.10024182295424566
723.5, 0.10024182294337436
724, 0.10024182294350226
724.5, 0.10024182294353068
725, 0.10024182294353068
725.5, 0.10024182294353068
726, 0.10024182294353068
726.5, 0.10024182294353068
727, 0.10024182294353068
727.5, 0.10024182294353068
728, 0.10024182294353068
728.5, 0.10024182294353068
729, 0.10024182294353068
729.5, 0.10024182294353068
730, 0.10024182294353068
730.5, 0.10024182294353068
731, 0.10024182294353068
731.5, 0.10024182294353068
732, 0.10024182294353068
732.5, 0.10024182294353068
733, 0.10024182294353068
733.5, 0.10024182294353068
734, 0.10024182294353068
734.5, 0.10024182294353068
735, 0.10024182294353068
735.5, 0.10024182294353068
736, 0.10024182294344541
736.5, 0.10024182295086348
737, 0.1002418230128228
737.5, 0.10024181739710514
738, 0.10024178031447661
738.5, 0.10024599721565153
739, 0.10026675436625965
739.5, 0.09711220416708954
740, 0.20036962087664278
'''

def read_txt_files(DIRECTORY):  
    '''Reads numerical data from text files in a specified directory,
       creates dictionaries where keys are values from the 1st column (wavelength)
       and values are values from the 2nd column. 
       Returns 3 dictionaries for data about dichroic, em & exc filters.
    '''
    dict_dichr = {}
    dict_em = {}
    dict_exc = {}

    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".txt"):
            with open(os.path.join(DIRECTORY, filename), 'r') as file:
                data = file.readlines()
                data_dict = {float(line.split()[0]): float(line.split()[1]) for line in data}
                
                if filename == dichr:
                    dict_dichr = data_dict
                elif filename == em:
                    dict_em = data_dict
                elif filename == exc:
                    dict_exc = data_dict

    return dict_dichr, dict_em, dict_exc

def create_dictionary_from_string(input_str):
    dict_from_string = {}
    lines = input_str.strip().split('\n')
    for line in lines:
        key, value = line.split(', ')
        dict_from_string[float(key)] = float(value)
    
    return  dict_from_string

def normalize_spectra(dictionary):
    
    # Filter the dictionary in case it has NaN values
    # The normalization calculation is performed only on non-NaN values
    valid_values = [v for v in dictionary.values() if not math.isnan(v)]
    
    if not valid_values:
        return {}  # Return an empty dictionary if all values are NaN
    
    x_min = min(valid_values)
    x_max = max(valid_values)
    
    normalized_dict = {k: (v - x_min) / (x_max - x_min) if not math.isnan(v) else math.nan for k, v in dictionary.items()}
    
    return normalized_dict

def plot_overlap(*dicts):
    '''
    Plots graphs for all input dictionaries and a graph for the overlapping part.
    Creates a new dictionary with just the overlapping x and y values.
    Returns a dictionary containing the overlapping x and y values.
    '''
    # Plot all graphs
    for d in dicts:
        plt.plot(list(d.keys()), list(d.values()), marker='o')
    plt.title('All Graphs')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.show()
    
    # Find overlap
# =============================================================================
#     bluedict and orangedict have the same keys.
#     if both items in bluedict and orangedict have equal keys:
# 
#         if value in bluedict > value in orangedict, the value in newdict
#         is equal to the values in orangedict.
#         if value in bluedict < value in orangedict, the value in newdict
#         is equal to the values in bluedict.
#         if value in bluedict = value in orangedict, the value in newdict
#         is equal to this same value.
#     
#     new dict should have the same keys as the bluedict and orangedict.
#     
# =============================================================================
    
    overlap_keys = set(dicts[0].keys())
    for d in dicts[1:]:
        overlap_keys &= set(d.keys())
    
    # Extract overlapping parts
    overlap_dict = {x: dicts[0][x] for x in overlap_keys}
    
    # Plot overlap
    plt.plot(list(overlap_dict.keys()), list(overlap_dict.values()), marker='o', color='red')
    plt.title('Overlap Graph')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.show()
    
    return overlap_dict

def cutoff_dicts(*dicts, minwavelength, maxwavelength):
    '''Takes in several dictionaries and two values.
        returns dictionaries with the same values, but with keys only in the
        range of minwavelength and maxwavelength. For example:
        dict1 = {1: 10, 2: 20, 3: 30, 4: 120}
        dict2 = {1: 5, 2: 15, 3: 25, 4: 108}
        minwavelength = 2
        maxwavelength = 3
        Returns:
        newdict1 = {2: 20, 3: 30}
        newdict1 = {2: 20, 3: 30}
    '''
    new_dicts = ()
   
    for d in dicts:
       new_dict = {k: v for k, v in d.items() if minwavelength <= k <= maxwavelength}
       new_dicts += (new_dict,)
   
    return new_dicts

def read_excel_to_dicts(filepath):
    data = pd.read_excel(filepath)
    dict1, dict2, dict3 = {}, {}, {}  
    for index, row in data.iterrows():
       dict1[row['Wavelength (nm)']] = row[data.columns[1]]
       dict2[row['Wavelength (nm)']] = row[data.columns[2]]
       dict3[row['Wavelength (nm)']] = row[data.columns[3]]
   
    return dict1, dict2, dict3

def main():
    
    print("Specify filenames for dichroic&filters (dichr, em, exc). \n")
    print("Specify amber_led_intensity. \n")
    print("Specify cutoff wavelengths. \n")
    minwavelength = 500
    maxwavelength = 700
    
    filename = "JF608 set.xlsx"
    filepath = f"{DIRECTORY_EXC}/{filename}"
    dict_exc, dict_dichr, dict_em = read_excel_to_dicts(filepath)
# =============================================================================
#     print("exc:", list(islice(exc.items(), 5)), '\n')
#     print(type(exc), '\n')
#     print("dichr:", list(islice(dichr.items(), 5)))
#     print("em:", list(islice(em.items(), 5)))
#     
# =============================================================================
#    dict_dichr, dict_em, dict_exc = read_txt_files(DIRECTORY)

    # Initialize dictionary with LED intensity data
    dict_led_intensity = create_dictionary_from_string(amber_led_intensity)
    
    # Normalize all data
    dict_dichr = normalize_spectra(dict_dichr)
    dict_exc = normalize_spectra(dict_exc)
    dict_em = normalize_spectra(dict_em)
    dict_led_intensity = normalize_spectra(dict_led_intensity)
    
    # Cutoff irrelevant wavelengths
    cut_dict_dichr, cut_dict_led_intensity, cut_dict_em, cut_dict_exc = cutoff_dicts(dict_dichr, dict_led_intensity, dict_em, dict_exc, minwavelength=minwavelength, maxwavelength=maxwavelength)
    # print(cut_dict_dichr)
    # Plot
    overlap_dict = plot_overlap(cut_dict_dichr, cut_dict_em, cut_dict_exc)
    #print("New dictionary with overlapping parts:", overlap_dict)

if __name__ == "__main__":
    main()
