insert into customer_payments
select
    orders.customer_id,
    sum(amount) as total_amount
from raw_payments
left join raw_orders using (order_id)
group by 1;
