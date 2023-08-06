CREATE OR REPLACE FUNCTION process_agg_variants() RETURNS TRIGGER AS $pcart_agg_variants$
    DECLARE tagset varchar[];
    DECLARE product_tagset varchar[];
    DECLARE variants_tagset varchar[];
    BEGIN
        -- We need the similar behaviour both for INSERT and UPDATE.
        IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
            -- Build an array of tags of all variants.
            tagset := (SELECT ARRAY(
                SELECT
                    concat(ptp.tag_prefix::text, ':'::text, json_data.value::text)
                FROM
                    pcart_catalog_productvariant AS v,
                    jsonb_each_text(v.properties) AS json_data
                INNER JOIN pcart_catalog_producttypeproperty AS ptp ON
                    json_data.key = ptp.title AND
                    json_data.value <> '' AND
                    ptp.tag_prefix <> '' AND
                    ptp.product_type_id = (
                        SELECT t.product_type_id FROM pcart_catalog_product AS t WHERE t.id = NEW.product_id)
                WHERE v.id = NEW.id));

            -- Build an array of tags for parent product (for common properties).
            product_tagset := (SELECT ARRAY(
                SELECT
                    concat(ptp.tag_prefix::text, ':'::text, json_data.value::text)
                FROM
                    pcart_catalog_product AS p,
                    jsonb_each_text(p.properties) AS json_data
                INNER JOIN pcart_catalog_producttypeproperty AS ptp ON
                    json_data.key = ptp.title AND
                    json_data.value <> '' AND
                    ptp.tag_prefix <> '' AND
                    ptp.product_type_id = (
                        SELECT t.product_type_id FROM pcart_catalog_product AS t WHERE t.id = NEW.product_id)
                WHERE p.id = NEW.product_id));

            -- Setup tags for variant. The next operator is necessary for prevent a recursion.
            IF (NEW.tags <> tagset) THEN
                UPDATE pcart_catalog_productvariant SET tags = tagset WHERE id = NEW.id;
            END IF;

            -- Update tags for parent product.
            variants_tagset := (
                SELECT ARRAY(
                    SELECT DISTINCT unnest(v.tags) AS tag
                    FROM pcart_catalog_productvariant AS v
                    WHERE v.product_id = NEW.product_id));

            -- Merge two sets of tags
            UPDATE pcart_catalog_product
            SET tags = (SELECT ARRAY(SELECT DISTINCT unnest(product_tagset || variants_tagset)))
            WHERE id = NEW.product_id;

            -- Update variants count, min/max variant prices.
            UPDATE pcart_catalog_product SET
                (variants_count, min_variant_price, max_variant_price) =
            (SELECT COUNT(*), MIN(v.price), MAX(v.price)
                FROM pcart_catalog_productvariant AS v WHERE v.product_id = NEW.product_id)
            WHERE id = NEW.product_id;
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            -- Build an array of tags of all variants.
            tagset := (SELECT ARRAY(
                SELECT
                    concat(ptp.tag_prefix::text, ':'::text, json_data.value::text)
                FROM
                    pcart_catalog_productvariant AS v,
                    jsonb_each_text(v.properties) AS json_data
                INNER JOIN pcart_catalog_producttypeproperty AS ptp ON
                    json_data.key = ptp.title AND
                    json_data.value <> '' AND
                    ptp.tag_prefix <> '' AND
                    ptp.product_type_id = (
                        SELECT t.product_type_id FROM pcart_catalog_product AS t WHERE t.id = OLD.product_id)
                WHERE v.id = OLD.id));

            -- Build an array of tags for parent product (for common properties).
            product_tagset := (SELECT ARRAY(
                SELECT
                    concat(ptp.tag_prefix::text, ':'::text, json_data.value::text)
                FROM
                    pcart_catalog_product AS p,
                    jsonb_each_text(p.properties) AS json_data
                INNER JOIN pcart_catalog_producttypeproperty AS ptp ON
                    json_data.key = ptp.title AND
                    json_data.value <> '' AND
                    ptp.tag_prefix <> '' AND
                    ptp.product_type_id = (
                        SELECT t.product_type_id FROM pcart_catalog_product AS t WHERE t.id = OLD.product_id)
                WHERE p.id = OLD.product_id));

            -- Update tags for parent product.
            variants_tagset := (
                SELECT ARRAY(
                    SELECT DISTINCT unnest(v.tags) AS tag
                    FROM pcart_catalog_productvariant AS v
                    WHERE v.product_id = OLD.product_id));

            -- Merge two sets of tags
            UPDATE pcart_catalog_product
            SET tags = (SELECT ARRAY(SELECT DISTINCT unnest(product_tagset || variants_tagset)))
            WHERE id = OLD.product_id;

            -- Update variants count, min/max variant prices.
            UPDATE pcart_catalog_product SET
                (variants_count, min_variant_price, max_variant_price) =
            (SELECT COUNT(*), COALESCE(MIN(v.price), 0), COALESCE(MAX(v.price), 0)
                FROM pcart_catalog_productvariant AS v WHERE v.product_id = OLD.product_id)
            WHERE id = OLD.product_id;
            RETURN OLD;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$pcart_agg_variants$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS pcart_agg_variants ON pcart_catalog_productvariant;
CREATE TRIGGER pcart_agg_variants
AFTER INSERT OR UPDATE OR DELETE ON pcart_catalog_productvariant
    FOR EACH ROW EXECUTE PROCEDURE process_agg_variants();
