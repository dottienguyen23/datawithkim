import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
# SQL Quest episode catalogue: edit here, rebuild, and the hub updates.
# status: live | soon ; slug used for /sql/<slug>/
WORLDS = [
  {
    'id': 'w1', 'name': 'World 1 · Speak SQL', 'tag': 'beginner', 'color': 'var(--mint)',
    'sub': 'From your first SELECT to building your own tables. By the end you can answer real business questions on your own.',
    'eps': [
      ('ep00', 'ep00-story-of-sql', 'A Short Story of SQL', 'Why SQL exists: Codd, SEQUEL, the optimizer, and the language that refused to die.', 'no lab · history + quiz', 'live', ''),
      ('ep01', 'ep01-first-query', 'Your first query', 'Install PostgreSQL + DBeaver, load a sample shop, and run SELECT, FROM and LIMIT.', 'lab: load the shop database', 'soon', ''),
      ('ep02', 'ep02-better-questions', 'Asking better questions', 'WHERE, AND / OR, IN, BETWEEN, LIKE, ORDER BY, and the NULL trap.', 'lab: find the "lost" orders', 'soon', ''),
      ('ep03', 'ep03-tables-that-talk', 'Tables that talk', 'INNER / LEFT / FULL JOIN, anti-joins, and stacking results with UNION, INTERSECT, EXCEPT.', 'lab: customers who never ordered', 'soon', ''),
      ('ep04', 'ep04-function-toolbox', 'The function toolbox', 'String, number and date functions, CASE logic, COALESCE and clean NULL handling.', 'lab: clean a messy customer list', 'soon', ''),
      ('ep05', 'ep05-counting-things', 'Counting things', 'COUNT, SUM, AVG, GROUP BY, HAVING: turning rows into answers.', 'lab: revenue per country', 'soon', ''),
      ('ep06', 'ep06-build-your-tables', 'Build your own tables', 'DDL vs DML, data types, PRIMARY / FOREIGN KEY, transactions with COMMIT and ROLLBACK.', 'lab: design a mini retail schema', 'soon', 'my SQL2 notes'),
    ]
  },
  {
    'id': 'w2', 'name': 'World 2 · Think like the database', 'tag': 'intermediate', 'color': 'var(--lav)',
    'sub': 'Stop guessing why a query is slow or wrong. Learn what the engine actually does, and the tools pros use every day.',
    'eps': [
      ('ep07', 'ep07-after-enter', 'What happens after Enter', 'Parser → optimizer → executor, execution order, and reading your first EXPLAIN.', 'lab: EXPLAIN five queries', 'soon', 'my SQL2 notes'),
      ('ep08', 'ep08-queries-in-queries', 'Queries inside queries', 'Subqueries, CTEs, WITH RECURSIVE, and temp tables.', 'lab: build an org chart', 'soon', ''),
      ('ep09', 'ep09-window-functions', 'Window functions', 'ROW_NUMBER / RANK / DENSE_RANK, PARTITION BY, named windows, frames, LAG and LEAD.', 'lab: month-over-month sales', 'soon', 'my sql3 notes'),
      ('ep10', 'ep10-code-in-the-db', 'Code that lives in the DB', 'Views, functions, stored procedures and triggers, and when not to use them.', 'lab: an auto updated_at trigger', 'soon', 'my SQL2 notes'),
      ('ep11', 'ep11-make-it-fast', 'Make it fast', 'B-tree, composite, partial and GIN indexes, why an index is ignored, EXPLAIN ANALYZE.', 'lab: the 145× index, extended', 'soon', 'my SQL_1 notes'),
    ]
  },
  {
    'id': 'w3', 'name': 'World 3 · SQL for Data Engineers', 'tag': 'advanced', 'color': 'var(--peach)',
    'sub': 'The SQL that runs pipelines: modeling, safe loading, concurrency, big tables and the modern data stack.',
    'eps': [
      ('ep12', 'ep12-shaping-data', 'Shaping data', 'Normalization vs star schema, fact and dimension tables, surrogate keys.', 'lab: model a fact_SalesLine', 'soon', ''),
      ('ep13', 'ep13-many-users', 'Many users at once', 'Transactions, isolation levels, locks and MVCC.', 'lab: two terminals, one row', 'soon', ''),
      ('ep14', 'ep14-loading-safely', 'Loading data safely', 'COPY, upserts with ON CONFLICT, idempotent loads, SCD Type 2.', 'lab: a rerunnable daily load', 'soon', ''),
      ('ep15', 'ep15-analytics', 'SQL for analytics', 'Exploratory data analysis, running totals, cohorts and segmentation in pure SQL.', 'lab: a customer report in one query', 'soon', ''),
      ('ep16', 'ep16-modern-stack', 'SQL in the modern stack', 'dbt models and tests, SQL from Python, warehouse SQL in Microsoft Fabric.', 'lab: your first dbt project', 'soon', ''),
      ('boss', 'boss-sql-warehouse', 'Boss level: build a SQL data warehouse', 'Raw → staging → star schema → dashboard, end to end, on my home database server.', 'capstone project', 'soon', ''),
    ]
  },
]

def all_eps():
    out = []
    for w in WORLDS:
        for e in w['eps']:
            out.append((w, e))
    return out
