-- get validation set prediction

/*
-- save validation result to a temporary talbe
create temp table valid_result as
    select i.gene_name, i.variation_name, i.gene_id, i.variation_id,
           i.prediction, i.expectation, v.class as actual
    from inference_result i, valid_labels v
    where i.gene_name = v.gene_name and i.variation_name = v.variation_name;
*/
/*
-- count distinct rows with the same gene and variation name, and the same prediction
--create temp table valid_result_count as
    select gene_name, variation_name, prediction, count(prediction) as counts 
    from valid_result
    group by gene_name, variation_name, prediction;
*/
/*
-- combine prediction of rows with the same gene and variation name
-- still has 23 replicated rows
create temp table valid_result_max_count as
    select c.gene_name, c.variation_name, c.prediction, c.counts
    from valid_result_count c
    join
    (
        select gene_name, variation_name, max(counts)
        from valid_result_count
        group by gene_name, variation_name
    ) t1
    on c.gene_name = t1.gene_name and c.variation_name = t1.variation_name
       and c.counts = t1.max;
*/
/*
-- replicated rows select smaller values
create temp table valid_result_distinct as
    select m.gene_name, m.variation_name, m.prediction, m.counts
    from valid_result_max_count m
    join
    (
        select gene_name, variation_name, min(prediction)
        from valid_result_max_count
        group by gene_name, variation_name
    ) t1
    on m.gene_name = t1.gene_name and m.variation_name = t1.variation_name
       and m.prediction = t1.min;
*/ 
-- calculate error rate
select * from
(
    select * from valid_result_distinct d, valid_labels v
    where d.gene_name = v.gene_name and d.variation_name = v.variation_name
) t1
where t1.prediction <> t1.class;