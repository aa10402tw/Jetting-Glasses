
##############
###  Note  ###
##############

整個實驗程式，分析程式必須以 Python 3.5 Build 來執行
( 可在Sublime Text 3 選擇 Tool -> Build System -> Python3.5 
  Sublime Text 按下 Ctrl+B 即為執行程式 )
  

############################
###   實驗 Experiment    ###
############################

0. 準備工作：架好實驗所需設備
   依照 Jetting-Glasses/Experiment/HandMarker.jpg 的圖片貼上對應的 Marker
   ( 可執行 Jetting-Glasses/Experiment/lookID.py 來看各個 Marker 的 ID ， 按下Ctrl+Space切換成英文輸入，再按下'q'可離開)

1. 執行 Jetting-Glasses/Experiment/experiment.py

2. 實驗程式流程：
	Step 1 : 執行實驗程式 -> 輸入受試者姓名 -> 輸入受試者各個指節厚度 -> 按下 "Test" 讓受試者練習 
			( Test 結束後會出現 Debug Info，若有問題請調整後再執行一次 Test 確保無問題 )
	Step 2 : 再次執行實驗程式 -> 輸入受試者姓名(請相同) -> 選擇 "haptic" 或 "no haptic" -> 實驗 -> 若無問題，最後請按 save data
	Step 3 : Step 2 換 Mode 再跑一次
	
	
	
############################
###    分析 Analysis     ###
############################
	
1. 將 Jetting-Glasses/Experiment/Data 整個資料夾複製到 Jetting-Glasses/Aruco/Analyze/ 底下 (選擇覆蓋全部)

2. 執行 Jetting-Glasses/Aruco/Analyze/analysis.py

3. 打開 Jetting-Glasses/Aruco/Analyze/AnalyzeResult/summary.excel 察看結果

P.S. 若想看某個受試Detail，可打開 Jetting-Glasses/Aruco/Analyze/analysis_single.py 並修改 "participant_name" 且執行