
##############
###  Note  ###
##############

整個程式必須以 Python 3.5 Build 或 Python 3.6 Build 來執行
( 可在Sublime Text 3 選擇 Tool -> Build System -> Python3.5 / Python 3.6
  Sublime Text 按下 Ctrl+B 即為執行程式 )
  

######################
###    收集DATA    ###
######################

0. 準備工作：架好收集Data所需設備(眼鏡，噴氣口，3個USB相機)
	執行 Jetting-Glasses/Deep Learning/testCamera.py 
	確認畫面如下圖
	
	╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴╴
	|			|			|			|
	|    Left   |	 Mid	|	Right	|
	|			|			|			|
	￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
	
	P.S. 若畫面不如上圖，有兩種解決方法
		1. 試著將 USB 插在電腦的不同接口，再執行程式一次試試看直到如上圖
		2. 若上述方法無法解決，可打開 Jetting-Glasses/Deep Learning/testCamera.py，
			並 Assign Line 7 ~ Line 9 的三個變數 CAMERA_LEFT, CAMERA_MID, CAMERA_RIGHT 新的值
			值可分別設為 0 ~ 4 (3個不同數字, Trial & Error)
			


1. 執行 Jetting-Glasses/Deep Learning/CollectData_Practice.py
	讓使用者熟悉流程及熟悉將手擺放至噴氣口位置
	
	流程：
	 Step 1. 輸入使用者姓名，按下開始 Mode 1
	 Step 2. 畫面會顯示手、藍點，藍點表示應該將手的哪個指節對到噴氣口
			 左上角會出現'Preparing'或'Recording'
			 'Preparing' 代表此時不會儲存，可稍微放鬆，但請使用者準備將對應的指節移到噴氣口做準備
			 'Recording' 代表已經開始儲存，必須要專注
	 Step 3. 

	 
2. 執行 Jetting-Glasses/Deep Learning/CollectData.py
	正式開始收Data

	不同 Mode 的差異
	 Mode 1 : 請使用者將指節中心對準噴口，若感覺穩定可進行小幅度的前後左右移動 (適中距離)
	 Mode 2 : 請使用者將指節中心對準噴口且盡量靠近，然後左右移動並同時慢慢拉遠 (近距離 -> 遠距離)
	 Mode 3 : 請使用者用氣流「描繪指節的邊界」，也就是讓噴氣孔對應到指節的邊界並在邊界上移動 (適中距離)
	
	
	
	
##################################
###    前處理 Preprocessing    ###
##################################

