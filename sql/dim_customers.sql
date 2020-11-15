insert into dim_customers
select
    raw_customers.customer_id,
    customer_orders.first_order,
    customer_orders.most_recent_order,
    customer_orders.number_of_orders,
    customer_payments.total_amount as customer_lifetime_value
from raw_customers
left join customer_orders using (customer_id)
left join customer_payments using (customer_id);
