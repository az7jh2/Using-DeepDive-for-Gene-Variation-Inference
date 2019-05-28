/*
-- get number of features belonged to observed variables
-- observed variables: label is not null in table "has_effect"
-- features saved in table "gene_variation_feature"
select count(f.gene_id) from gene_variation_feature f
join 
    -- get observed variables
    (select * from has_effect where label is not null ) observed
on f.gene_id = observed.gene_id and f.variation_id = observed.variation_id;
*/

/*
-- get holdout set result
-- id start from 0 to 68,195
-- id of holdout set saved in table "dd_graph_variables_holdout"
-- inference result saved in table "dd_inference_result_variables"
-- true labels saved in table "has_effect"
-- gene name saved in table "gene_variation_candidate"

-- calculate error rate
select count(id) from (
-- get whole information
select i.id, c.gene_name, c.variation_name,
i.category as prediction, i.expectation, e.label as actual
from dd_inference_result_variables i 
join
    -- get inference result
    (select id, max(expectation) as expectation from (
        -- match holdout set id
        select * from dd_inference_result_variables i
        join dd_graph_variables_holdout h on i.id = h.variable_id 
    ) result1
    group by id) result2
on i.id = result2.id and i.expectation = result2.expectation
join has_effect e on i.id = e.id
join gene_variation_candidate c
on e.gene_id = c.gene_id and e.variation_id = c.variation_id
order by i.id
) result3
where result3.prediction <> result3.actual
*/

-- get validation set result
-- id start from 0 to 68,195
-- validation set saved in table "valid_labels"
-- inference result saved in table dd_inference_result_variables
-- id saved in table has_effect
-- gene name saved in table gene_variation_candidate

-- calculate error rate
select count(gene_name) from (
-- get whole information
-- get validation set
select c.gene_name, c.variation_name, t2.category as prediction, t2.expectation, v.class as actual
from gene_variation_candidate c
join valid_labels v
on c.gene_name = v.gene_name and c.variation_name = v.variation_name
join (
-- get inference result
select gene_id, variation_id, t1.expectation, category from dd_inference_result_variables i
join
    ( select id, max(expectation) as expectation
      from dd_inference_result_variables group by id 
    ) t1
on i.id = t1.id and i.expectation = t1.expectation
join has_effect e
on i.id = e.id
) t2
on c.gene_id = t2.gene_id and c.variation_id = t2.variation_id
) t3
where t3.prediction <> t3.actual