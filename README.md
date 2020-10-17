# Multi-Agent-Search-AI
Câu 1 Hàm dánh giá
 - minfood là quãng đường mahattan từ pacman đến thức ăn gần nhất
 - minghost là quãng đường mahattan từ pacman đến con magần nhất
 - vì muốn tránh con ma gần nhất nên điểm đánh giá sẽ trừ đi 1/(minghost + 0.1) phải lấy 1 chia vì minghost càng nhỏ thì 1/(minghost + 0.1) càng lớn còn phải cộng thêm 0.1 tránh trường hợp không 
   có con ma gây lỗi chương trình 
 - vì muốn ăn thức ăn gần nhất nên điểm đánh giá sẽ cộng thêm 1/(minfood + 0.1) phải lấy 1 vì minfood càng nhỏ thì 1/(minfood + 0.1) càng lớn còn phải cộng thêm 0.1 tránh trường hợp không có 
   thức ăn gây lỗi chương trình và tạo ra số lớn để cho con ma đi đến trạng thái là ăn hết thức ăn.
 - điểm đánh giá sẽ cộng thêm min của số bước đi của con ma khi nó sợ, lấy min vì khi pacman ăn phải con ma thì nó sẽ trở về trạng thái đi ăn pacman nên phải tránh con ma đó nhưng có thể
   con ma còn lại vẫn còn sợ nên phải lấy min để có một giải pháp an toàn cho pacman.
Câu 2 minimax
 - hàm get_max sẽ lấy giá trị max điểm đánh giá của các nút dưới. Các nút dưới ở đây là các action của pacman có thể đi .Các điểm đánh giá của nút con này là min của các action của tất cả con 
   ma di chuyển đồng thời mà nó có thể di.Hàm sẽ trả về điểm đánh giá cao nhất và action ứng với nó. Nếu chiều cao cây duyệt nhỏ hơn không sẽ lấy thì nó sẽ là lá của cây mà ta cần duyệt 
hoặc trạng thái của game là thắng hoặc thua  thì sẽ trả về là điểm đánh giá của trạng thái đó
   
 - hàm get_min sẽ lấy giá trị min  điểm đánh giá của các nút dưới. Các nút dưới ở đây là các action của tất cả con ma có thể đi và các con ma di chuyển đồng thời .Các điểm đánh giá 
của nút con này là max của các action của pacman có thể di tiếp theo. Hàm sẽ trả về điểm đánh giá thấp nhất và action ứng với nó.Nếu chiều cao cây duyệt nhỏ hơn không sẽ lấy 
thì nó sẽ là lá của cây mà ta cần duyệt hoặc trạng thái của game là thắng hoặc thua  thì sẽ trả về là điểm đánh giá của trạng thái đó

Câu 3 alpha beta
 - Giống với hàm minimax nhưng với hàm hàm get_max và get_min ta thêm đầu vào 2 giá trị alpha và beta. Với mỗi lần duyệt các action sau khi lấy được điểm đánh giá của action thì thêm 
   thuật toán cắt nhánh nếu không cắt được cây thì cập nhật alpha hoặc beta tương ứng. Alpha sẽ dùng cho hàm get_max và beta dùng cho hàm get_min.
 - Thuật toán cắt nhánh với get_max nếu v > beta có nghĩa là điểm đánh giá lại lớn hơn số nhỏ nhất tốt nhất thì chắc chắn pacman sẽ không đi vào nhánh này nên ta sẽ cắt nhánh 
   bằng return luôn v và action.
 - Thuật toán cắt nhánh với get_min nếu v < alpha có nghĩa là điểm đánh giá lại nhỏ hơn số lớn nhất tốt nhất thì chắc chắn pacman sẽ không đi vào nhánh này nên ta sẽ cắt nhánh 
   bằng return luôn v và action.
 - Khởi tạo ban đầu vì chưa có số tốt nhất lớn nhất và nhỏ nhất nên sẽ khởi tạo alpha là inf và beta là -inf
Câu 4  Expectimax
 - Hàm này dùng với các con ma không tối ưu nên sẽ lấy action có điểm đánh giá trung bình cao nhất vì với điểm trung bình cao nhất nên tỉ lệ thắng sẽ cao hơn
 - Hàm get_max sẽ lấy điểm cao nhất của các action của pacman có thể đi. Các điểm của các action của pacman là điểm trung bình của điểm tất cả các con ma có thể đi với action đó
 - Hàm get_score sẽ lấy điểm trung bình của tất cả các bước đi chuyển của con ma khi tất cả các con ma di chuyển đồng thời new_score của các action này lại là max của các action của con ma 
có thể đi
 - Hàm getAction vì các hàm get_max và get_score chỉ trả về điểm đánh giá nên ta phải lấy các action của trạng thái đầu tiên và lấy các điểm trung bình (hàm get_score) của điểm tất cả các 
   con ma có thể đi với action đó điểm nào cao nhất thì sẽ trả về action tương ứng

Câu 5 Hàm dánh giá
 - minfood là quãng đường mahattan ngắn nhất của pacman đi ăn hết tất cả các thức ăn trên bản đồ
 -  minDistGhost là quãng đường mahattan từ pacman đến con magần nhất
 - vì muốn tránh con ma gần nhất nên điểm đánh giá sẽ trừ đi 1/ (minDistGhost+ 0.1) phải lấy 1 chia vì minghost càng nhỏ thì 1/( minDistGhost + 0.1) càng lớn còn phải cộng thêm 0.1 tránh 
   trường hợp không có con ma gây lỗi chương trình 
 - vì muốn ăn hết các thức ăn nhanh nhất nên điểm đánh giá sẽ cộng thêm 1/(minfood + 0.1) phải lấy 1 vì minfood càng nhỏ thì 1/(minfood + 0.1) càng lớn còn phải cộng thêm 0.1 tránh trường 
   hợp không có thức ăn gây lỗi chương trình và tạo ra số lớn để cho con ma đi đến trạng thái là ăn hết thức ăn.
 - điểm đánh giá sẽ cộng thêm min của số bước đi của con ma khi nó sợ, lấy min vì khi pacman ăn phải con ma thì nó sẽ trở về trạng thái đi ăn pacman nên phải tránh con ma đó nhưng có thể
   con ma còn lại vẫn còn sợ nên phải lấy min để có một giải pháp an toàn cho pacman.