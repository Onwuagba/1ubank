1)	**What kind of problems or disadvantages may occur in the handling/maintenance of this list (imagine, that a real world list like this would contain thousands of entries)?**

        Some of the problems/disadvantages that could occur with the list include:

        -	Redundant data, such as the article numbers and currency types, can lead to data inconsistencies and updating these would involve updating all instances of the same data. 
        -	Searching this list would be difficult as the list grows and this would result in sluggish query performance.
        -	The list does not follow best practices in database design in that the data is not normalised and this can lead to data anomalies such as the update anomalies which would occur when article numbers, stored in different places, may not all be updated across board if updated in one location.
        -	Assuming price is to follow global currency standard, the price field should accept decimal values.

2)	**Create a better data model (Entity Relationship Diagram) for these pieces of information.**

        ERD attached to codebase in file erd.png

3)	**Explain why your data model is better than the original list.**

        My model is better than the original list for several reasons:

        -	The data is normalized by separating it into multiple related tables. This minimizes redundancy and data inconsistency.
        -	I used foreign key constraints in the data model to ensure data integrity. It enforces relationships between tables, preventing inconsistencies and errors in the data.
        -	My data model is more scalable because it allows for the addition of new articles and providers without duplicating data. In the original table, each new entry requires repeating the same information, leading to data bloat and potential inconsistencies.
        -	My article model, containing the normalized data, is also indexed to provide better query performance. 

4)	**Create an SQL query that generates the original list again.**

        SELECT
            a.article_no,
            c.currency_name AS article,
            p.provider_no,
            p.provider_name AS provider,
            a.price
        FROM
            app_article a
        JOIN
            app_currency c
        ON
            a.article_id = c.currency_id
        JOIN
            app_provider p
        ON
            a.provider_id = p.provider_no;


