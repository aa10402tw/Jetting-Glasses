
#################
###   Note    ###
#################
要先校準 High Speed Camera 得到相機參數，才有辦法算 ArUco 的 Pose，才能得到座標。
因此要得到 OptiTrack 與 High Speed Camera 關係之前，需先校準 High Speed Camera。

流程 ： Calibrate high speed camera --> Calib_optiTrack_Camera --> 得到兩組點座標 --> 交給邱玄學姊分析


########################################
###   Calibrate high speed camera    ###
########################################
1.  印出 Jetting-Glasses\Aruco\Camera Calibration\Image_to_print\chessboard5x6.docx 貼在平面上
2.	執行 Jetting-Glasses\Aruco\Camera Calibration\calib_chessboard.py 
	切換輸入法為英文，按下 a 為拍攝，拍攝不同視角(viewpoint)的 chessboard照片(大約50張左右)
	按下 c 開始計算相機參數，最後按下 q 離開
	
	
#################################################################
###   Transformaion between OptiTrack and High Speed Camera   ###
#################################################################
1.  印出 Jetting-Glasses\Aruco\Camera Calibration\Image_to_print\Marker.docx 貼在 Rigibody 中心
2.	執行 Jetting-Glasses\Aruco\Camera Calibration\Align_optiTrack_Camera
	拍攝過程只有在 Marker 被偵測到的時候會分別記錄此時在 optiTrack 及 Camera 的座標
	且為自動記錄，當完成後切換輸入法為英文按下 q 離開
3. 	將 Jetting-Glasses\Aruco\Camera Calibration\CalibResult\TwoCoordinatePoints.csv 檔案傳給邱玄學姊分析，
	並告知她 "point_OptiTrack" 欄位為 optiTrack 記錄下來的點，"point_Camera" 欄位為 High Speed Camera 記錄下來的點
	而我們希望得到的是 「從 OptiTrack 坐標系到 High Speed Camera坐標系 的 Transformation」