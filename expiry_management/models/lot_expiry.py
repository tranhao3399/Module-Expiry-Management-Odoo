# expiry_management/models/lot_expiry.py
from odoo import models, fields, api
from datetime import date, timedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'

    # --- 1. CÁC TRƯỜNG DỮ LIỆU ---

    # Trường Tính toán: Số ngày còn lại (Giữ nguyên)
    days_to_expire = fields.Integer(
        string='Days Remaining',
        compute='_compute_days_to_expire',
        store=True,
    )

    # Lấy giá vốn từ Sản phẩm
    unit_cost_price = fields.Float(
        string="Giá Vốn Đơn Vị",
        related='product_id.standard_price',
        readonly=True
    )

    # Trường Tính toán: Số lượng tồn kho lưu trữ (cho báo cáo)
    stored_product_qty = fields.Float(
        string="Số lượng Tồn kho",
        compute='_compute_stored_product_qty',
        store=True,
        group_operator='sum',
        digits='Product Unit of Measure'
    )

    # Trường Tính toán: Tổng Giá trị Tổn thất
    total_loss_value = fields.Float(
        string="Tổng Giá Trị Tổn Thất",
        compute='_compute_total_loss_value',
        store=True,
        group_operator='sum'
    )

    # Trường Logic: Đã hết hạn và chưa xử lý
    is_expired_unsold = fields.Boolean(
        string='Đã hết hạn và chưa xử lý',
        compute='_compute_is_expired_unsold',
        store=True,
        help="True nếu lô hàng đã quá hạn và vẫn còn số lượng tồn kho > 0."
    )

    # --- 2. CÁC HÀM TÍNH TOÁN (@api.depends) ---

    @api.depends('expiration_date')
    def _compute_days_to_expire(self):
        today = date.today()
        for lot in self:
            if lot.expiration_date:
                diff = lot.expiration_date.date() - today
                lot.days_to_expire = diff.days
            else:
                lot.days_to_expire = 99999

    @api.depends('product_qty')
    def _compute_stored_product_qty(self):
        for lot in self:
            lot.stored_product_qty = lot.product_qty

    @api.depends('stored_product_qty', 'product_id.standard_price')
    def _compute_total_loss_value(self):
        for lot in self:
            lot.total_loss_value = lot.stored_product_qty * lot.unit_cost_price

    @api.depends('expiration_date', 'stored_product_qty')
    def _compute_is_expired_unsold(self):
        today = date.today()
        for lot in self:
            # Điều kiện: Ngày hết hạn < Ngày hôm nay VÀ Tồn kho > 0
            if lot.expiration_date and lot.expiration_date.date() < today and lot.stored_product_qty > 0:
                lot.is_expired_unsold = True
            else:
                lot.is_expired_unsold = False

    # --- 3. CÁC HÀM ĐẶC BIỆT (Gửi Email) ---

    @api.model
    def send_expiry_alert_email(self):
        # 1. Định nghĩa ngày hôm nay và ngày cảnh báo (10 ngày sau)
        today = fields.Date.today()
        upcoming = today + timedelta(days=10)

        # 2. Tìm kiếm lô hàng sắp hết hạn
        products = self.env['stock.lot'].search([
            ('expiration_date', '!=', False),
            ('expiration_date', '<=', upcoming.strftime('%Y-%m-%d')),
            ('expiration_date', '>=', today.strftime('%Y-%m-%d'))
        ])

        if products:
            # 3. Tham chiếu Template (expiry_management là tên module của bạn)
            template_id = self.env.ref('expiry_management.email_template_product_expiry_alert')

            # 4. Tìm địa chỉ Email của Sale Manager
            sales_manager_group = self.env.ref('sales_team.group_sale_manager', raise_if_not_found=False)
            recipient_emails = ','.join(sales_manager_group.users.mapped(
                'email_formatted')) if sales_manager_group and sales_manager_group.users else self.env.user.email_formatted

            # Chọn bản ghi đầu tiên làm bản ghi gốc để kích hoạt Template
            record = products[0]

            # Gửi mail, truyền danh sách lô hàng qua context và ghi đè người nhận
            template_id.with_context(
                expiring_products=products
            ).send_mail(
                record.id,
                force_send=True,
                email_values={'email_to': recipient_emails}
            )