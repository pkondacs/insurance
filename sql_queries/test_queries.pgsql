SELECT * FROM "fct_covers_table" LIMIT 1000;
SELECT * FROM "fct_policies_table" LIMIT 1000;
SELECT * FROM "dim_products" LIMIT 1000;


ALTER TABLE "fct_policies_table" 
    ALTER COLUMN "policy_id" TYPE TEXT
    ALTER COLUMN "transaction_id" TYPE TEXT;
ALTER TABLE "fct_covers_table"
    ALTER COLUMN "cover_premium" TYPE DOUBLE PRECISION USING "cover_premium"::double precision,
    ALTER COLUMN "cover_premium_without_taxes" TYPE DOUBLE PRECISION USING "cover_premium_without_taxes"::double precision,
    ALTER COLUMN "tax_amount" TYPE DOUBLE PRECISION USING "tax_amount"::double precision;
ALTER TABLE "fct_covers_table" 
    ALTER COLUMN "transaction_id" TYPE TEXT USING REPLACE(TRIM(TRAILING '0' FROM REPLACE("transaction_id"::TEXT, '.', '')), '.', '');


SELECT 
    CASES, 
    COUNT(*) FROM (
SELECT 
    coalesce(policies_polids.policy_id,covers_polids.policy_id) as policy_id,
    case 
        when policies_polids.policy_id is not null and covers_polids.policy_id is not null then 'in both'
        when policies_polids.policy_id is not null then 'in policies'
        when covers_polids.policy_id is not null then 'in covers'
        else '' end as cases
FROM 
(select distinct policy_id from "fct_policies_table") as policies_polids
full join 
(select distinct policy_id from "fct_covers_table") as covers_polids
on policies_polids.policy_id = covers_polids.policy_id)
GROUP BY 1;


SELECT * FROM fct_covers_table WHERE policy_id = '100000041251';
SELECT * FROM fct_policies_table WHERE policy_id = '100000041251';


-- select when policy_id was last updated
SELECT *
FROM fct_policies_table
WHERE policy_id = '100000041251'
ORDER BY transaction_date DESC
LIMIT 1;

-- check if within 1 transaction id there are distinct type of cover_id's
SELECT 
    policy_id,
    transaction_id,
    count(cover_id) as count,
    count(distinct cover_id) as count_distinct
from fct_covers_table
group by 1, 2

-- check an example with duplicate cover_id's
SELECT * FROM fct_covers_table 
WHERE policy_id = '100000041251'
AND transaction_id = '3000003162'
AND cover_id = 'BE008'
ORDER BY cover_id;
-- result: object_type (e.g. within a home) is different within a cover_id


-- sum the premiums to check correct type casting cover_premium type
SELECT
    case when cover_premium > 0 then 99999 else cover_premium end as cover_premium,
    count(distinct policy_id)
FROM fct_covers_table 
GROUP BY 1;


-- sum the premiums
SELECT
    case when policy_premium > 0 then 99999 else policy_premium end as policy_premium,
    count(distinct policy_id)
FROM fct_policies_table 
GROUP BY 1;

-- What would be the composite primary key for this table?
SELECT 
    policy_id,
    transaction_id,
    cover_id,
    object_type,
    count(*) as count
from fct_covers_table
group by 1, 2, 3, 4
having count(*) = 1

-- Count the number of policies by product, country, line of business  
SELECT 
    pol.product_id,
    dim.country,
    dim.line_of_business,
    count(distinct pol.policy_id) as count_pols
from fct_policies_table as pol
left join 
dim_products as dim
on pol.product_id = dim.product_id
GROUP by 1, 2, 3


-- Output the sum of the premiums per product for not closed policies
-- 1st nested query: create a 'window' or partition select
-- 2nd main query: select only the most recent transaction for each policy_id
with pol as
    (select *,
    row_number() 
    over (partition by policy_id order by transaction_date desc)
    from fct_policies_table
    WHERE policy_id in 
        ('100000067666',
        '100000041650',
        '100000082765'))
SELECT 
    pol.product_id,
    count(pol.policy_id) as count_pols,
    sum(pol.policy_premium) as sum_premiums 
FROM pol
WHERE pol.row_number = 1 and policy_status <> 'Closed'
GROUP BY 1
