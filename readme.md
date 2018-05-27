Hướng dẫn cài đặt .

Hệ thống được cài đặt trên ngôn ngữ lập trình PYTHON 2.7 .

Các bước cài đặt :

B1 : Cài đặt python 2.7 tại https://www.python.org/downloads/

B2 : Sau khi đã cài python ta cài các gói hỗ trợ sau :
- numpy
- scipy
- scikit-learn
- underthesea
- flask

Để cài đặt gói , ta dùng lệnh sau :
pip install [package_name]

B3 : Sau khi cài xong các gói , để chạy hệ thống ta chạy file server.py
Sau đó vào url  127.0.0.1:8008 để vào hệ thống

Các kết quả thử nghiệm đã được lưu sẵn trong các file trong thư mục /thongke
w2v_test_created.txt : Kết quả thử nghiệm dùng Word2vec trên bộ test_created.txt
tfidf_test_created.txt : Kết quả thử nghiệm dùng VSM trên bộ test_created.txt
tfidf_test.txt : Kết quả thử nghiệm dùng VSM trên bộ test.txt

Để chạy lại kết quả thử nghiệm , chạy file thongke.py .
