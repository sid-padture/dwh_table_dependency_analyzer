# DWH Table Dependency Grapher

Toy project to read queries that move data from raw to models tables within an ELT style data warehouse and graph the dependencies those queries create.

For example, using the example data warehouse schema from the [dbt](https://github.com/fishtown-analytics/jaffle_shop) project an interesting finding we can see is that the models `customer_orders` and `customer_payments` have no dependency on the `raw_customers` source table.

```python
sql_files = ['customer_orders', 'customer_payments', 'dim_customers','fct_orders', 'order_payments']
queries = []
for file in sql_files:
    with open(f'sql/{file}.sql') as sql:
        queries.append(sql.read().strip().replace('\n', ' '))
```

```python
import networkx as nx
import matplotlib.pyplot as plt

from parser import Parser

parser = Parser(queries=queries)

pos = nx.drawing.nx_agraph.graphviz_layout(parser.graph, prog='dot')
nx.draw(parser.graph, pos, with_labels=True, arrows=True)
plt.show()
```

![png](images/graph.png)
    

