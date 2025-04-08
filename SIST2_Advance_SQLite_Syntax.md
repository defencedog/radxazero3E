# SIST2 SQLITE Queries
No need to use its socker with `elasticseatch`. The `sqlite` backend is more than enough for an SBC & provides proximity searches
> https://github.com/defencedog/radxazero3E/blob/main/CasaOS_yaml/sist2-admin_sqlite.yaml

*Preferably use CAPITAL letters for programming syntax & lower for content syntax to be searched*
> https://www.sqlite.org/fts5.html

## Word & Phrases
```sql
control valve --x2 fixed words
--x1 expandable word (control or controllable or controlling) 
--and x1 fixed word
control* valve 
"control valve" --x1 phrase
```
## Boolean searches
In order of precedence, from highest to lowest, the operators are: 
| Operator | Function |
| --- | --- |
| `query1` NOT `query2` | Matches if query1 matches and query2 does not match |
| `query1` AND `query2` | Matches if both query1 and query2 match. |
| `query1` OR `query2` | Matches if either query1 or query2 match. |

```sql
faraday AND hydrogen --x2 words
faraday OR "hydrogen production" --word & phrase
--Matches documents that contain at least one instance of "flame" and "arrest*" (arrestor or arrestor)
--but do not contain any instances of "safety".
(flame AND arrest*) NOT safety
```
## Proximity searches
*Queries inside NEAR() have no sequence*
```sql
--Matches x1 phrase and x1 fixed word and x1 expandable word (calculation or calculate).
--All x3 queries separated by single space
--In between maximum 30 characters slack possible
NEAR("choke flow" valve calc*, 30)
--Matches x1 phrase and x1 expandable word form and x1 word.
--In between maximum 100 characters slack possible
--OR to be pulled out of NEAR(); cannot use noise OR sound inside NEAR()
NEAR("control valve" vibrat* noise, 100) OR NEAR("control valve" vibrat* sound, 100)
```
