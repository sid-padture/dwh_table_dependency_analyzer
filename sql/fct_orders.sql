insert into fct_orders
select
    raw_orders.order_id,
    raw_orders.customer_id,
    raw_orders.order_date,
    raw_orders.status,
    order_payments.credit_card_amount,
    order_payments.coupon_amount,
    order_payments.bank_transfer_amount,
    order_payments.gift_card_amount,
    order_payments.total_amount as amount
from raw_orders
left join order_payments using (order_id);
