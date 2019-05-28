-- get inference result of whole samples
-- save query result to a new table

create table inference_result as
select c.gene_name, c.variation_name, c.gene_id, c.variation_id, 
       t2.category as prediction, t2.expectation
from gene_variation_candidate c
join 
    (
    -- get inference result from table "dd_inference_result_variables"
    select gene_id, variation_id, t1.expectation, category from dd_inference_result_variables i
    join
        ( select id, max(expectation) as expectation
          from dd_inference_result_variables group by id 
        ) t1
    on i.id = t1.id and i.expectation = t1.expectation
    -- match to gene_id and variation_id through id column in table "has_effect"
    join has_effect e on i.id = e.id
    ) t2
on c.gene_id = t2.gene_id and c.variation_id = t2.variation_id;
