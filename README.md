## Expiry Management Module (Odoo)
## Tổng quan
Expiry Management là module hỗ trợ quản lý các sản phẩm sắp hết hạn trong hệ thống Odoo.
Module giúp doanh nghiệp theo dõi hạn sử dụng sản phẩm, cảnh báo các sản phẩm gần hết hạn và tự động gửi email thông báo để tránh thất thoát hàng hóa.
## Chức năng chính
### 1. Quản lý sản phẩm sắp hết hạn

* Hiển thị danh sách các sản phẩm sắp hết hạn trong **30 ngày tới**.
* Hỗ trợ theo dõi các lô sản phẩm (lot/serial) và ngày hết hạn.
* Các sản phẩm còn **dưới 7 ngày** trước khi hết hạn sẽ được **tô màu đỏ** để cảnh báo trực quan cho người quản lý.

### 2. Tự động gửi mail thông báo

* Hệ thống sử dụng **Cron Job của Odoo** để tự động chạy mỗi ngày.
* Tự động gửi email thông báo các sản phẩm sắp hết hạn cho bộ phận sales.

### 3. Dashboard quản trị

* Dashboard tổng quan hiển thị  Pivot và Graph:
  
  * Số lượng sản phẩm sắp hết hạn
  * Số sản phẩm đã quá hạn
  * Tổng giá trị tổn thất
    
### 4. Phân quyền người dùng

* Phân thành 2 nhóm người dùng User và Manager. Đối với nhóm Manager sẽ có thể xem được Báo cáo Dashboard

## Installation

1. Copy module vào thư mục `addons` của Odoo.
2. Restart Odoo server.
3. Update Apps List.
4. Cài đặt module **Expiry Management**.

## Technologies

* Odoo Framework
* Python
* XML (Views & Reports)

## Author
Tran Hao
